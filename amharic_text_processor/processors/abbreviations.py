"""Expand Amharic abbreviations to their full forms."""

from __future__ import annotations

import re
from typing import Dict, List, Tuple

from amharic_text_processor.assets.abbreviations import ABBREVIATIONS

from amharic_text_processor.base import BaseProcessor, ProcessorInput, ProcessorOutput


class AbbreviationExpander:
    """Replace abbreviations (characters separated by slashes) with their full forms."""

    def __init__(self, mapping: Dict[str, str] | None = None) -> None:
        self._mapping = dict(ABBREVIATIONS if mapping is None else mapping)
        self._patterns: List[Tuple[re.Pattern[str], str]] = self._build_patterns(self._mapping)
        self._raw_abbr_pattern = re.compile(r"[^\s/\.]+(?:(?:/+|\.+)[^\s/\.]+)+")

    @staticmethod
    def _build_patterns(mapping: Dict[str, str]) -> List[Tuple[re.Pattern[str], str]]:
        patterns: List[Tuple[re.Pattern[str], str]] = []
        for abbr, meaning in sorted(mapping.items(), key=lambda item: len(item[0]), reverse=True):
            if "/" in abbr:
                parts = [re.escape(part) for part in abbr.split("/")]
                abbr_pattern = r"/+".join(parts)
            else:
                abbr_pattern = re.escape(abbr)
            patterns.append((re.compile(abbr_pattern), meaning))
        return patterns

    def apply(self, data: ProcessorInput) -> ProcessorOutput:
        text = BaseProcessor._extract_text(data)
        expanded = text
        replacements = 0
        for pattern, meaning in self._patterns:
            expanded, count = pattern.subn(meaning, expanded)
            replacements += count

        unknown_abbreviations = self._collect_unknown_abbreviations(expanded)

        return {
            "text": expanded,
            "abbreviations_expanded": replacements,
            "abbreviations_unknown": sorted(unknown_abbreviations),
        }

    def _collect_unknown_abbreviations(self, text: str) -> List[str]:
        unknown: set[str] = set()
        for match in self._raw_abbr_pattern.finditer(text):
            raw = match.group(0)
            normalized = re.sub(r"[/.]+", "/", raw.strip("/."))
            if normalized and normalized not in self._mapping:
                unknown.add(normalized)
        return list(unknown)


class DottedAbbreviationNormalizer(BaseProcessor):
    """Convert dotted Amharic abbreviations (e.g., እ. ኤ. አ.) into slash format (እ/ኤ/አ).

    A valid dotted abbreviation is expected to start after a space or an opening parenthesis.
    """

    _pattern = re.compile(
        r"(?:(?<=\s)|(?<=\()|(?<=^))"  # preceded by space, ( , or start
        r"((?:[\u1200-\u137F]{1,3}\s*\.\s*)+[\u1200-\u137F]{1,3})"  # dotted segments
        r"\.?"  # optional trailing dot
        r"(?=\s|\)|$)"  # must end before space, closing paren, or end
    )

    def apply(self, data: ProcessorInput) -> ProcessorOutput:
        text = self._extract_text(data)

        def replace(match: re.Match[str]) -> str:
            abbr = match.group(1)
            parts = [part.strip() for part in re.split(r"\s*\.\s*", abbr) if part.strip()]
            replacement = "/".join(parts)
            # Do not append a slash for the trailing dot; add a space only if needed.
            next_char = text[match.end(0) : match.end(0) + 1]
            suffix = "" if not next_char or next_char.isspace() or next_char == ")" else " "
            return replacement + suffix

        converted, count = self._pattern.subn(replace, text)
        return {"text": converted, "dotted_abbreviations_normalized": count > 0}
