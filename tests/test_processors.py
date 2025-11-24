import unicodedata

import pytest

from amharic_text_processor.processors import (
    AbbreviationExpander,
    AmharicCharacterFilter,
    CharacterRemapper,
    HtmlStripper,
    GeezToNumber,
    WordNumberToDigits,
    DigitsToWordNumber,
    OldPhoneMapper,
    EthiopicNumberSpacer,
    PunctuationNormalizer,
    RegexFilter,
    UnicodeNormalizer,
    WhitespaceNormalizer,
    NumberToGeez,
)


def test_html_stripper_removes_tags_and_scripts():
    processor = HtmlStripper()
    result = processor.apply("<div>ሰላም <script>bad()</script></div>")
    assert result["text"] == "ሰላም"
    assert result["html_removed"] is True


def test_whitespace_normalizer_collapses_spaces():
    processor = WhitespaceNormalizer()
    result = processor.apply({"text": "  ሰላም \n \t ዓለም  "})
    assert result["text"] == "ሰላም ዓለም"
    assert result["whitespace_normalized"] is True


def test_amharic_character_filter_keeps_block_and_basic_punctuation():
    processor = AmharicCharacterFilter()
    result = processor.apply({"text": "ሰላም! hello 123"})
    assert result["text"] == "ሰላም!  123"
    assert result["invalid_characters_removed"] == 5  # hello


def test_punctuation_normalizer_unifies_ethiopic_marks_and_spacing():
    processor = PunctuationNormalizer()
    result = processor.apply({"text": "ሰላም።እንዴት  ነህ፣"})
    assert result["text"] == "ሰላም. እንዴት ነህ,"
    assert result["punctuation_normalized"] is True


def test_unicode_normalizer_uses_nfc_and_strips_control():
    raw = "e\u0301\n"  # decomposed e + accent plus newline
    processor = UnicodeNormalizer()
    result = processor.apply({"text": raw})
    assert unicodedata.is_normalized("NFC", result["text"])
    assert "\n" not in result["text"]
    assert result["unicode_normalized"] is True


def test_regex_filter_substitutes_and_counts():
    processor = RegexFilter(r"[0-9]+", replacement="")
    result = processor.apply({"text": "አንድ1ሁለት2ሶስት3"})
    assert result["text"] == "አንድሁለትሶስት"
    assert result["regex_substitutions"] == 3


def test_character_remapper_normalizes_variants():
    processor = CharacterRemapper()
    text = "ሠሥ ሓህ ፀፅ ዐዒ ጎኰ"
    result = processor.apply({"text": text})
    assert result["text"] == "ሰስ ሀህ ጸጽ አኢ ጐኮ"
    assert result["characters_remapped"] is True


def test_abbreviation_expander_replaces_known_values():
    processor = AbbreviationExpander()
    text = "ሀ/ማርያም በለሜ/ጄኔራል ጋር ተነጋግሯል።"
    result = processor.apply({"text": text})
    assert "ሀይለ ማርያም" in result["text"]
    assert "ለሜጀር ጄኔራል" in result["text"]
    assert result["abbreviations_expanded"] >= 2
    assert result["abbreviations_unknown"] == []


def test_abbreviation_expander_handles_multiple_slashes():
    processor = AbbreviationExpander()
    result = processor.apply({"text": "ሀ//ማርያም እዚህ ነው ገ///ሀ"})
    assert result["text"].startswith("ሀይለ ማርያም")
    assert "ገ/ሀ" in result["abbreviations_unknown"]


def test_abbreviation_expander_handles_dot_abbreviation():
    processor = AbbreviationExpander()
    result = processor.apply({"text": "ዛሬ ዓ.ም. በሚል ይጻፋል"})
    assert "ዓመተ ምሕረት" in result["text"]


def test_number_to_geez_converts_in_text():
    processor = NumberToGeez()
    result = processor.apply({"text": "ከ123 በላይ 4567 አሉ"})
    assert "፻፳፫" in result["text"]
    assert "፵፭፻፷፯" in result["text"]
    assert result["numbers_converted"] is True


def test_number_to_geez_handles_zero_and_negative():
    processor = NumberToGeez()
    result = processor.apply("0 -12")
    assert result["text"].startswith("0 -፲፪")


def test_geez_to_number_converts_back():
    processor = GeezToNumber()
    result = processor.apply({"text": "፻፳፫ ፵፭፻፷፯ -፲፪"})
    assert result["text"].startswith("123 4567 -12")
    assert result["numbers_converted"] is True


def test_word_number_to_digits_converts_simple_phrase():
    processor = WordNumberToDigits()
    result = processor.apply({"text": "አምስት መቶ ሃያ ሁለት ተማሪዎች"})
    assert result["text"].startswith("522")
    assert result["numbers_converted"] is True


def test_word_number_to_digits_handles_thousands():
    processor = WordNumberToDigits()
    result = processor.apply({"text": "ሁለት ሺህ ሶስት መቶ አምሳ አንድ"})
    assert result["text"].startswith("2351")


def test_word_number_to_digits_handles_millions_and_billions():
    processor = WordNumberToDigits()
    result = processor.apply({"text": "ሶስት ሚሊዮን አምስት መቶ ቢሊዮን ሁለት"})
    assert "500003000002" in result["text"]


def test_digits_to_word_number_converts_in_text():
    processor = DigitsToWordNumber()
    result = processor.apply({"text": "ብዙ 123 ሰዎች"})
    assert "መቶ ሃያ ሶስት" in result["text"]
    assert result["numbers_converted"] is True


def test_digits_to_word_number_handles_large():
    processor = DigitsToWordNumber()
    result = processor.apply({"text": "1000000000001"})
    assert "አንድ ትሪሊዮን አንድ" in result["text"]


def test_old_phone_mapper_replaces_sequences():
    processor = OldPhoneMapper()
    result = processor.apply({"text": "ህኡኣ ቅኡኤ ቅኡኢ"})
    assert result["text"] == "ኋ ቌ ቊ"
    assert result["old_phone_mapped"] is True


def test_ethiopic_number_spacer_inserts_spaces():
    processor = EthiopicNumberSpacer()
    result = processor.apply({"text": "ዜና11 12ዜና"})
    assert result["text"] == "ዜና 11 12 ዜና"
    assert result["spaces_added_between_text_and_digits"] is True


def test_digits_to_word_number_handles_decimal():
    processor = DigitsToWordNumber()
    result = processor.apply({"text": "ቁጥር 123.45"})
    assert "መቶ ሃያ ሶስት ነጥብ አራት አምስት" in result["text"]
