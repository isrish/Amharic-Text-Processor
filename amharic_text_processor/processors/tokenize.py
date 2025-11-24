"""Tokenization helpers."""

from __future__ import annotations

import re

from amharic_text_processor.base import BaseProcessor, ProcessorInput, ProcessorOutput


class EthiopicNumberSpacer:
    """Insert spaces between Ethiopic letters and adjacent digits."""

    # Matches letter-digit or digit-letter boundaries to inject a space.
    pattern = re.compile(r"([\u1200-\u137F])(\d)|(\d)([\u1200-\u137F])")

    def apply(self, data: ProcessorInput) -> ProcessorOutput:
        text = BaseProcessor._extract_text(data)

        def replacer(match: re.Match[str]) -> str:
            if match.group(1) and match.group(2):
                return f"{match.group(1)} {match.group(2)}"
            if match.group(3) and match.group(4):
                return f"{match.group(3)} {match.group(4)}"
            return match.group(0)

        spaced = self.pattern.sub(replacer, text)
        return {"text": spaced, "spaces_added_between_text_and_digits": spaced != text}
