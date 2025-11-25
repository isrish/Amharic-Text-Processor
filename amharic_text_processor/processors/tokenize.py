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


class SentenceLineFormatter(BaseProcessor):
    """Insert a newline after each sentence-ending punctuation mark."""

    _sentence_end = re.compile(r"\s*([!?።፧፨])\s*") # Matches sentence-ending punctuation with surrounding whitespace.

    def apply(self, data: ProcessorInput) -> ProcessorOutput:
        text = BaseProcessor._extract_text(data)
        # Insert newlines after sentence-ending punctuation and normalize whitespace.
        formatted = self._sentence_end.sub(r"\1\n", text)
        formatted = re.sub(r"[ \t]+\n", "\n", formatted)  # trim trailing spaces before newline
        formatted = re.sub(r"\n{2,}", "\n", formatted)  # collapse duplicate newlines
        formatted = formatted.strip()
        if not formatted.endswith("\n"):
            formatted = f"{formatted}\n"
        return {"text": formatted, "sentences_formatted": formatted != text}
