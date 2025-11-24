"""Core processor interfaces."""

from __future__ import annotations

from typing import Any, Dict, Protocol, Union, runtime_checkable

ProcessorInput = Union[str, Dict[str, Any]]
ProcessorOutput = Dict[str, Any]


@runtime_checkable
class BaseProcessor(Protocol):
    """Interface for all processors."""

    def apply(self, data: ProcessorInput) -> ProcessorOutput:  # pragma: no cover - interface only
        """Transform the incoming data and return a dictionary with a ``text`` key."""
        raise NotImplementedError

    @staticmethod
    def _extract_text(data: ProcessorInput) -> str:
        """Return the text value from supported inputs or raise a helpful error."""
        if isinstance(data, str):
            return data
        if isinstance(data, dict):
            text = data.get("text")
            if isinstance(text, str):
                return text
            raise ValueError("Expected key 'text' with a string value in processor input.")
        raise TypeError("Processor input must be a string or a dictionary containing 'text'.")
