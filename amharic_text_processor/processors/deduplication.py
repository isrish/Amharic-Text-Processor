"""Sentence deduplication utilities."""

from __future__ import annotations

import re
from typing import List

from rapidfuzz import fuzz
from rapidfuzz.distance import Levenshtein

from amharic_text_processor.base import BaseProcessor, ProcessorInput, ProcessorOutput


class SentenceDeduplicator:
    """Remove identical or semantically similar sentences.

    Sentences are compared with normalized Levenshtein similarity from ``rapidfuzz``.
    A sentence is dropped when its best similarity to a previously kept sentence
    is greater than or equal to ``similarity_threshold``.
    """

    sentence_pattern = re.compile(r"[^.!?።፣፤፧፨]+(?:[.!?።፣፤፧፨]|$)")

    def __init__(self, similarity_threshold: float = 0.9) -> None:
        if not 0 <= similarity_threshold <= 1:
            raise ValueError("similarity_threshold must be within [0, 1]")
        self.similarity_threshold = similarity_threshold

    def apply(self, data: ProcessorInput) -> ProcessorOutput:
        text = BaseProcessor._extract_text(data)
        sentences = self._split_sentences(text)

        kept: List[str] = []
        removed: List[str] = []

        for sentence in sentences:
            if not kept:
                kept.append(sentence)
                continue

            best_similarity = max((self._similarity(sentence, candidate) for candidate in kept), default=0.0)
            if best_similarity >= self.similarity_threshold:
                removed.append(sentence)
            else:
                kept.append(sentence)

        deduplicated_text = " ".join(kept)
        return {
            "text": deduplicated_text,
            "sentences_kept": len(kept),
            "sentences_removed": removed,
        }

    def _split_sentences(self, text: str) -> List[str]:
        return [match.group(0).strip() for match in self.sentence_pattern.finditer(text) if match.group(0).strip()]

    @staticmethod
    def _similarity(left: str, right: str) -> float:
        """Return similarity score in [0, 1] using a robust string metric."""
        # Combine full and partial ratios to catch contained sentences.
        exact_like = Levenshtein.normalized_similarity(left, right)
        partial = fuzz.partial_ratio(left, right) / 100
        return max(exact_like, partial)
