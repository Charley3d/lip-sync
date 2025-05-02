from typing import TypedDict


class WordTiming(TypedDict):
    word_frame_start: int
    word_frame_end: int
    duration: int


class VisemeData(TypedDict):
    visemes: list[str]
    visemes_len: int
    visemes_parts: float

class VisemeSKeyAnimationData(TypedDict):
    keyframe: int
    viseme: str
    viseme_index: int
    value: float
    shape_key: str