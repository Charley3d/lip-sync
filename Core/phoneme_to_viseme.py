phoneme_to_viseme_arkit_v2 = {
    # Silence
    "": "sil",
    "ʔ": "sil",
    "UNK": "sil",
    # PP – closed lips
    "m": "PP",
    "b": "PP",
    "p": "PP",
    # FF – upper teeth and lower lip
    "f": "FF",
    "v": "FF",
    # TH – tongue between teeth
    "θ": "TH",
    "ð": "TH",
    # CH – affricates
    "tʃ": "CH",
    "dʒ": "CH",
    # SS – narrow gap fricatives
    "s": "SS",
    "z": "SS",
    # SH → grouped visually into SS
    "ʃ": "SS",
    "ʒ": "SS",
    "ɕ": "SS",
    "ʑ": "SS",
    # RR – r-like sounds
    "r": "RR",
    "ɾ": "RR",
    "ʁ": "RR",
    "ʀ": "RR",
    "ɹ": "RR",
    "ɻ": "RR",
    "ɚ": "RR",
    "ɜ:": "RR",
    "ɜ": "RR",
    # DD – default consonants
    "t": "DD",
    "d": "DD",
    "ʈ": "DD",
    "ɖ": "DD",
    "c": "DD",
    "ɟ": "DD",
    "x": "DD",
    "ɣ": "DD",
    "h": "DD",
    "ɦ": "DD",
    "j": "DD",
    "ç": "DD",
    "ʝ": "DD",
    # kk – velar stops
    "k": "kk",
    "g": "kk",
    "ɡ": "kk",
    # nn – nasal group + "L"
    "n": "nn",
    "ŋ": "nn",
    "ɲ": "nn",
    "ɳ": "nn",
    # LL – lateral group
    "l": "LL",
    "ɫ": "LL",
    # aa – open and low/mid front vowels
    "a": "aa",
    "aː": "aa",
    "ɑː": "aa",
    "ä": "aa",
    "æ": "aa",
    "ɐ": "aa",
    "ɑ": "aa",
    "ɑ̃": "aa",
    "aɪ": "aa",
    "ɛ": "aa",
    "ɛː": "aa",
    # E – mid/closed front vowels
    "e": "E",
    "eː": "E",
    "œ": "E",
    "ø": "E",
    "ə": "E",
    # ih – high front
    "i": "ih",
    "ɪ": "ih",
    "y": "ih",
    "iː": "ih",
    "ʏ": "ih",
    # oh – mid back / open-mid
    "o": "oh",
    "ɔ": "oh",
    "ɔ̃": "oh",
    "ɒ": "oh",
    "oː": "oh",
    "ʌ": "oh",
    # ou – high back rounded
    "u": "ou",
    "uː": "ou",
    "ɯ": "ou",
    "ɰ": "ou",
    "ʊ": "ou",
    "w": "ou",
}

visemes_priority = {"sil": 0, "pp": 1, "th": 2}
UNSKIPPABLE_VISEMES = ["sil", "pp", "th", "ff"]


def get_viseme_priority(viseme: str) -> int:
    """Get viseme priority. Lower number = higher priority."""
    if not viseme:
        return 999  # Lowest priority for invalid visemes

    try:
        return getattr(visemes_priority, viseme.lower(), 999)
    except (AttributeError, TypeError):
        return 999  # Default to lowest priority on any error


def viseme_items_mpeg4_v2(self, context):
    return [
        ("sil", "sil", "Silence / Rest"),
        ("PP", "PP", "P, B, M (closed lips)"),
        ("FF", "FF", "F, V (teeth on lip)"),
        ("TH", "TH", "TH, DH (tongue between teeth)"),
        ("DD", "DD", "T, D, etc. (tongue behind teeth)"),
        ("kk", "kk", "K, G (velar stops)"),
        ("CH", "CH", "CH, J (affricates)"),
        ("SS", "SS", "S, Z, SH, ZH (narrow fricatives)"),
        ("nn", "nn", "N, NG (nasals)"),
        ("LL", "LL", "L (lateral)"),
        ("RR", "RR", "R (r-like sounds)"),
        ("aa", "aa", "A, Æ (open/low vowels)"),
        ("E", "E", "E, Ø, Ə (mid front vowels)"),
        ("ih", "ih", "I, Y (high front vowels)"),
        ("oh", "oh", "O, ɔ, ʌ (mid back vowels)"),
        ("ou", "ou", "U, W (high back vowels)"),
        ("UNK", "unk", "Unknown phoneme"),
    ]


def phonemes_to_default_sprite_index():
    phoneme_map = {
        "sil": 0,
        "PP": 4,
        "FF": 7,
        "TH": 1,
        "DD": 9,
        "kk": 9,
        "CH": 10,
        "SS": 2,
        "nn": 10,
        "LL": 10,
        "RR": 3,
        "aa": 11,
        "E": 8,
        "ih": 6,
        "oh": 5,
        "ou": 5,
        "UNK": 0,
    }

    return phoneme_map
