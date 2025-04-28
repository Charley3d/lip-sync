from ...LIPSYNC2D_Utils import get_package_name
from ...Core.types import VisemeData, WordTiming
from ...lipsync_types import BpyContext, BpyObject, BpyPropertyGroup


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

    def insert_on_visemes(self, obj: BpyObject, props: BpyPropertyGroup, visemes_data: VisemeData,
                          word_timing: WordTiming,
                          delay_until_next_word, is_last_word, words, index: int):
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
            add_sil_at_word_end = ((delay_until_next_word > 2.4) and (viseme_index + 1) == visemes_data[
                "visemes_len"]) or is_last_word
            viseme_frame_start = word_timing["word_frame_start"] + round(viseme_index * visemes_data["visemes_parts"])

            viseme_index = props[f"lip_sync_2d_viseme_{v}"]

            props["lip_sync_2d_sprite_sheet_index"] = viseme_index
            obj.keyframe_insert("lipsync2d_props.lip_sync_2d_sprite_sheet_index", frame=viseme_frame_start)
            if add_sil_at_word_end:
                props["lip_sync_2d_sprite_sheet_index"] = props[f"lip_sync_2d_viseme_sil"]
                obj.keyframe_insert("lipsync2d_props.lip_sync_2d_sprite_sheet_index",
                                    frame=word_timing["word_frame_end"])

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
        pass

    def cleanup(self, obj: BpyObject):
        pass

    def poll(self, cls, context: BpyContext):
        package_name = get_package_name()
        prefs = context.preferences.addons[package_name].preferences  # type: ignore
        return (context.scene is not None or context.active_object is not None) and prefs.is_downloading is False
