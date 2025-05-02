from typing import cast

from phonemizer import phonemize

from .Timeline.LIPSYNC2D_TimeConversion import LIPSYNC2D_TimeConversion
from .types import VisemeData, WordTiming
from ..Core.LIPSYNC2D_ISOLangConverter import LIPSYNC2D_ISOLangConverter
from ..Core.phoneme_to_viseme import phoneme_to_viseme_arkit_v2 as phoneme_to_viseme
from ..Preferences.LIPSYNC2D_AP_Preferences import LIPSYNC2D_AP_Preferences
from ..lipsync_types import BpyContext, BpyRenderSettings


class LIPSYNC2D_DialogInspector:
    time_conversion: LIPSYNC2D_TimeConversion

    def __init__(self, render_settings: BpyRenderSettings):
        self.time_conversion = LIPSYNC2D_TimeConversion(render_settings)

    @staticmethod
    def extract_phonemes(words: list[str], context: BpyContext) -> list[str]:
        lang_code = LIPSYNC2D_AP_Preferences.get_current_lang_code(context)
        iso_639_3 = LIPSYNC2D_ISOLangConverter.convert_iso6391_to_iso6393(lang_code)
        phonemes = cast(list[str], phonemize(words, language=iso_639_3, backend='espeak'))
        return phonemes

    @staticmethod
    def ipaphoneme_to_viseme(ipa_phoneme: str):
        clean = ipa_phoneme.strip("ː̥̬̃012")  # remove length, nasal, stress etc
        return phoneme_to_viseme.get(clean, "UNK")

    def get_word_timing(self, recognized_word) -> WordTiming:
        word_frame_start = self.time_conversion.time_to_frame(recognized_word['start'])
        word_frame_end = self.time_conversion.time_to_frame(recognized_word['end'])
        duration = word_frame_end - word_frame_start

        return {
            "word_frame_start": word_frame_start,
            "word_frame_end": word_frame_end,
            "duration": duration,
        }

    @staticmethod
    def get_visemes(phoneme, duration: float) -> VisemeData:
        phoneme = phoneme.strip()
        visemes = [LIPSYNC2D_DialogInspector.ipaphoneme_to_viseme(p) for p in phoneme]
        visemes_no_sil = [v for v in visemes if v != "sil"]
        visemes_len = len(visemes_no_sil)
        visemes_parts = duration / len(visemes_no_sil)

        return {
            "visemes": visemes_no_sil,
            "visemes_len": visemes_len,
            "visemes_parts": visemes_parts,
        }

    def get_next_word_timing(self, recognized_words, index: int) -> WordTiming:
        result: WordTiming = {
            "word_frame_start": -1,
            "word_frame_end": -1,
            "duration": -1,
        }

        if index + 1 >= len(recognized_words):
            return result

        return self.get_word_timing(recognized_words[index + 1])
