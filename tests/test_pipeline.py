import pytest

from amharic_text_processor import Pipeline
from amharic_text_processor.processors import (
    HtmlStripper,
    PunctuationNormalizer,
    WhitespaceNormalizer,
)


def test_pipeline_applies_processors_in_order():
    pipeline = Pipeline([HtmlStripper(), WhitespaceNormalizer(), PunctuationNormalizer()])
    result = pipeline.apply("<p>ሰላም   እንዴት ነህ።</p>")
    assert result["text"] == "ሰላም እንዴት ነህ."


def test_pipeline_accepts_dict_input():
    pipeline = Pipeline([WhitespaceNormalizer()])
    result = pipeline.apply({"text": " ሰላም  "})
    assert result["text"] == "ሰላም"


def test_pipeline_rejects_invalid_input():
    pipeline = Pipeline([])
    with pytest.raises(TypeError):
        pipeline.apply(123)  # type: ignore[arg-type]


def test_pipeline_raises_when_processor_output_invalid():
    class BadProcessor:
        def apply(self, data):  # pragma: no cover - intentionally wrong return
            return "not-a-dict"

    pipeline = Pipeline([BadProcessor()])  # type: ignore[list-item]
    with pytest.raises(TypeError):
        pipeline.apply("ሰላም")


def test_pipeline_returns_dict_when_no_processors():
    pipeline = Pipeline([])
    result = pipeline.apply("ሰላም")
    assert result == {"text": "ሰላም"}
