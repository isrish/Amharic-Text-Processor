"""Expand Amharic abbreviations to their full forms."""

from __future__ import annotations

import csv
import re
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

from amharic_text_processor.base import BaseProcessor, ProcessorInput, ProcessorOutput


class AbbreviationExpander:
    """Replace abbreviations (characters separated by slashes) with their full forms."""

    def __init__(self, abbreviations_path: Path | None = None) -> None:
        default_path = Path(__file__).resolve().parents[1] / "assets" / "AmharicAbbreviations.txt"
        self.abbreviations_path = abbreviations_path or default_path
        self._mapping = self._load_abbreviations(self.abbreviations_path)
        # Hard-coded unique abbreviations not covered by the CSV. 
        # TODO: add to CSV later.
        self._mapping.update({"ዓ.ም.": "ዓመተ ምሕረት"})
        self._patterns: List[Tuple[re.Pattern[str], str]] = self._build_patterns(self._mapping)
        self._raw_abbr_pattern = re.compile(r"[^\s/]+(?:/+[^\s/]+)+")

    @staticmethod
    def _load_abbreviations(path: Path) -> Dict[str, str]:
        if not path.exists():
            raise FileNotFoundError(f"Abbreviations file not found: {path}")

        mapping: Dict[str, str] = {}
        with path.open(encoding="utf-8", newline="") as handle:
            reader = csv.reader(handle)
            next(reader, None)  # skip header
            for row in reader:
                if len(row) < 2:
                    continue
                abbreviation, meaning = row[0].strip(), row[1].strip()
                if abbreviation and meaning:
                    mapping[abbreviation] = meaning
        return mapping

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
            normalized = re.sub(r"/+", "/", raw.strip("/"))
            if normalized and normalized not in self._mapping:
                unknown.add(normalized)
        return list(unknown)
