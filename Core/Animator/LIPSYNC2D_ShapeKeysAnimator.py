from typing import Any, cast

import bpy

from ..Timeline.LIPSYNC2D_TimeConversion import LIPSYNC2D_TimeConversion

from ...LIPSYNC2D_Utils import get_package_name

from ...Core.types import VisemeData, VisemeSKeyAnimationData, WordTiming
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
        self.active_keyframes: list[VisemeSKeyAnimationData] = []
        self.silence_frame_threshold: float
        self.in_between_frame_threshold: float
        self.silence_shape_key_name: str
        self.add_sil_at_word_end: bool = False
        self.previous_start = -1
        self.previous_viseme = None
        self.inserted_keyframes = 0

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

        self.word_frame_end = word_timing["word_frame_end"]
        self.word_frame_start = word_timing["word_frame_start"]
        self.delay_until_next_word = delay_until_next_word
        self.is_last_word = is_last_word


        add_sil_at_word_end = ((self.delay_until_next_word > self.silence_frame_threshold)) or is_last_word

        if add_sil_at_word_end:
            delay = max(0, self.delay_until_next_word)

            # print(f"LAst word: {add_sil_at_word_end} @{self.word_frame_end} - {(delay_until_next_word > self.silence_frame_threshold)}  - {is_last_word}")
            for fcurve in self.channelbag.fcurves:
                fcurve:bpy.types.FCurve
                shape_key_data_path = f'key_blocks["{self.silence_shape_key_name}"].value'
                value = 1 if shape_key_data_path == fcurve.data_path else 0
                
                frame = self.word_frame_end + min(delay - self.in_between_frame_threshold, self.last_word_motion_duration_frame)
                fcurve.keyframe_points.insert(frame, value=value, options={"FAST"})
                self.inserted_keyframes += 1

                frame = self.word_frame_end + delay - max(1,self.in_between_frame_threshold)
                fcurve.keyframe_points.insert(frame, value=value, options={"FAST"})
                self.inserted_keyframes += 1

        for t in self._insert_on_visemes(obj, props, visemes_data, word_timing, delay_until_next_word, is_last_word, word_index):
                
            for fcurve in self.channelbag.fcurves:
                fcurve:bpy.types.FCurve
                shape_key_name = t['shape_key']
                shape_key_data_path = f'key_blocks["{shape_key_name}"].value'
                value = t["value"] if shape_key_data_path == fcurve.data_path else 0
                fcurve.keyframe_points.insert(t["keyframe"], value=value, options={"FAST"})
                self.inserted_keyframes += 1

                

                
        # yield {"keyframe": -1, "viseme": "", "value": -1}
    def _insert_on_visemes(self, obj: BpyObject, props: BpyPropertyGroup, visemes_data: VisemeData,
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

        if not isinstance(obj.data, bpy.types.Mesh) or obj.data.shape_keys is None:
            yield {"keyframe": -1, "viseme": "", "value": -1, "shape_key": "", "viseme_index": -1}


        key_blocks = self._key_blocks
        visemes = enumerate(visemes_data["visemes"])
        in_between_threshold = props.lip_sync_2d_in_between_threshold # type: ignore

        for viseme_index, v in visemes:
            self.is_last_viseme = (viseme_index + 1) == visemes_data["visemes_len"]
            # sil_threshold = props.lip_sync_2d_sil_threshold # type: ignore
            # add_sil_at_word_end = ((delay_until_next_word > self.silence_frame_threshold) 
            #                        and (viseme_index + 1) == visemes_data["visemes_len"]) or is_last_word
            
            # This is done to ensure that we catch the very last part of our viseme total duration
            # index = viseme_index if not self.is_last_viseme else viseme_index + 1
            viseme_frame_start = word_timing["word_frame_start"] + round(viseme_index * visemes_data["visemes_parts"])

            
            # Do not insert a keyframe on a frame that alread contains a keyframed shapekey
            if viseme_frame_start == self.previous_start: continue

            if self.previous_start >= 0 and viseme_frame_start - self.previous_start <= self.in_between_frame_threshold:
                continue

            if viseme_frame_start == 805:
                print(self.previous_viseme, v)
            
            if (self.previous_viseme and self.previous_viseme != "sil") and getattr(props, f'lip_sync_2d_viseme_shape_keys_{self.previous_viseme}') == getattr(props, f'lip_sync_2d_viseme_shape_keys_{v}'):
                continue

            self.add_sil_at_word_end = ((self.delay_until_next_word > self.silence_frame_threshold) 
                                   and self.is_last_viseme) or is_last_word


            # delay = max(0,delay_until_next_word)
            # shape_key.value = 1
            # shape_key.keyframe_insert("value", frame=max(self.get_frame_start(), viseme_frame_start))
            yield {
                "keyframe": viseme_frame_start, 
                "viseme": v, 
                "viseme_index": viseme_index,
                "value": 1, 
                "shape_key": getattr(props, f"lip_sync_2d_viseme_shape_keys_{v}")
                }

            self.previous_start = viseme_frame_start
            self.previous_viseme = v

        # if add_sil_at_word_end:
        #     # Force the SIL shape key to 1
        #     shape_key_prop = getattr(props, f"lip_sync_2d_viseme_shape_keys_sil")
        #     shape_key = key_blocks.get(shape_key_prop)

        #     # Add sil right after viseme, respecting the last_word_motion_duration_frame duration. If last_word_motion_duration_frame is longer than delay, falloff to delay
        #     self.active_keyframes.append({"keyframe": word_timing["word_frame_end"] + min(delay - self.time_conversion.time_to_frame(in_between_threshold), self.last_word_motion_duration_frame), "viseme": "sil"})
        #     # Add sil just before the next viseme
        #     self.active_keyframes.append({"keyframe": word_timing["word_frame_end"] + delay - max(1,self.time_conversion.time_to_frame(in_between_threshold)), "viseme": "sil"})
        
        # # Force SIL before very first word of dialog
        # if word_index == 0 and viseme_index == 0:
        #     self.active_keyframes.append({"keyframe": max(1, viseme_frame_start - self.time_conversion.time_to_frame(in_between_threshold)), "viseme": "sil"})

        

    def insert_on_silence(self):
        
        delay = max(0, self.delay_until_next_word)
        # add_sil_at_word_end = ((self.delay_until_next_word > self.silence_frame_threshold) and self.is_last_viseme) or self.is_last_word
        
        a = {"keyframe": self.word_frame_end + min(delay - self.in_between_frame_threshold, self.last_word_motion_duration_frame), "viseme": "sil"}
        b = {"keyframe": self.word_frame_end + delay - max(1,self.in_between_frame_threshold), "viseme": "sil"}
        
        # Force SIL before very first word of dialog
        c = {"keyframe": max(1, self.word_frame_start - self.in_between_frame_threshold), "viseme": "sil"}

        return [f["keyframe"] for f in [a,b,c]]

        # yield {"keyframe": frame, "viseme": viseme, "value": value, "shape_key": getattr(props, f"lip_sync_2d_viseme_shape_keys_{viseme}")}



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


        strip = action.layers[0].strips[0]
        channelbag = strip.channelbag(self._slot, ensure=True)

        for fcurve in channelbag.fcurves:
            for fcurve in action.layers[0].strips[0].channelbag(action.slots.get("KELipSync")).fcurves:
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
        if not isinstance(obj.data, bpy.types.Mesh):
            return

        if obj.animation_data is None or obj.data.shape_keys is None or obj.data.shape_keys.animation_data is None:
            return
        
        if bpy.context.scene is not None:
            self.time_conversion = LIPSYNC2D_TimeConversion(bpy.context.scene.render)
            self.last_word_motion_duration_frame = self.time_conversion.time_to_frame(self.last_word_motion_duration)

        obj_name = obj.name
        props = obj.lipsync2d_props #type: ignore
        action = bpy.data.actions.get(f"{obj_name}-LipSyncAction")

        self.silence_frame_threshold = self.time_conversion.time_to_frame(props.lip_sync_2d_sil_threshold)
        self.in_between_frame_threshold = self.time_conversion.time_to_frame(props.lip_sync_2d_in_between_threshold)
        self.silence_shape_key_name = getattr(props, 'lip_sync_2d_viseme_shape_keys_sil')

        if action is None:
            action = bpy.data.actions.new(f"{obj_name}-LipSyncAction")
            layer = action.layers.new("Layer")
            strip = cast(bpy.types.ActionKeyframeStrip, layer.strips.new(type='KEYFRAME'))
            obj.data.shape_keys.animation_data.action = action
        else:
            layer = action.layers[0]
            strip = cast(bpy.types.ActionKeyframeStrip, layer.strips[0])


        self._slot = action.slots.get("KELipSync") or action.slots.new(id_type='KEY', name="LipSync")
        self._key_blocks = obj.data.shape_keys.key_blocks
        self.channelbag = strip.channelbag(self._slot, ensure=True)

        for shape_key in self._key_blocks:
            fcurves: bpy.types.ActionChannelbagFCurves
            fcurves = self.channelbag.fcurves
            shape_key_data_path = f'key_blocks["{shape_key.name}"].value'
            
            if fcurves.find(shape_key_data_path) == None:
                fcurves.new(shape_key_data_path)

        obj.data.shape_keys.animation_data.action = action
        obj.data.shape_keys.animation_data.action_slot = self._slot

        
        


    def cleanup(self, obj: BpyObject):
        self.reset_shape_keys(self._key_blocks)

        # Ensure keyframes are well sorted
        self.active_keyframes.sort(key=lambda x: x["keyframe"])
        
        # Get placeholder keyframes
        keyframe_to_remove = self.get_keyframes_to_remove()
        # Get Keyframes to close to each other
        to_clean = self.get_inbetween_to_remove(obj)
        # Redundancy
        redundant = self.get_redundant_to_remove(obj, to_clean)


        keyframe_to_remove += to_clean + redundant

        # Simply delete undesired keyframes
        for i in keyframe_to_remove:
            for s in self._key_blocks:
                s: BpyShapeKey 
                s.keyframe_delete("value", frame=i)

        self.active_keyframes = []

    def get_inbetween_to_remove(self, obj: BpyObject) -> list[int]:
        to_clean = []
        total = len(self.active_keyframes)
        props = obj.lipsync2d_props #type: ignore

        min_threshold = self.time_conversion.time_to_frame(props.lip_sync_2d_in_between_threshold)
        
        for i, _ in enumerate(self.active_keyframes):
            if i + 1 >= total: break

            current_keyframe = self.active_keyframes[i]["keyframe"]
            next_keyframe = self.active_keyframes[i + 1]["keyframe"]

            if ((current_keyframe not in to_clean)
                    and (current_keyframe + min_threshold == next_keyframe)):
                to_clean.append(next_keyframe)
            
        return to_clean
    
    def get_redundant_to_remove(self, obj: BpyObject, tmp: list[int]) -> list[int]:
        to_clean = []
        n = [k for k in self.active_keyframes if k["keyframe"] not in tmp]
        total = len(n)
        props = obj.lipsync2d_props #type: ignore
        
        for i, _ in enumerate(n):
            if i + 1 >= total: break

            current_keyframe = n[i]
            next_keyframe = n[i + 1]

            if (current_keyframe["viseme"] != "sil"
                and (getattr(props, f'lip_sync_2d_viseme_shape_keys_{current_keyframe["viseme"]}') == getattr(props, f'lip_sync_2d_viseme_shape_keys_{next_keyframe["viseme"]}'))):
                to_clean.append(next_keyframe["keyframe"])

        return list(set(to_clean))

    def get_keyframes_to_remove(self) -> list[int]:
        fps_range = self.get_fps_range()
        all_frames = list(range(1, fps_range + 1))
        only_active_frame = [f["keyframe"] for f in self.active_keyframes]
        keyframe_to_remove = list(set(all_frames) - set(only_active_frame))

        return keyframe_to_remove

    def poll(self, cls, context: BpyContext):
        obj = context.active_object

        if obj is None or not isinstance(obj.data, bpy.types.Mesh):
            return False
        
        if obj.data.shape_keys is None:
            return False
        
        package_name = get_package_name()
        prefs = context.preferences.addons[package_name].preferences  # type: ignore
        return (context.scene is not None or context.active_object is not None) and prefs.is_downloading is False
    
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
