from typing import Any

import bpy

from ..Timeline.LIPSYNC2D_TimeConversion import LIPSYNC2D_TimeConversion

from ...LIPSYNC2D_Utils import get_package_name

from ...Core.types import VisemeData, WordTiming
from ...lipsync_types import BpyActionSlot, BpyContext, BpyObject, BpyPropertyGroup, BpyShapeKey


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

    last_word_motion_duration = .200
    last_word_motion_duration_frame = 0

    def __init__(self) -> None:
        self._slot: BpyActionSlot
        self._key_blocks: Any

    @staticmethod
    def get_shape_key_action(obj):
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

        strip = action.layers[0].strips[0]
        channelbag = strip.channelbag(self._slot, ensure=True)

        for fcurve in channelbag.fcurves:
            fcurve.keyframe_points.clear()

    def insert_on_visemes(self, obj: BpyObject, props: BpyPropertyGroup, visemes_data: VisemeData,
                          word_timing: WordTiming,
                          delay_until_next_word: int, is_last_word: bool, words: list[Any], word_index: int):
        """
        Insert viseme animations based on given viseme data, word timing, and properties. This function ensures
        that the shape keys for lip-sync animations are manipulated and keyframed correctly for smooth transitions
        between viseme states. It also optionally adds a silence (SIL) shape key at the end of a word depending
        on specific conditions.

        :param obj: The Blender object to insert visemes into.
        :param props: Properties related to lipsync and shape key data.
        :param visemes_data: Data about visemes, including their order and division details.
        :param word_timing: Timing information for the word's animation frames.
        :param delay_until_next_word: A delay value used to determine if silence should be inserted between words.
        :param is_last_word: Indicates whether the current word is the last word in the sequence.
        :return: None
        """

        if not isinstance(obj.data, bpy.types.Mesh) or obj.data.shape_keys is None:
            return

        key_blocks = self._key_blocks
        visemes = enumerate(visemes_data["visemes"])
        vis_len = len(visemes_data["visemes"])
        # If there is more visemes than this threshold, shape key will be proportionally decreased
        viseme_threshold = 3
        # Before inserting new Keyframe, go back this number of frame and set all Shapes Keys to 0
        before_frame = 2

        for viseme_index, v in visemes:
            

            add_sil_at_word_end = ((delay_until_next_word > self.time_conversion.time_to_frame(.1)) and (viseme_index + 1) == visemes_data[
                "visemes_len"]) or is_last_word
            viseme_frame_start = word_timing["word_frame_start"] + round(viseme_index * visemes_data["visemes_parts"])

            LIPSYNC2D_ShapeKeysAnimator.reset_shape_keys(key_blocks, viseme_frame_start)
            shape_key_prop = getattr(props, f"lip_sync_2d_viseme_shape_keys_{v}")
            shape_key = key_blocks.get(shape_key_prop)

            if shape_key is not None:
                delay = max(0,delay_until_next_word)
                shape_key.value = viseme_threshold / vis_len
                shape_key.keyframe_insert("value", frame=viseme_frame_start)
            
                if add_sil_at_word_end:
                    # Force Current Shape Key value to 0 at the end of word, with a delay to prevent snap effect
                    shape_key.value = 0
                    shape_key.keyframe_insert("value", frame=word_timing["word_frame_end"] + min(delay, self.last_word_motion_duration_frame))

                    # To prevent lips sliping, ensure that previous shape key is set to 0, set all of Shapes Keys to 0 too
                    for s in key_blocks:
                        s.value = 0
                        s.keyframe_insert("value", frame=word_timing["word_frame_end"] + delay - before_frame)

                    # Force the SIL shape key to 1
                    shape_key_prop = getattr(props, f"lip_sync_2d_viseme_shape_keys_sil")
                    shape_key = key_blocks.get(shape_key_prop)

                    if shape_key is not None:
                        shape_key.value = 1
                        shape_key.keyframe_insert("value", frame=word_timing["word_frame_end"] + min(delay, self.last_word_motion_duration_frame))
                
                # Force SIL before very first word of dialog
                if word_index == 0 and viseme_index == 0:
                    shape_key.value = 0
                    shape_key.keyframe_insert("value", frame=viseme_frame_start - 1)

                    shape_key_prop = getattr(props, f"lip_sync_2d_viseme_shape_keys_sil")
                    shape_key = key_blocks.get(shape_key_prop)

                    shape_key.value = 1
                    shape_key.keyframe_insert("value", frame=viseme_frame_start - 1)


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
        action = obj.animation_data.action if obj.animation_data else None

        if action:
            for fcurve in action.fcurves:
                for keyframe in fcurve.keyframe_points:
                    keyframe.interpolation = 'LINEAR'

    @staticmethod
    def reset_shape_keys(key_blocks: Any, viseme_frame_start: float):
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
            s.value = 0
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
        if not isinstance(obj.data, bpy.types.Mesh):
            return

        if obj.animation_data is None or obj.data.shape_keys is None or obj.data.shape_keys.animation_data is None:
            return

        obj_name = obj.name
        action = bpy.data.actions.get(f"{obj_name}-LipSyncAction")

        if action is None:
            action = bpy.data.actions.new(f"{obj_name}-LipSyncAction")
            layer = action.layers.new("Layer")
            layer.strips.new(type='KEYFRAME')
            obj.data.shape_keys.animation_data.action = action

        self._slot = action.slots.get("KELipSync") or action.slots.new(id_type='KEY', name="LipSync")
        self._key_blocks = obj.data.shape_keys.key_blocks

        obj.data.shape_keys.animation_data.action = action
        obj.data.shape_keys.animation_data.action_slot = self._slot

        if bpy.context.scene is not None:
            self.time_conversion = LIPSYNC2D_TimeConversion(bpy.context.scene.render)

            self.last_word_motion_duration_frame = self.time_conversion.time_to_frame(self.last_word_motion_duration)

    def cleanup(self, obj: BpyObject):
        pass

    def poll(self, cls, context: BpyContext):
        obj = context.active_object

        if obj is None or not isinstance(obj.data, bpy.types.Mesh):
            return False
        
        if obj.data.shape_keys is None:
            return False
        
        package_name = get_package_name()
        prefs = context.preferences.addons[package_name].preferences  # type: ignore
        return (context.scene is not None or context.active_object is not None) and prefs.is_downloading is False
