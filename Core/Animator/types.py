from typing import TypedDict

class VoskRecognitionWord(TypedDict):
    conf: float
    end: float
    start: float
    word: str