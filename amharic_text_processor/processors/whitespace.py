"""Whitespace normalization processor."""

from __future__ import annotations

import re

from amharic_text_processor.base import BaseProcessor, ProcessorInput, ProcessorOutput


class WhitespaceNormalizer:
    """Collapse repeated whitespace and trim the text."""

    def apply(self, data: ProcessorInput) -> ProcessorOutput:
        text = BaseProcessor._extract_text(data)
        cleaned = re.sub(r"\s+", " ", text).strip()
        return {"text": cleaned, "whitespace_normalized": cleaned != text}
