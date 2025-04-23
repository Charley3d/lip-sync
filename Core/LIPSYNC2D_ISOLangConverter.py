class LIPSYNC2D_ISOLangConverter():
    # Default fallback ISO 639-3 language code
    DEFAULT_ISO6393_CODE = "en-us"

    # Mapping from Vosk (ISO 639-1) to eSpeak language codes (ISO 639-3 + custom codes)
    vosk_to_espeak_map = {
        "ar": "ar",  # Arabic
        "ar-tn": "ar",  # Arabic (Tunisian) maps to generic Arabic
        "ca": "ca",  # Catalan
        "cn": "cmn",  # Chinese maps to Mandarin (cmn)
        "cs": "cs",  # Czech
        "de": "de",  # German
        "en": "en-gb",  # English maps to US English
        "en-gb": "en-gb",  # UK English
        "en-in": "en-us",  # Indian English maps to US English
        "en-us": "en-us",  # US English
        "eo": "eo",  # Esperanto
        "es": "es",  # Spanish
        "fa": "fa",  # Farsi / Persian
        "fr": "fr-fr",  # French. In espeak it's identify with fr-fr
        "gu": "gu",  # Gujarati
        "hi": "hi",  # Hindi
        "it": "it",  # Italian
        "ja": "ja",  # Japanese
        "ko": "ko",  # Korean
        "kz": "kk",  # Kazakh (ISO 639-3: kk)
        "nl": "nl",  # Dutch
        "pl": "pl",  # Polish
        "pt": "pt",  # Portuguese
        "ru": "ru",  # Russian
        "sv": "sv",  # Swedish
        "te": "te",  # Telugu
        "tg": "fa",  # Tajik maps to Farsi / Persian
        "tr": "tr",  # Turkish
        "ua": "uk",  # Ukrainian (maps from ua to ISO code uk)
        "uz": "uz",  # Uzbek
        "vn": "vi",  # Vietnamese (maps to ISO 639-3: vi)
    }

    @staticmethod
    def convert_iso6391_to_iso6393(iso6391_code: str) -> str:
        """
        Converts an ISO 639-1 language code to its corresponding ISO 639-3
        code using a predefined mapping. If the provided code is not found,
        returns the default fallback code ("en").

        :param iso6391_code: The ISO 639-1 language code to convert.
        :return: The mapped ISO 639-3 code or the default fallback code.
        """
        return LIPSYNC2D_ISOLangConverter.vosk_to_espeak_map.get(
            iso6391_code, LIPSYNC2D_ISOLangConverter.DEFAULT_ISO6393_CODE
        )

