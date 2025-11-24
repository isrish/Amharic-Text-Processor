"""Public API for amharic-text-processor."""

from .base import BaseProcessor
from .pipeline import Pipeline
from .processors import (
    AmharicCharacterFilter,
    AbbreviationExpander,
    HtmlStripper,
    GeezToNumber,
    DigitsToWordNumber,
    NumberToGeez,
    WordNumberToDigits,
    OldPhoneMapper,
    EthiopicNumberSpacer,
    PunctuationNormalizer,
    RegexFilter,
    UnicodeNormalizer,
    WhitespaceNormalizer,
    CharacterRemapper,
)

__all__ = [
    "BaseProcessor",
    "Pipeline",
    "HtmlStripper",
    "WhitespaceNormalizer",
    "AmharicCharacterFilter",
    "PunctuationNormalizer",
    "UnicodeNormalizer",
    "RegexFilter",
    "CharacterRemapper",
    "AbbreviationExpander",
    "NumberToGeez",
    "GeezToNumber",
    "WordNumberToDigits",
    "DigitsToWordNumber",
    "OldPhoneMapper",
    "EthiopicNumberSpacer",
]
