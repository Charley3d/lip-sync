phoneme_to_viseme = {
    # Silence
    "": "SIL",
    "ʔ": "SIL",

    # MBP – closed lips
    "m": "MBP",
    "b": "MBP",
    "p": "MBP",

    # FV – upper teeth and lower lip
    "f": "FV",
    "v": "FV",

    # TH – tongue between teeth (not in all languages)
    "θ": "TH",
    "ð": "TH",

    # CHJSH – post-alveolar sounds
    "ʃ": "CHJSH",  # "sh"
    "ʒ": "CHJSH",  # "zh"
    "tʃ": "CHJSH", # "ch"
    "dʒ": "CHJSH", # "j"
    "ɕ": "CHJSH",  # Japanese "sh"
    "ʑ": "CHJSH",

    # L – lateral
    "l": "L",
    "ɫ": "L",

    # RR – r-like sounds
    "r": "RR",     # alveolar
    "ɾ": "RR",     # flap (Spanish)
    "ʁ": "RR",     # French uvular
    "ʀ": "RR",     # uvular trill
    "ɹ": "RR",     # English "r"
    "ɻ": "RR",     # retroflex "r"

    # CDGKNRSTHYZ – default consonant group
    "k": "CDGKNRSTHYZ",
    "g": "CDGKNRSTHYZ",
    "ŋ": "CDGKNRSTHYZ",
    "n": "CDGKNRSTHYZ",
    "ɲ": "CDGKNRSTHYZ",  # French "gn"
    "ɳ": "CDGKNRSTHYZ",  # retroflex nasal
    "t": "CDGKNRSTHYZ",
    "d": "CDGKNRSTHYZ",
    "s": "CDGKNRSTHYZ",
    "z": "CDGKNRSTHYZ",
    "ʈ": "CDGKNRSTHYZ",
    "ɖ": "CDGKNRSTHYZ",
    "c": "CDGKNRSTHYZ",
    "ɟ": "CDGKNRSTHYZ",
    "x": "CDGKNRSTHYZ",
    "ɣ": "CDGKNRSTHYZ",
    "h": "CDGKNRSTHYZ",
    "ɦ": "CDGKNRSTHYZ",
    "j": "CDGKNRSTHYZ",  # English "y"
    "ç": "CDGKNRSTHYZ",
    "ʝ": "CDGKNRSTHYZ",

    # AI – open front or low vowels
    "a": "AI",
    "aː": "AI",
    "ä": "AI",
    "æ": "AI",
    "ɐ": "AI",
    "ɑ": "AI",
    "ɑ̃": "AI",
    "aɪ": "AI",  # diphthong

    # E – mid front vowels
    "ɛ": "E",
    "e": "E",
    "eː": "E",
    "ɛː": "E",
    "œ": "E",
    "ø": "E",
    "ə": "E",

    # IH – high front vowels
    "i": "IH",
    "ɪ": "IH",
    "y": "IH",
    "iː": "IH",
    "ʏ": "IH",

    # OH – mid/low back rounded vowels
    "o": "OH",
    "ɔ": "OH",
    "ɔ̃": "OH",
    "ɒ": "OH",
    "oː": "OH",
    "ʌ": "OH",

    # U – high back rounded vowels
    "u": "U",
    "uː": "U",
    "ɯ": "U",
    "ɰ": "U",
    "ʊ": "U",
    "w": "U",    # semivowel

    # Unknown or uncategorized
    "UNK": "UNK",
}

phoneme_to_viseme_arkit = {
    # Silence
    "": "SIL",
    "ʔ": "SIL",

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
    "tʃ": "CH",  # "ch"
    "dʒ": "CH",  # "j"

    # SS – narrow gap fricatives
    "s": "SS",
    "z": "SS",

    # SH – retracted/rounded fricatives
    "ʃ": "SH",   # "sh"
    "ʒ": "SH",   # "zh"
    "ɕ": "SH",   # Japanese "sh"
    "ʑ": "SH",

    # LL – lateral
    "l": "LL",
    "ɫ": "LL",

    # RR – r-like sounds
    "r": "RR",
    "ɾ": "RR",
    "ʁ": "RR",
    "ʀ": "RR",
    "ɹ": "RR",
    "ɻ": "RR",

    # DD – tongue behind teeth and other default consonants
    "t": "DD",
    "d": "DD",
    "n": "DD",
    "k": "DD",
    "g": "DD",
    "ŋ": "DD",
    "ɲ": "DD",
    "ɳ": "DD",
    "ʈ": "DD",
    "ɖ": "DD",
    "c": "DD",
    "ɟ": "DD",
    "x": "DD",
    "ɣ": "DD",
    "h": "DD",
    "ɦ": "DD",
    "j": "DD",   # "y" in "yes"
    "ç": "DD",
    "ʝ": "DD",

    # AA – open and mid front vowels
    "a": "AA",
    "aː": "AA",
    "ä": "AA",
    "æ": "AA",
    "ɐ": "AA",
    "ɑ": "AA",
    "ɑ̃": "AA",
    "aɪ": "AA",  # diphthong
    "ɛ": "AA",
    "e": "AA",
    "eː": "AA",
    "ɛː": "AA",
    "œ": "AA",
    "ø": "AA",
    "ə": "AA",

    # OO – rounded vowels (i, o, u group)
    "i": "OO",
    "ɪ": "OO",
    "y": "OO",
    "iː": "OO",
    "ʏ": "OO",
    "o": "OO",
    "ɔ": "OO",
    "ɔ̃": "OO",
    "ɒ": "OO",
    "oː": "OO",
    "ʌ": "OO",
    "u": "OO",
    "uː": "OO",
    "ɯ": "OO",
    "ɰ": "OO",
    "ʊ": "OO",
    "w": "OO",  # semivowel

    # Unknown
    "UNK": "SIL",
}



def viseme_items(self, context):
    return [
        ('SIL', "SIL", "Silence / Rest"),
        ('MBP', "MBP", "M, B, P (closed lips)"),
        ('FV', "FV", "F, V (teeth on lip)"),
        ('TH', "TH", "Th (tongue between teeth)"),
        ('CHJSH', "CHJSH", "Ch, J, Sh, Zh (pursed lips)"),
        ('L', "L", "L (tongue touches upper teeth)"),
        ('RR', "RR", "R (various r-like sounds)"),
        ('CDGKNRSTHYZ', "CDGKNRSTHYZ", "Neutral consonants (tongue sounds)"),
        ('AI', "AI", "A, I (open front vowels)"),
        ('E', "E", "E (mid front vowels)"),
        ('IH', "IH", "I, Y (high front vowels)"),
        ('OH', "OH", "O (rounded mid/low back vowels)"),
        ('U', "U", "U, W (rounded high back vowels)"),
        ('UNK', "UNK", "Unknown or unclassified phoneme")
    ]

def viseme_items_arkit(self, context):
    return [
        ('SIL', "SIL", "Silence / Rest"),
        ('PP', "PP", "P, B, M (closed lips)"),
        ('FF', "FF", "F, V (teeth on lip)"),
        ('TH', "TH", "TH, DH (tongue between teeth)"),
        ('DD', "DD", "T, D, N (tongue behind teeth)"),
        ('KK', "KK", "K, G, NG (back of mouth)"),
        ('CH', "CH", "CH, J (affricates)"),
        ('SS', "SS", "S, Z (narrow tongue/teeth gap)"),
        ('SH', "SH", "SH, ZH (rounded and retracted)"),
        ('RR', "RR", "R (tongue curled back)"),
        ('LL', "LL", "L (tongue touches roof of mouth)"),
        ('AA', "AA", "A, E (open and mid front vowels)"),
        ('OO', "OO", "I, O, U (rounded vowels)"),
    ]