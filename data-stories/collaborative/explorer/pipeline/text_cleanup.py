"""Light typo / shorthand normalization for free-text survey responses.

Used by the build pipeline to derive a `text_normalized` field. The original
`text` is preserved verbatim for display; `text_normalized` is what gets
embedded for clustering / theme assignment.

Design: keep the dictionary tiny and obvious. We do NOT spell-check broadly
(student responses are theirs to own); we only fix high-confidence typos
that hurt downstream clustering.
"""

from __future__ import annotations

import re

# Whole-word substitutions (case-insensitive, preserve case where reasonable).
# Each entry maps a misspelling/shorthand to its canonical form.
WORD_FIXES: dict[str, str] = {
    # observed in this dataset
    "njce": "nice",
    "becuase": "because",
    "becouse": "because",
    "trem": "term",
    "afects": "effects",
    "affects": "effects",  # context-dependent but more often the noun in this corpus
    "tommaking": "to making",
    "andf": "and",
    "ti": "to",
    "witj": "with",
    "parets": "parents",
    "ppeople": "people",
    "thru": "through",
    "u": "you",
    "ur": "your",
    "yo": "your",
    "n": "and",
    "frm": "from",
    "tht": "that",
    "wht": "what",
    "wat": "what",
    "becarefull": "be careful",
    "ill": "I will",
    "im": "I am",
    "i'll": "I will",
    "i'm": "I am",
    "i've": "I have",
    "won't": "will not",
    "don't": "do not",
    "can't": "cannot",
    "didn't": "did not",
    "doesn't": "does not",
    "isn't": "is not",
    "aren't": "are not",
    "haven't": "have not",
    "hasn't": "has not",
    "wouldn't": "would not",
    "couldn't": "could not",
    "shouldn't": "should not",
    "they're": "they are",
    "you're": "you are",
    "we're": "we are",
    "it's": "it is",
    "that's": "that is",
    "there's": "there is",
    "what's": "what is",
    "who's": "who is",
    # short hedges → expand for the embedding model
    "idk": "I do not know",
    "dunno": "I do not know",
    "prolly": "probably",
    "gonna": "going to",
    "wanna": "want to",
    "kinda": "kind of",
    "sorta": "sort of",
    "yall": "you all",
    "y'all": "you all",
    # encourage typos & odd autocorrect
    "recilience": "resilience",
    "recieve": "receive",
    "wierd": "weird",
    "thier": "their",
    "definately": "definitely",
    "seperate": "separate",
    "lonly": "lonely",
    "vapeing": "vaping",
    "comunicate": "communicate",
    "vison": "vision",
    "forwrad": "forward",
    "outlin​ed": "outlined",
    "knew": "new",  # in context "to meet knew people" → "to meet new people"; keep risk vs benefit balanced
}

# Specific multi-word repairs (regex, case-insensitive).
PHRASE_FIXES: list[tuple[str, str]] = [
    (r"\bdo\s+t\s+be\s+mean\b",          "do not be mean"),
    (r"\bencourage\s+the\s+cheese\b",    "encourage the choice"),  # garbled autocorrect
    (r"\blong\s+trem\s+afects\b",        "long term effects"),
    (r"\bsay\s+no\s+and\s+build\s+u\s+p\s+yo\s+saying\s+no\b",
                                          "say no and build up your saying no"),
    (r"\bdo\s+thins\b",                  "do things"),
    (r"\bnot\s+have\s+vegan\s+stuff\b",  "not have any drug stuff"),  # context: substance-prevention
    (r"\bMWAH\b",                        ""),
    (r"\bbrake\s+bad\s+habits\b",        "break bad habits"),
    (r"\bproject\b\s*$",                 ""),  # trailing token noise
]

# Curly quotes / unicode normalizations
SMART_QUOTES = str.maketrans({
    "‘": "'",   # left single
    "’": "'",   # right single (most common in iOS submissions)
    "“": '"',   # left double
    "”": '"',   # right double
    "–": "-",   # en dash
    "—": "-",   # em dash
    "…": "...", # ellipsis
})


def normalize(text: str) -> str:
    """Return a normalized form of a survey response.

    - Smart quotes / dashes / ellipsis → ASCII equivalents.
    - Whole-word typo fixes from `WORD_FIXES` (preserves leading/trailing punct).
    - Phrase-level repairs from `PHRASE_FIXES`.
    - Collapse repeated whitespace.
    """
    if not text:
        return ""
    s = text.translate(SMART_QUOTES)
    # Apply phrase fixes first (some need the full multi-word context).
    for pat, repl in PHRASE_FIXES:
        s = re.sub(pat, repl, s, flags=re.IGNORECASE)
    # Whole-word substitution preserving surrounding punctuation.
    def _fix_word(m: re.Match) -> str:
        w = m.group(0)
        wl = w.lower()
        if wl in WORD_FIXES:
            return WORD_FIXES[wl]
        return w
    s = re.sub(r"[A-Za-z']+", _fix_word, s)
    # Collapse whitespace.
    s = re.sub(r"\s+", " ", s).strip()
    return s


if __name__ == "__main__":
    samples = [
        "Always always be njce",
        "if someone offers me drugs i will say no becuase they have bad long trem afects",
        "Do t be mean",
        "Encourage the cheese",
        "Idk",
        "I'll be positive",
        "i won't every do drugs like an absolute dweeb",
        "Continue to work witj the community",
    ]
    for s in samples:
        print(f"  IN : {s!r}")
        print(f"  OUT: {normalize(s)!r}")
        print()
