"""HTML stripping processor."""

from __future__ import annotations

from bs4 import BeautifulSoup

from amharic_text_processor.base import BaseProcessor, ProcessorInput, ProcessorOutput


class HtmlStripper:
    """Remove HTML tags while preserving readable text."""

    def apply(self, data: ProcessorInput) -> ProcessorOutput:
        text = BaseProcessor._extract_text(data)
        soup = BeautifulSoup(text, "html.parser")
        for tag in soup(["script", "style"]):
            tag.decompose()
        cleaned = soup.get_text(" ", strip=True)
        return {"text": cleaned, "html_removed": cleaned != text}
