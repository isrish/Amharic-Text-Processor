"""Composable pipeline for chaining processors."""

from __future__ import annotations

from typing import Iterable, List

from .base import BaseProcessor, ProcessorInput, ProcessorOutput


class Pipeline:
    """Run text through a sequence of processors."""

    def __init__(self, processors: Iterable[BaseProcessor]):
        processors_list: List[BaseProcessor] = list(processors)
        for processor in processors_list:
            if not hasattr(processor, "apply"):
                raise TypeError("All pipeline components must implement an 'apply' method.")
        self.processors = processors_list

    def apply(self, data: ProcessorInput) -> ProcessorOutput:
        """Apply each processor in order, validating I/O at every hop."""
        self._validate_input(data)
        current: ProcessorInput | ProcessorOutput = data

        if not self.processors:
            return {"text": self._extract_text(current)} if isinstance(current, str) else current

        for processor in self.processors:
            current = processor.apply(current)
            self._validate_output(current, processor)

        return current  # type: ignore[return-value]

    @staticmethod
    def _extract_text(data: ProcessorInput) -> str:
        from .base import BaseProcessor as _Base  # local import to avoid cycle in type checkers

        return _Base._extract_text(data)

    @staticmethod
    def _validate_input(data: ProcessorInput) -> None:
        if isinstance(data, str):
            return
        if isinstance(data, dict) and isinstance(data.get("text"), str):
            return
        raise TypeError("Pipeline input must be a string or a dict containing a string 'text'.")

    @staticmethod
    def _validate_output(output: ProcessorOutput, processor: BaseProcessor) -> None:
        if not isinstance(output, dict):
            raise TypeError(
                f"{processor.__class__.__name__}.apply must return a dict containing 'text'."
            )
        if "text" not in output or not isinstance(output["text"], str):
            raise ValueError(
                f"{processor.__class__.__name__}.apply must return a dict with string 'text'."
            )
