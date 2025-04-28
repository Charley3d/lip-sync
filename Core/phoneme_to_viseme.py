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

    # nn – nasal group + "L"
    "n": "nn",
    "ŋ": "nn",
    "ɲ": "nn",
    "ɳ": "nn",
    "l": "nn",
    "ɫ": "nn",

    # aa – open and low/mid front vowels
    "a": "aa",
    "aː": "aa",
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
    "w": "ou"
}

def viseme_items_mpeg4_v2(self, context):
    return [
        ('sil', "sil", "Silence / Rest"),
        ('PP', "PP", "P, B, M (closed lips)"),
        ('FF', "FF", "F, V (teeth on lip)"),
        ('TH', "TH", "TH, DH (tongue between teeth)"),
        ('DD', "DD", "T, D, etc. (tongue behind teeth)"),
        ('kk', "kk", "K, G (velar stops)"),
        ('CH', "CH", "CH, J (affricates)"),
        ('SS', "SS", "S, Z, SH, ZH (narrow fricatives)"),
        ('nn', "nn", "N, NG, L (nasals and laterals)"),
        ('RR', "RR", "R (r-like sounds)"),
        ('aa', "aa", "A, Æ (open/low vowels)"),
        ('E', "E", "E, Ø, Ə (mid front vowels)"),
        ('ih', "ih", "I, Y (high front vowels)"),
        ('oh', "oh", "O, ɔ, ʌ (mid back vowels)"),
        ('ou', "ou", "U, W (high back vowels)"),
        ('UNK', "unk", "Unknown phoneme"),
    ]