import tracemalloc
from typing import Iterator, Literal, cast

import bpy

from .LIPSYNC2D_ShapeKeysAnimator import LIPSYNC2D_ShapeKeysAnimator


from ..phoneme_to_viseme import viseme_items_mpeg4_v2

from ..Timeline.LIPSYNC2D_TimeConversion import LIPSYNC2D_TimeConversion
from ..constants import ACTION_SUFFIX_NAME, SLOT_POSE_LIB_NAME
from ..Timeline.LIPSYNC2D_Timeline import LIPSYNC2D_Timeline
from ..types import (
    VisemeActionAnimationData,
    VisemeData,
    WordTiming,
)
from ...Preferences.LIPSYNC2D_AP_Preferences import LIPSYNC2D_AP_Preferences
from ...lipsync_types import (
    BpyAction,
    BpyActionChannelbag,
    BpyActionKeyframeStrip,
    BpyActionSlot,
    BpyContext,
    BpyObject,
    BpyPropertyGroup,
)


class LIPSYNC2D_PoseLibraryAnimator:
    """
    A class designed to manage lip-sync animation using shape keys in Blender.

    This class provides methods for manipulating shape key animations, including clearing
    existing keyframes, setting up new animations, modifying interpolation types, and inserting
    keyframes for viseme data.

    :ivar _slot: Internal storage representing a reference to an action slot used in
        the animation chain for lip-syncing (assigned during setup phase).
    :type _slot: BpyActionSlot
    """

    def __init__(self) -> None:
        self._slot: BpyActionSlot | None = None
        self.pose_assets_actions: dict[str, bpy.types.Action]
        self.silence_frame_threshold: float = -1
        self.in_between_frame_threshold: float = -1
        self.previous_start: int = -1
        self.previous_viseme: str | None = None
        self.inserted_keyframes: int = 0
        self.word_end_frame = -1
        self.word_start_frame = -1
        self.delay_until_next_word = -1
        self.is_last_word = False
        self.is_first_word = False
        self.time_conversion = None
        self.close_motion_duration = -1
        self.channelbag: BpyActionChannelbag
        self.armature: BpyObject | None = None

    def get_armature_action(self, obj: BpyObject):
        """
        Retrieves the action associated with the shape keys of the given object, if available.

        This function checks if the provided object has shape keys defined. If shape keys
        are present and they have associated animation data and an assigned action, the
        function returns the action. If any of these conditions fail, the function returns None.

        :param obj: The object to retrieve the shape key action from.
        :type obj: Any
        :return: The action associated with the object's shape keys if available, otherwise None.
        :rtype: Any or None
        """
        if not isinstance(obj.data, bpy.types.Mesh):
            return None

        if (
            self.armature
            and self.armature.animation_data
            and self.armature.animation_data.action
        ):
            return self.armature.animation_data.action

        return None

    def clear_previous_keyframes(self, obj: BpyObject):
        """
        Clears all previous keyframes from the shape key action's channelbag for
        the provided object, ensuring the removal of existing animation
        data within the specified context.

        :param obj: The Blender object from which previous keyframes are to be
            cleared. Must have a mesh data type.
        :type obj: BpyObject
        :return: This function does not return any value. If the provided object
            does not meet the required conditions (e.g., not a mesh or has no
            trackable action), the function terminates without modification.
        :rtype: None
        """
        if not isinstance(obj.data, bpy.types.Mesh):
            return

        if (action := self.get_armature_action(obj)) is None:
            return

        strip = cast(BpyActionKeyframeStrip, action.layers[0].strips[0])
        channelbag = strip.channelbag(self._slot, ensure=True)

        for fcurve in channelbag.fcurves:
            fcurve.keyframe_points.clear()

    def insert_keyframes(
        self,
        obj: BpyObject,
        props: BpyPropertyGroup,
        visemes_data: VisemeData,
        word_timing: WordTiming,
        delay_until_next_word: int,
        is_last_word: bool,
        word_index: int,
    ):
        """
        Insert viseme animations based on given viseme data, word timing, and properties. This function ensures
        that the shape keys for lip-sync animations are manipulated and keyframed correctly for smooth transitions
        between viseme states. It also optionally adds a silence (SIL) shape key at the end of a word depending
        on specific conditions.

        :param word_index: Word index
        :param obj: The Blender object to insert visemes into.
        :param props: Properties related to lipsync and shape key data.
        :param visemes_data: Data about visemes, including their order and division details.
        :param word_timing: Timing information for the word's animation frames.
        :param delay_until_next_word: A delay value used to determine if silence should be inserted between words.
        :param is_last_word: Indicates whether the current word is the last word in the sequence.
        :return: None
        """

        # Initialize word properties
        self.word_end_frame = word_timing["word_frame_end"]
        self.word_start_frame = word_timing["word_frame_start"]
        self.delay_until_next_word = max(0, delay_until_next_word)
        self.is_last_word = is_last_word
        self.is_first_word = word_index == 0

        # Insert silences before or after word when needed
        self.insert_silences(visemes_data, word_index)

        # Iterate through visemes and insert keyframes on time
        for action_anim_data in self._insert_on_visemes(
            obj, props, visemes_data, word_timing
        ):
            if (action := action_anim_data["action"]) is None:
                continue

            self.insert_keyframe_points(action, action_anim_data["frame"])

    def insert_keyframe_points(
        self,
        pose_action: BpyAction,
        frame: int,
        interpolation: Literal["LINEAR"] = "LINEAR",
    ):
        for fcurve in self.channelbag.fcurves:
            pose_asset_fcurve = pose_action.fcurves.find(
                fcurve.data_path, index=fcurve.array_index
            )
            if pose_asset_fcurve is None:
                continue

            # Since Action is from a Pose Asset, we can safely assume that first keyframe point holds the Pose
            fcurve_value = pose_asset_fcurve.keyframe_points[0].co.y
            kframe = fcurve.keyframe_points.insert(
                frame,
                value=fcurve_value,
            )
            kframe.interpolation = interpolation
            self.inserted_keyframes += 1

    def insert_silences(self, visemes_data: VisemeData, word_index: int):
        add_sil_at_word_end = (
            self.delay_until_next_word > self.silence_frame_threshold
        ) or self.is_last_word
        action: BpyAction = getattr(self.props, f"lip_sync_2d_viseme_pose_sil")

        if add_sil_at_word_end:

            # Last viseme is inserted a bit before end of word. This ensures that silence uses correct timing
            corrected_word_end_frame = (
                LIPSYNC2D_ShapeKeysAnimator.get_corrected_end_frame(
                    self.word_start_frame, visemes_data
                )
            )
            frame = corrected_word_end_frame + max(
                1,
                min(
                    self.delay_until_next_word - self.in_between_frame_threshold,
                    self.close_motion_duration,
                ),
            )

            if not self.is_last_word:
                # Add silence after current word, with some delay to allow a smooth motion
                # If close_motion_duration is too high, fallback to next word time-postion minus defined threshold
                frame = corrected_word_end_frame + max(
                    1,
                    min(
                        self.delay_until_next_word - self.in_between_frame_threshold,
                        self.close_motion_duration,
                    ),
                )
                self.insert_keyframe_points(action, int(frame))

                frame = (
                    corrected_word_end_frame
                    + self.delay_until_next_word
                    - max(1, self.in_between_frame_threshold)
                )
                self.insert_keyframe_points(action, int(frame))
            else:
                frame = corrected_word_end_frame + self.close_motion_duration
                self.insert_keyframe_points(action, int(frame))

        if self.is_first_word:

            frame = max(
                LIPSYNC2D_Timeline.get_frame_start(),
                self.word_start_frame - max(1, self.close_motion_duration / 2),
            )
            self.insert_keyframe_points(action, int(frame))

    def _insert_on_visemes(
        self,
        obj: BpyObject,
        props: BpyPropertyGroup,
        visemes_data: VisemeData,
        word_timing: WordTiming,
    ) -> Iterator[VisemeActionAnimationData]:
        """
        Insert viseme animations based on given viseme data, word timing, and properties. This function ensures
        that the shape keys for lip-sync animations are manipulated and keyframed correctly for smooth transitions
        between viseme states. It also optionally adds a silence (SIL) shape key at the end of a word depending
        on specific conditions.

        :param word_index: Word index
        :param obj: The Blender object to insert visemes into.
        :param props: Properties related to lipsync and shape key data.
        :param visemes_data: Data about visemes, including their order and division details.
        :param word_timing: Timing information for the word's animation frames.
        :param delay_until_next_word: A delay value used to determine if silence should be inserted between words.
        :param is_last_word: Indicates whether the current word is the last word in the sequence.
        :return: None
        """

        if not isinstance(obj.data, bpy.types.Mesh):
            yield {
                "frame": -1,
                "viseme": "",
                "action": None,
                "action_name": "",
                "viseme_index": -1,
            }

        visemes = enumerate(visemes_data["visemes"])

        for viseme_index, v in visemes:
            self.is_last_viseme = (viseme_index + 1) == visemes_data["visemes_len"]
            viseme_frame_start = word_timing["word_frame_start"] + round(
                viseme_index * visemes_data["visemes_parts"]
            )

            if (
                # Do not insert a keyframe on a frame that already contains a keyframe
                self.has_already_a_kframe(viseme_frame_start)
                # Do not insert a keyframe if previous keyframe is too close
                or self.is_prev_kframe_too_close(viseme_frame_start)
                # Do not insert a keyframe if previous keyframe was for the same viseme
                or self.is_redundant(props, v)
            ):
                continue

            action_name: str = getattr(props, f"lip_sync_2d_viseme_pose_{v}")
            action = self.pose_assets_actions[v]
            # self.pose_assets_fcurves.
            yield {
                "frame": viseme_frame_start,
                "viseme": v,
                "action": action,
                "viseme_index": viseme_index,
                "action_name": action_name,
            }

            self.previous_start = viseme_frame_start
            self.previous_viseme = v

    def has_already_a_kframe(self, viseme_frame_start):
        return viseme_frame_start == self.previous_start

    def is_prev_kframe_too_close(self, viseme_frame_start):
        return self.previous_start >= 0 and (
            viseme_frame_start - self.previous_start <= self.in_between_frame_threshold
        )

    def is_redundant(self, props: BpyPropertyGroup, v: str):
        if self.previous_viseme is None or self.previous_viseme == "sil":
            return False

        previous_viseme_prop_name = getattr(
            props, f"lip_sync_2d_viseme_pose_{self.previous_viseme}"
        )
        viseme_prop_name = getattr(props, f"lip_sync_2d_viseme_pose_{v}")

        return previous_viseme_prop_name == viseme_prop_name

    def set_interpolation(self, obj: BpyObject):
        pass

    def setup(self, obj: BpyObject):
        """
        Sets up the animation action and its components for the provided Blender object
        if it meets the necessary conditions. Verifies the object's data type and animation
        data, ensures that a specific action exists for lip-syncing, and assigns it to the
        shape key animation data.

        :param obj: The Blender object for which the lip-sync animation is being set up.
                    Must have a data type of Mesh and support animation data.
        :type obj: BpyObject
        :return: None if the object does not meet the specified conditions for setup.
        :rtype: None
        """

        self.setup_properties(obj)
        self.setup_animation_properties(obj)

    def setup_properties(self, obj: BpyObject):
        props = obj.lipsync2d_props  # type: ignore

        if bpy.context.scene is not None:
            self.time_conversion = LIPSYNC2D_TimeConversion(bpy.context.scene.render)
            self.close_motion_duration = self.time_conversion.time_to_frame(
                props.lip_sync_2d_close_motion_duration
            )

        if self.time_conversion is None:
            return

        self.silence_frame_threshold = self.time_conversion.time_to_frame(
            props.lip_sync_2d_sil_threshold
        )
        self.in_between_frame_threshold = self.time_conversion.time_to_frame(
            props.lip_sync_2d_in_between_threshold
        )
        self.previous_start = -1
        self.previous_viseme = None
        self.inserted_keyframes = 0
        self.props = props
        self.armature = getattr(props, "lip_sync_2d_armature_to_animate")

    def setup_animation_properties(self, obj: BpyObject):
        _, strip = self.set_up_action(obj)

        if strip is None:
            return

        self.setup_fcurves(obj, strip)

    def get_available_actions(self) -> dict[str, bpy.types.Action]:
        visemes = viseme_items_mpeg4_v2(None, None)

        available_actions: dict[str, bpy.types.Action] = {
            enum_id: key
            for (enum_id, _, _) in visemes
            if (key := getattr(self.props, f"lip_sync_2d_viseme_pose_{enum_id}"))
            is not None
        }

        return available_actions

    def setup_fcurves(self, obj: BpyObject, strip: BpyActionKeyframeStrip):
        if not isinstance(obj.data, bpy.types.Mesh):
            return
        tracemalloc.start()
        props = obj.lipsync2d_props  # type: ignore
        is_basic_rig = props.lip_sync_2d_rig_type_basic
        self.pose_assets_actions = self.get_available_actions()
        self.channelbag = strip.channelbag(self._slot, ensure=True)
        fcurves = self.channelbag.fcurves

        if props.lip_sync_2d_use_clear_keyframes:
            fcurves.clear()

        seen_actions = set()
        bone_groups_cache = {}

        for action in self.pose_assets_actions.values():
            action_id = id(action)
            if action_id in seen_actions:
                continue

            seen_actions.add(action_id)

            if (
                len(action.layers) == 0
                or len(action.layers[0].strips) == 0
                or not isinstance(
                    pose_strip := action.layers[0].strips[0],
                    bpy.types.ActionKeyframeStrip,
                )
                or len(action.slots) == 0
            ):
                continue  # Skip malformed actions

            pose_channelbag = pose_strip.channelbag(action.slots[0])

            for fcurve in pose_channelbag.fcurves:
                if fcurves.find(fcurve.data_path, index=fcurve.array_index):
                    continue

                property_name = fcurve.data_path.split(".")[-1]

                if is_basic_rig and (
                    "bbone" in fcurve.data_path
                    or property_name
                    not in {
                        "location",
                        "rotation_euler",
                        "rotation_quaternion",
                        "scale",
                    }
                ):
                    continue

                new_fcurve = fcurves.new(fcurve.data_path, index=fcurve.array_index)

                if "pose.bones[" in fcurve.data_path:
                    bone_name = fcurve.data_path.split('"')[1]

                    if bone_name not in bone_groups_cache:
                        bone_groups_cache[bone_name] = self.channelbag.groups.get(
                            bone_name
                        ) or self.channelbag.groups.new(bone_name)

                    new_fcurve.group = bone_groups_cache[bone_name]

        current, peak = tracemalloc.get_traced_memory()
        print(f"Current memory usage: {current / 1024 :.3f} kb")
        print(f"Peak memory usage: {peak / 1024 :.3f} kb")

        tracemalloc.stop()

    def set_up_action(
        self, obj: BpyObject
    ) -> tuple[BpyAction, BpyActionKeyframeStrip] | tuple[None, None]:
        if not isinstance(obj.data, bpy.types.Mesh):
            return (None, None)

        # Safety check but should never occur because of Operator's poll method
        if self.armature is None:
            return (None, None)

        if self.armature.animation_data is None:
            self.armature.animation_data_create()

        if not isinstance(self.armature.animation_data, bpy.types.AnimData):
            return (None, None)

        obj_name = obj.name
        action = bpy.data.actions.get(f"{obj_name}-{ACTION_SUFFIX_NAME}")
        if action is None:
            action = bpy.data.actions.new(f"{obj_name}-{ACTION_SUFFIX_NAME}")
            layer = action.layers.new("Layer")
            strip = cast(
                bpy.types.ActionKeyframeStrip, layer.strips.new(type="KEYFRAME")
            )
            self.armature.animation_data.action = action
        else:
            self.armature.animation_data.action = action
            layer = action.layers[0]
            strip = cast(bpy.types.ActionKeyframeStrip, layer.strips[0])

        self._slot = action.slots.get(f"OB{SLOT_POSE_LIB_NAME}") or action.slots.new(
            id_type="OBJECT", name=f"{SLOT_POSE_LIB_NAME}"
        )

        self.armature.animation_data.action = action
        self.armature.animation_data.action_slot = self._slot

        return action, strip

    def cleanup(self, obj: BpyObject):
        pass

    def poll(self, cls, context: BpyContext):
        obj = context.active_object

        if obj is None or not isinstance(obj.data, bpy.types.Mesh):
            return False

        props = getattr(obj, "lipsync2d_props")
        if props is None or getattr(props, f"lip_sync_2d_armature_to_animate") is None:
            return False

        model_state = LIPSYNC2D_AP_Preferences.get_model_state()

        return (
            context.scene is not None or context.active_object is not None
        ) and model_state != "DOWNLOADING"

    @staticmethod
    def get_corrected_end_frame(word_start_frame, visemes_data: VisemeData) -> int:
        return word_start_frame + round(
            visemes_data["visemes_parts"] * (visemes_data["visemes_len"] - 1)
        )
