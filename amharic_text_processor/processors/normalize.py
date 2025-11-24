"""Normalization processors."""

from __future__ import annotations

import re
import unicodedata

from amharic_text_processor.base import BaseProcessor, ProcessorInput, ProcessorOutput


class PunctuationNormalizer:
    """Unify punctuation characters and reduce repeats."""

    PUNCT_TRANSLATION = str.maketrans(
        {
            "።": ".",
            "፣": ",",
            "፤": ";",
            "፥": ":",
            "፦": ":",
            "፧": "?",
            "፨": "!",
            "“": '"',
            "”": '"',
            "‘": "'",
            "’": "'",
            "，": ",",
            "。": ".",
            "！": "!",
            "？": "?",
            "、": ",",
            "；": ";",
            "：": ":",
        }
    )

    def apply(self, data: ProcessorInput) -> ProcessorOutput:
        text = BaseProcessor._extract_text(data)
        normalized = text.translate(self.PUNCT_TRANSLATION)
        normalized = re.sub(r"([?!.,;:]){2,}", r"\1", normalized)
        normalized = re.sub(r"\s+([?!.,;:])", r" \1", normalized)
        normalized = re.sub(r"([?!.,;:])([^\s])", r"\1 \2", normalized)
        normalized = re.sub(r"\s+", " ", normalized).strip()
        return {"text": normalized, "punctuation_normalized": normalized != text}


class UnicodeNormalizer:
    """Normalize Unicode using the given form (default NFC)."""

    def __init__(self, form: str = "NFC", strip_control: bool = True) -> None:
        self.form = form
        self.strip_control = strip_control

    def apply(self, data: ProcessorInput) -> ProcessorOutput:
        text = BaseProcessor._extract_text(data)
        normalized = unicodedata.normalize(self.form, text)
        if self.strip_control:
            normalized = "".join(ch for ch in normalized if unicodedata.category(ch)[0] != "C")
        return {"text": normalized, "unicode_normalized": normalized != text}


class CharacterRemapper:
    """Remap legacy/variant Ethiopic characters to canonical forms."""

    REMAP = {
        "ሠ": "ሰ",
        "ሡ": "ሱ",
        "ሢ": "ሲ",
        "ሣ": "ሳ",
        "ሤ": "ሴ",
        "ሥ": "ስ",
        "ሦ": "ሶ",
        "ሧ": "ሷ",
        "ሐ": "ሀ",
        "ሑ": "ሁ",
        "ሒ": "ሂ",
        "ሓ": "ሀ",
        "ሔ": "ሄ",
        "ሕ": "ህ",
        "ሖ": "ሆ",
        "ሃ": "ሀ",
        "ኀ": "ሀ",
        "ኁ": "ሁ",
        "ኂ": "ሂ",
        "ኃ": "ሀ",
        "ኄ": "ሄ",
        "ኅ": "ህ",
        "ኆ": "ሆ",
        "ፀ": "ጸ",
        "ፁ": "ጹ",
        "ፂ": "ጺ",
        "ፃ": "ጻ",
        "ፄ": "ጼ",
        "ፅ": "ጽ",
        "ፆ": "ጾ",
        "ፇ": "ጿ",
        "ዐ": "አ",
        "ዑ": "ኡ",
        "ዒ": "ኢ",
        "ዓ": "አ",
        "ዔ": "ኤ",
        "ዕ": "እ",
        "ዖ": "ኦ",
        "ጎ": "ጐ",
        "ኰ": "ኮ",
    }

    def __init__(self) -> None:
        self._translation_table = str.maketrans(self.REMAP)

    def apply(self, data: ProcessorInput) -> ProcessorOutput:
        text = BaseProcessor._extract_text(data)
        remapped = text.translate(self._translation_table)
        return {"text": remapped, "characters_remapped": remapped != text}
