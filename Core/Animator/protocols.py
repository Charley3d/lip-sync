from typing import Any, Iterator, Protocol

from ...Core.types import VisemeData, VisemeSKeyAnimationData, WordTiming
from ...lipsync_types import BpyContext, BpyObject, BpyPropertyGroup


class LIPSYNC2D_LipSyncAnimator(Protocol):
    """
    Interface for handling lip-sync animation.

    This protocol defines methods for animating lip-sync via viseme-based
    keyframe generation, interpolation setup, and cleanup. Classes
    implementing this protocol are expected to provide mechanisms for setting
    up animation objects, managing keyframes, and generating smooth
    transitions between visemes.

    :ivar setup: Initializes and configures the given animation object for lip-sync.
    :type setup: Callable[[BpyObject], None]
    :ivar clear_previous_keyframes: Clears all keyframes previously set on the animation object.
    :type clear_previous_keyframes: Callable[[BpyObject], None]
    :ivar insert_on_visemes: Inserts keyframes on the animation object based on the provided
        viseme data, word timings, and additional properties.
    :type insert_on_visemes: Callable[[BpyObject, BpyPropertyGroup, VisemeData, WordTiming, int, bool], None]
    :ivar set_interpolation: Adjusts keyframe interpolation for smoother lip-sync animation.
    :type set_interpolation: Callable[[BpyObject], None]
    :ivar cleanup: Finalizes animation and removes temporary data from the object.
    :type cleanup: Callable[[BpyObject], None]
    """

    inserted_keyframes: int

    def setup(self, obj: BpyObject):
        pass

    def clear_previous_keyframes(self, obj: BpyObject):
        pass

    def insert_keyframes(
        self,
        obj: BpyObject,
        props: BpyPropertyGroup,
        visemes_data: VisemeData,
        word_timing: WordTiming,
        delay_until_next_word: int,
        is_last_word: bool,
        index: int,
    ):
        pass

    def set_interpolation(self, obj: BpyObject):
        pass

    def cleanup(self, obj: BpyObject):
        pass

    def poll(self, cls, context: BpyContext) -> bool:
        return False
