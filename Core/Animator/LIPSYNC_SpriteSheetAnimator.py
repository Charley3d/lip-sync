import bpy
from typing import cast

from ...Preferences.LIPSYNC2D_AP_Preferences import LIPSYNC2D_AP_Preferences
from ...Core.constants import ACTION_SUFFIX_NAME, SLOT_SPRITE_SHEET_NAME
from ...Core.Timeline.LIPSYNC2D_Timeline import LIPSYNC2D_Timeline
from ...Core.types import VisemeData, WordTiming
from ...lipsync_types import BpyAction, BpyActionChannelbag, BpyActionSlot, BpyActionKeyframeStrip, BpyContext, BpyObject, BpyPropertyGroup
from .LIPSYNC2D_ShapeKeysAnimator import LIPSYNC2D_ShapeKeysAnimator
from ..Timeline.LIPSYNC2D_TimeConversion import LIPSYNC2D_TimeConversion

class LIPSYNC_SpriteSheetAnimator:
    """
    Class responsible for handling sprite sheet animation specifically for lipsync. It provides functionalities
    to manage keyframes, interpolate lipsync viseme animations, and perform animation configurations.

    This class is focused on managing the animation data for 2D lipsync sprite sheets by clearing keyframes,
    inserting viseme keyframes, setting interpolation methods, and providing setup and cleanup methods.

    :ivar lipsync2d_props: Holds properties relevant for 2D lipsync, such as the sprite sheet index and viseme
        mappings.
    :type lipsync2d_props: BpyPropertyGroup
    :ivar lip_sync_2d_sprite_sheet_index: Index of the current viseme in the sprite sheet.
    :type lip_sync_2d_sprite_sheet_index: int
    :ivar lip_sync_2d_viseme_sil: Viseme index representing silence or no sound.
    :type lip_sync_2d_viseme_sil: int
    :ivar lip_sync_2d_viseme_{v}: Dynamically managed viseme index mapping for different mouth shapes.
    :type lip_sync_2d_viseme_{v}: int
    """

    def __init__(self) -> None:
        self.inserted_keyframes: int = 0
        self._slot: BpyActionSlot | None = None
        self.silence_frame_threshold: float = -1
        self.in_between_frame_threshold: float = -1
        self.previous_start: int = -1
        self.previous_viseme: str | None = None
        self.word_end_frame = -1
        self.word_start_frame = -1
        self.delay_until_next_word = -1
        self.is_last_word = False
        self.is_first_word = False
        self.time_conversion: LIPSYNC2D_TimeConversion | None = None
        self.channelbag: BpyActionChannelbag

    def clear_previous_keyframes(self, obj: BpyObject):
        """
        Clears all previous keyframes associated with the property
        'lipsync2d_props.lip_sync_2d_sprite_sheet_index' for the given object's
        animation data.

        This function iterates over the f-curves in the object's animation action,
        if any, and removes all keyframe points for the specified data path.

        :param obj: The object whose keyframes associated with the specified property
                    should be cleared.
        :type obj: BpyObject
        :return: None
        """
        action = obj.animation_data.action if obj.animation_data else None
        if action:
            for fcurve in action.fcurves:
                if fcurve.data_path == "lipsync2d_props.lip_sync_2d_sprite_sheet_index":
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
        self.insert_silences(props, visemes_data)

        # Iterate through visemes and insert keyframes on time
        for shape_key_anim_data in self._insert_on_visemes(obj, props, visemes_data, word_timing):

            for fcurve in self.channelbag.fcurves:
                fcurve: bpy.types.FCurve
                value = shape_key_anim_data["value"]
                fcurve.keyframe_points.insert(shape_key_anim_data["frame"], value=value, options={"FAST"})
                self.inserted_keyframes += 1

    def insert_silences(self, props, visemes_data):
        add_sil_at_word_end = (self.delay_until_next_word > self.silence_frame_threshold) or self.is_last_word

        if add_sil_at_word_end:

            for fcurve in self.channelbag.fcurves:
                fcurve: bpy.types.FCurve
                # Define data-path and value

                value = props[f"lip_sync_2d_viseme_sil"]

                # Last viseme is inserted a bit before end of word. This ensures that silence uses correct timing
                corrected_word_end_frame = LIPSYNC2D_ShapeKeysAnimator.get_corrected_end_frame(self.word_start_frame,
                                                                                               visemes_data)

                # Add silence after current word
                #TODO previous_start is not updated although new keyframe is inserted. see how to update it
                frame = corrected_word_end_frame + self.in_between_frame_threshold
                fcurve.keyframe_points.insert(frame, value=value, options={"FAST"})
                self.inserted_keyframes += 1

                if self.is_last_word:
                    frame = corrected_word_end_frame + self.in_between_frame_threshold
                    fcurve.keyframe_points.insert(frame, value=value, options={"FAST"})
                    self.inserted_keyframes += 1

        if self.is_first_word:
            for fcurve in self.channelbag.fcurves:
                fcurve: bpy.types.FCurve
                value = props["lip_sync_2d_viseme_sil"]
                frame = max(LIPSYNC2D_Timeline.get_frame_start(),
                            self.word_start_frame - max(1, self.in_between_frame_threshold))
                fcurve.keyframe_points.insert(frame, value=value, options={"FAST"})

    def _insert_on_visemes(self, obj: BpyObject, props: BpyPropertyGroup, visemes_data: VisemeData,
                         word_timing: WordTiming):
        """
        Inserts keyframes for viseme animations based on viseme data and timing information for lip-syncing.
        This function computes the required frame indices for animating visemes in a sprite sheet and handles
        the insertion of "silent" visemes during pauses or at the end of a word. It takes into account the
        timing of each viseme and applies it to an object's animation data.

        :param obj: The Blender object (BpyObject) to which keyframes will be added.
        :param props: A Blender property group (BpyPropertyGroup) containing viseme animation settings,
                      including indices for each viseme.
        :param visemes_data: A dictionary containing viseme-related data such as "visemes" and
                             "visemes_len".
        :param word_timing: A dictionary containing word timing information, including "word_frame_start"
                            and "word_frame_end".
        :param delay_until_next_word: A float value representing the delay until the next word in seconds.
        :param is_last_word: A boolean indicating whether the current word is the last word in the sequence.
        :return: None
        """
        visemes = enumerate(visemes_data["visemes"])
        for viseme_index, v in visemes:
            self.is_last_viseme = (viseme_index + 1) == visemes_data["visemes_len"]
            viseme_frame_start = word_timing["word_frame_start"] + round(viseme_index * visemes_data["visemes_parts"])
            sprite_index = props[f"lip_sync_2d_viseme_{v}"]

            if (
                    # Do not insert a keyframe on a frame that already contains a keyframed shapekey
                    self.has_already_a_kframe(viseme_frame_start)
                    # Do not insert a keyframe if previous keyframe is too close
                    or self.is_prev_kframe_too_close(viseme_frame_start)
                    # Do not insert a keyframe if previous keyframed shapekey was for the same viseme
                    or self.is_redundant(props, v)
                    ):
                continue

            yield {
                "frame": viseme_frame_start,
                "viseme": v,
                "viseme_index": viseme_index,
                "value": sprite_index,
                "shape_key": getattr(props, "lip_sync_2d_sprite_sheet_index")
            }

            self.previous_start = viseme_frame_start
            self.previous_viseme = v
    
    def has_already_a_kframe(self, viseme_frame_start):
        return viseme_frame_start == self.previous_start

    def is_prev_kframe_too_close(self, viseme_frame_start):
        return self.previous_start >= 0 and (
                (viseme_frame_start - self.previous_start) <= self.in_between_frame_threshold)
    
    def is_redundant(self, props: BpyPropertyGroup, v: str):
        if self.previous_viseme is None or self.previous_viseme == "sil":
            return False
        
    def set_interpolation(self, obj: BpyObject):
        """
        Sets the interpolation mode of keyframes in the animation action of a given object
        to 'CONSTANT'. This operation affects all keyframe points of all f-curves within the
        action, modifying their interpolation behavior.

        :param obj: The object whose animation action keyframe interpolation will be
                    modified. It must have animation data with an action to apply changes.
        :type obj: BpyObject
        :return: None
        """
        action = obj.animation_data.action if obj.animation_data else None

        if action:
            for fcurve in action.fcurves:
                for keyframe in fcurve.keyframe_points:
                    keyframe.interpolation = 'CONSTANT'

    def setup(self, obj: BpyObject):
        self.setup_animation_properties(obj)
        self.setup_properties(obj)

    def setup_properties(self, obj: BpyObject):
        props = obj.lipsync2d_props  # type: ignore

        if bpy.context.scene is not None:
            self.time_conversion = LIPSYNC2D_TimeConversion(bpy.context.scene.render)

        if self.time_conversion is None:
            return

        self.silence_frame_threshold = self.time_conversion.time_to_frame(props.lip_sync_2d_sps_sil_threshold)
        self.in_between_frame_threshold =  max(1,self.time_conversion.time_to_frame(props.lip_sync_2d_sps_in_between_threshold))
        self.previous_start = -1
        self.previous_viseme = None
        self.inserted_keyframes = 0

    def setup_animation_properties(self, obj: BpyObject):
        _, strip = self.set_up_action(obj)

        if strip is None:
            return

        self.setup_fcurves(obj, strip)


    def setup_fcurves(self, obj: BpyObject, strip: BpyActionKeyframeStrip):
        if not isinstance(obj.data, bpy.types.Mesh):
            return

        props = obj.lipsync2d_props  # type: ignore
        self.channelbag = strip.channelbag(self._slot, ensure=True)

        data_path = 'lipsync2d_props.lip_sync_2d_sprite_sheet_index'
        fcurves = self.channelbag.fcurves

        if props.lip_sync_2d_use_clear_keyframes:
            fcurves.clear()
        
        if fcurves.find(data_path) is None:
            fcurves.new(data_path)


    def set_up_action(self, obj: BpyObject) -> tuple[BpyAction, BpyActionKeyframeStrip] | tuple[None, None]:
        if not isinstance(obj.data, bpy.types.Mesh):
            return (None, None)

        
        if obj.animation_data is None:
            obj.animation_data_create()

        if not isinstance(obj.animation_data, bpy.types.AnimData):
            return (None, None)

        obj_name = obj.name
        action = bpy.data.actions.get(f"{obj_name}-{ACTION_SUFFIX_NAME}")
        if action is None:
            action = bpy.data.actions.new(f"{obj_name}-{ACTION_SUFFIX_NAME}")
            layer = action.layers.new("Layer")
            strip = cast(bpy.types.ActionKeyframeStrip, layer.strips.new(type='KEYFRAME'))
            obj.animation_data.action = action
        else:
            layer = action.layers[0]
            strip = cast(bpy.types.ActionKeyframeStrip, layer.strips[0])

        self._slot = action.slots.get(f"OB{SLOT_SPRITE_SHEET_NAME}") or action.slots.new(id_type='OBJECT', name=SLOT_SPRITE_SHEET_NAME)

        obj.animation_data.action = action
        obj.animation_data.action_slot = self._slot

        return action, strip

    def cleanup(self, obj: BpyObject):
        pass

    def poll(self, cls, context: BpyContext):
        model_state = LIPSYNC2D_AP_Preferences.get_model_state()

        return (context.scene is not None or context.active_object is not None) and model_state != "DOWNLOADING"
