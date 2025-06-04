from __future__ import annotations
from typing import TypedDict

from ..lipsync_types import BpyAction


class WordTiming(TypedDict):
    word_frame_start: int
    word_frame_end: int
    duration: int


class VisemeData(TypedDict):
    visemes: list[str]
    visemes_len: int
    visemes_parts: float


class VisemeSKeyAnimationData(TypedDict):
    frame: int
    viseme: str
    viseme_index: int
    value: float
    shape_key: str


class VisemeActionAnimationData(TypedDict):
    frame: int
    viseme: str
    action: BpyAction | None
    viseme_index: int
    action_name: str
