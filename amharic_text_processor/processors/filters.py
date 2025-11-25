"""Filtering processors."""

from __future__ import annotations

import re
from typing import Iterable, Set

from amharic_text_processor.base import BaseProcessor, ProcessorInput, ProcessorOutput


class AmharicCharacterFilter:
    """Keep Ethiopic characters and optionally a set of safe extras."""

    AMHARIC_BLOCK = re.compile(r"[\u1200-\u137F]")
    # print("".join(chr(cp) for cp in range(0x1200, 0x137F + 1)))

    def __init__(self, extra_allowed: Iterable[str] | None = None) -> None:
        self.extra_allowed: Set[str] = set(extra_allowed or []) | set(
            " /\\\t\n\r\f\v.,;:!?-—'\"()[]{}።፣፤፥፦፧፨፼0123456789%"
        )

    def apply(self, data: ProcessorInput) -> ProcessorOutput:
        text = BaseProcessor._extract_text(data)
        kept = []
        removed = 0
        for ch in text:
            if self.AMHARIC_BLOCK.match(ch) or ch in self.extra_allowed:
                kept.append(ch)
            else:
                removed += 1
        filtered = "".join(kept)
        return {"text": filtered, "invalid_characters_removed": removed}


class RegexFilter:
    """Apply a regex substitution."""

    def __init__(self, pattern: str, replacement: str = "", flags: int = re.MULTILINE) -> None:
        self.pattern = re.compile(pattern, flags)
        self.replacement = replacement

    def apply(self, data: ProcessorInput) -> ProcessorOutput:
        text = BaseProcessor._extract_text(data)
        cleaned, count = self.pattern.subn(self.replacement, text)
        return {"text": cleaned, "regex_substitutions": count}


class CommonNoiseRemover(BaseProcessor):
    """Remove common non-Ethiopic noise such as file-like tokens (IMG_1124) or Latin-only brackets."""

    _patterns = [
        # Tokens containing Latin letters with underscores/digits (e.g., IMG_1124, file_names_01)
        re.compile(r"\b[A-Za-z]+_[A-Za-z0-9_]*[A-Za-z0-9]\b"),
        # Parentheses containing no Ethiopic characters (e.g., (FlyDubai))
        re.compile(r"\(([^()\u1200-\u137F]*)\)"),
        # Square brackets containing no Ethiopic characters.
        re.compile(r"\[([^\[\]\u1200-\u137F]*)\]"),
        # Curly braces containing no Ethiopic characters.
        re.compile(r"\{([^{}\u1200-\u137F]*)\}"),
        # Angle brackets containing no Ethiopic characters.
        re.compile(r"<([^<>\u1200-\u137F]*)>"),
        # TODO: Add more patterns as needed
    ]

    def apply(self, data: ProcessorInput) -> ProcessorOutput:
        text = self._extract_text(data)
        cleaned = text
        removed = 0
        for pattern in self._patterns:
            cleaned, count = pattern.subn("", cleaned)
            removed += count
        cleaned = re.sub(r"\s{2,}", " ", cleaned).strip()
        return {"text": cleaned, "noise_removed": removed}
