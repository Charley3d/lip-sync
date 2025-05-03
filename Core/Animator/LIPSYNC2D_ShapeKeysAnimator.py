from typing import Any, Iterator, cast

import bpy

from ..Timeline.LIPSYNC2D_TimeConversion import LIPSYNC2D_TimeConversion
from ...Core.constants import ACTION_SUFFIX_NAME, SLOT_SHAPE_KEY_NAME
from ...Core.types import VisemeData, VisemeSKeyAnimationData, WordTiming
from ...Preferences.LIPSYNC2D_AP_Preferences import LIPSYNC2D_AP_Preferences
from ...lipsync_types import BpyAction, BpyActionKeyframeStrip, BpyActionSlot, BpyContext, BpyObject, \
    BpyPropertyGroup, \
    BpyShapeKey


class LIPSYNC2D_ShapeKeysAnimator:
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
        self._key_blocks: Any
        self.silence_frame_threshold: float = -1
        self.in_between_frame_threshold: float = -1
        self.silence_shape_key_name: str | None = None
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

    @staticmethod
    def get_shape_key_action(obj: BpyObject):
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

        if (obj.data.shape_keys and
                obj.data.shape_keys.animation_data and
                obj.data.shape_keys.animation_data.action):
            return obj.data.shape_keys.animation_data.action

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

        if (action := self.get_shape_key_action(obj)) is None:
            return

        strip = cast(BpyActionKeyframeStrip, action.layers[0].strips[0])
        channelbag = strip.channelbag(self._slot, ensure=True)

        for fcurve in channelbag.fcurves:
            fcurve.keyframe_points.clear()

    def insert_keyframes(self, obj: BpyObject, props: BpyPropertyGroup, visemes_data: VisemeData,
                         word_timing: WordTiming,
                         delay_until_next_word: int, is_last_word: bool, word_index: int):
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
        for shape_key_anim_data in self._insert_on_visemes(obj, props, visemes_data, word_timing):

            for fcurve in self.channelbag.fcurves:
                fcurve: bpy.types.FCurve
                shape_key_name = shape_key_anim_data['shape_key']
                shape_key_data_path = f'key_blocks["{shape_key_name}"].value'
                value = shape_key_anim_data["value"] if shape_key_data_path == fcurve.data_path else 0
                fcurve.keyframe_points.insert(shape_key_anim_data["frame"], value=value, options={"FAST"})
                self.inserted_keyframes += 1

    def insert_silences(self, visemes_data: VisemeData, word_index: int):
        add_sil_at_word_end = (self.delay_until_next_word > self.silence_frame_threshold) or self.is_last_word
        silence_data_path = f'key_blocks["{self.silence_shape_key_name}"].value'

        if add_sil_at_word_end:

            for fcurve in self.channelbag.fcurves:
                fcurve: bpy.types.FCurve
                # Define data-path and value

                value = 1 if silence_data_path == fcurve.data_path else 0

                # Last viseme is inserted a bit before end of word. This ensures that silence uses correct timing
                corrected_word_end_frame = LIPSYNC2D_ShapeKeysAnimator.get_corrected_end_frame(self.word_start_frame,
                                                                                               visemes_data)

                # Add silence after current word, with some delay to allow a smooth motion
                # If close_motion_duration is too high, fallback to next word time-postion minus defined threshold
                frame = corrected_word_end_frame + min(self.delay_until_next_word - self.in_between_frame_threshold,
                                                       self.close_motion_duration)

                fcurve.keyframe_points.insert(frame, value=value, options={"FAST"})
                self.inserted_keyframes += 1

                # Add silence just before the next word.
                # This prevents the lips from sliding unnaturally.
                #TODO previous_start is not updated although new keyframe is inserted. see how to update it
                frame = corrected_word_end_frame + self.delay_until_next_word - max(1, self.in_between_frame_threshold)
                fcurve.keyframe_points.insert(frame, value=value, options={"FAST"})
                self.inserted_keyframes += 1

                if self.is_last_word:
                    frame = corrected_word_end_frame + self.close_motion_duration
                    fcurve.keyframe_points.insert(frame, value=value, options={"FAST"})
                    self.inserted_keyframes += 1

        if self.is_first_word:
            for fcurve in self.channelbag.fcurves:
                fcurve: bpy.types.FCurve
                value = 1 if silence_data_path == fcurve.data_path else 0
                frame = max(LIPSYNC2D_ShapeKeysAnimator.get_frame_start(),
                            self.word_start_frame - max(1, self.close_motion_duration))
                fcurve.keyframe_points.insert(frame, value=value, options={"FAST"})

    def _insert_on_visemes(self, obj: BpyObject, props: BpyPropertyGroup, visemes_data: VisemeData,
                           word_timing: WordTiming) -> Iterator[VisemeSKeyAnimationData]:

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

        if not isinstance(obj.data, bpy.types.Mesh) or obj.data.shape_keys is None:
            yield {"frame": -1, "viseme": "", "value": -1, "shape_key": "", "viseme_index": -1}

        visemes = enumerate(visemes_data["visemes"])

        for viseme_index, v in visemes:
            self.is_last_viseme = (viseme_index + 1) == visemes_data["visemes_len"]
            viseme_frame_start = word_timing["word_frame_start"] + round(viseme_index * visemes_data["visemes_parts"])

            if (
                    # Do not insert a keyframe on a frame that already contains a keyframed shapekey
                    self.has_already_a_kframe(viseme_frame_start)
                    # Do not insert a keyframe if previous keyframe is too close
                    or self.is_prev_kframe_too_close(viseme_frame_start)
                    # Do not insert a keyframe if previous keyframed shapekey was for the same viseme
                    or self.is_redundant(props, v)):
                continue

            yield {
                "frame": viseme_frame_start,
                "viseme": v,
                "viseme_index": viseme_index,
                "value": 1,
                "shape_key": getattr(props, f"lip_sync_2d_viseme_shape_keys_{v}")
            }

            self.previous_start = viseme_frame_start
            self.previous_viseme = v

    def has_already_a_kframe(self, viseme_frame_start):
        return viseme_frame_start == self.previous_start

    def is_prev_kframe_too_close(self, viseme_frame_start):
        return self.previous_start >= 0 and (
                viseme_frame_start - self.previous_start <= self.in_between_frame_threshold)

    def is_redundant(self, props: BpyPropertyGroup, v: str):
        if self.previous_viseme is None or self.previous_viseme == "sil":
            return False

        previous_viseme_prop_name = getattr(props, f'lip_sync_2d_viseme_shape_keys_{self.previous_viseme}')
        viseme_prop_name = getattr(props, f'lip_sync_2d_viseme_shape_keys_{v}')

        return previous_viseme_prop_name == viseme_prop_name

    def set_interpolation(self, obj: BpyObject):
        """
        Sets the interpolation type for all keyframes of the given object's animation
        data to 'LINEAR'. This ensures that the transition between keyframes is linear
        and removes any other interpolation effects.

        :param obj: The Blender object whose animation keyframe interpolation will be
            modified.
        :type obj: BpyObject
        :return: None
        """
        if (action := self.get_shape_key_action(obj)) is None:
            return

        strip = cast(BpyActionKeyframeStrip, action.layers[0].strips[0])

        channelbag = strip.channelbag(self._slot, ensure=True)

        for fcurve in channelbag.fcurves:
            for fcurve in cast(BpyActionKeyframeStrip, action.layers[0].strips[0]).channelbag(
                    action.slots.get(f"KE{SLOT_SHAPE_KEY_NAME}")).fcurves:
                for keyframe in fcurve.keyframe_points:
                    keyframe.interpolation = 'LINEAR'

    @staticmethod
    def reset_shape_keys(key_blocks: Any, viseme_frame_start: float | None = None):
        """
        Resets the values of all shape keys in the provided key blocks to 0 and inserts
        keyframes for those values at the specified frame.

        :param key_blocks: The collection of shape key blocks to reset. Typically
            consists of shape keys associated with an object.
        :type key_blocks: Any
        :param viseme_frame_start: The starting frame at which the keyframe for the
            shape key values will be inserted.
        :type viseme_frame_start: float
        :return: None
        """
        for s in key_blocks:
            s: BpyShapeKey
            if s.name == "Basis": continue
            s.value = 0
            if viseme_frame_start is not None:
                s.keyframe_insert("value", frame=viseme_frame_start)

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
            self.close_motion_duration = self.time_conversion.time_to_frame(props.lip_sync_2d_close_motion_duration)

        if self.time_conversion is None:
            return

        self.silence_frame_threshold = self.time_conversion.time_to_frame(props.lip_sync_2d_sil_threshold)
        self.in_between_frame_threshold = self.time_conversion.time_to_frame(props.lip_sync_2d_in_between_threshold)
        self.silence_shape_key_name = getattr(props, 'lip_sync_2d_viseme_shape_keys_sil')
        self.previous_start = -1
        self.previous_viseme = None
        self.inserted_keyframes = 0

    def setup_animation_properties(self, obj: BpyObject):
        _, strip = self.set_up_action(obj)

        if strip is None:
            return

        self.setup_fcurves(obj, strip)

    def setup_fcurves(self, obj: BpyObject, strip: BpyActionKeyframeStrip):
        if not isinstance(obj.data, bpy.types.Mesh) or obj.data.shape_keys is None:
            return

        self._key_blocks = obj.data.shape_keys.key_blocks
        self.channelbag = strip.channelbag(self._slot, ensure=True)

        for shape_key in self._key_blocks:
            fcurves: bpy.types.ActionChannelbagFCurves
            fcurves = self.channelbag.fcurves
            shape_key_data_path = f'key_blocks["{shape_key.name}"].value'

            if (fcurve := fcurves.find(shape_key_data_path)) is not None:
                fcurves.remove(fcurve)

            fcurves.new(shape_key_data_path)

    def set_up_action(self, obj: BpyObject) -> tuple[BpyAction, BpyActionKeyframeStrip] | tuple[None, None]:
        if not isinstance(obj.data, bpy.types.Mesh):
            return (None, None)

        # Safety check but should never occur because of Operator's poll method
        if obj.data.shape_keys is None:
            return (None, None)
        
        if obj.data.shape_keys.animation_data is None:
            obj.data.shape_keys.animation_data_create()

        if not isinstance(obj.data.shape_keys.animation_data, bpy.types.AnimData):
            return (None, None)

        obj_name = obj.name
        action = bpy.data.actions.get(f"{obj_name}-{ACTION_SUFFIX_NAME}")
        if action is None:
            action = bpy.data.actions.new(f"{obj_name}-{ACTION_SUFFIX_NAME}")
            layer = action.layers.new("Layer")
            strip = cast(bpy.types.ActionKeyframeStrip, layer.strips.new(type='KEYFRAME'))
            obj.data.shape_keys.animation_data.action = action
        else:
            obj.data.shape_keys.animation_data.action = action
            layer = action.layers[0]
            strip = cast(bpy.types.ActionKeyframeStrip, layer.strips[0])

        self._slot = action.slots.get(f"KE{SLOT_SHAPE_KEY_NAME}") or action.slots.new(id_type='KEY', name=f"{SLOT_SHAPE_KEY_NAME}")

        obj.data.shape_keys.animation_data.action = action
        obj.data.shape_keys.animation_data.action_slot = self._slot

        return action, strip

    def cleanup(self, obj: BpyObject):
        self.reset_shape_keys(self._key_blocks)

    def poll(self, cls, context: BpyContext):
        obj = context.active_object

        if obj is None or not isinstance(obj.data, bpy.types.Mesh):
            return False

        if obj.data.shape_keys is None:
            return False

        model_state = LIPSYNC2D_AP_Preferences.get_model_state()

        return (context.scene is not None or context.active_object is not None) and model_state != "DOWNLOADING"

    @staticmethod
    def get_fps_range() -> int:
        if bpy.context.scene is None:
            return -1

        return bpy.context.scene.frame_end - bpy.context.scene.frame_start

    @staticmethod
    def get_frame_start():
        if bpy.context.scene is None:
            return -1

        return bpy.context.scene.frame_start

    @staticmethod
    def get_corrected_end_frame(word_start_frame, visemes_data: VisemeData) -> int:
        return word_start_frame + round(visemes_data["visemes_parts"] * (visemes_data["visemes_len"] - 1))
