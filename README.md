# Amharic Text Processor

**Amharic Text Processor** is a modular Python toolkit for cleaning, normalizing, and formatting Amharic (and general) text. Each processing step is a small class with a predictable `.apply()` method, and steps are easily chained with `Pipeline`.

**Why this exists:** Amharic text from the web, documents, and OCR often arrives with HTML noise, mixed Ethiopic variants, inconsistent punctuation, legacy abbreviations, and numerals in different forms. This toolkit provides predictable, composable processors so you can rapidly build robust pipelines for ML datasets, search indexing, or downstream NLP tasks without reinventing cleaning logic.

---

## ✨ Features

- Composable pipeline built from simple processor classes
- Consistent I/O contract: accepts `str` or `{"text": ...}`, returns a dict with `"text"`
- HTML stripping, whitespace cleanup, Amharic character filtering
- Punctuation and Unicode normalization plus configurable regex filtering
- Pure, side-effect-free processors that are easy to test and extend

---

## 📦 Installation

```bash
pip install amharic-text-processor
```

---

## 🚀 Quick Start

```python
from amharic_text_processor import Pipeline
from amharic_text_processor.processors import (
    HtmlStripper,
    WhitespaceNormalizer,
    PunctuationNormalizer,
    UnicodeNormalizer,
    CharacterRemapper,
    AbbreviationExpander,
    AmharicCharacterFilter,
)

pipeline = Pipeline([
    HtmlStripper(),             # drop HTML/script/style
    UnicodeNormalizer(),        # NFC + strip control chars
    CharacterRemapper(),        # normalize Ethiopic variants (ሠ->ሰ, ዐ->አ, ...)
    AbbreviationExpander(),     # expand slash/dot abbreviations (e.g., ዓ.ም. -> ዓመተ ምሕረት)
    PunctuationNormalizer(),    # unify punctuation and spacing
    WhitespaceNormalizer(),     # collapse repeated whitespace
    AmharicCharacterFilter(),   # keep Ethiopic chars and safe punctuation/digits
])

raw = """
<article>
  <p>  ሰላም። ልኡኣ ዓ.ም. 2016 ሀ/ማርያም በሚሊዮን ይዘት ሰጠ። </p>
  <script>alert('ignore me')</script>
</article>
"""

result = pipeline.apply(raw)
print(result["text"])
# -> ሰላም. ሏ ዓመተ ምሕረት 2016 ሀይለ ማርያም በሚሊዮን ይዘት ሰጠ.
```

---

## 🔗 Pipeline Contract

- Input: `str` or `dict` containing `"text": str`
- Output: always a `dict` with at least `"text": str`
- Processors run in order; output from one is passed to the next
- Fail-fast validation on invalid inputs or processor outputs

---

## 🧰 Built-in Processors

- `HtmlStripper`: remove HTML tags and script/style content
- `WhitespaceNormalizer`: collapse repeated whitespace and trim
- `PunctuationNormalizer`: unify Ethiopic/ASCII punctuation and spacing
- `UnicodeNormalizer`: normalize Unicode (default NFC) and strip control chars
- `AmharicCharacterFilter`: keep Ethiopic characters plus safe punctuation/digits
- `CharacterRemapper`: normalize variant Ethiopic glyphs to canonical forms
- `AbbreviationExpander`: expand slash-separated Amharic abbreviations to full forms (e.g., ፍ/ቤቱ -> ፍርድ ቤቱ, ፕ/ር -> ፕሮፌሰር)
- `NumberToGeez`: convert Arabic digits in text to Ethiopic (Geez) numerals
- `GeezToNumber`: convert Ethiopic (Geez) numerals back to Arabic digits
- `WordNumberToDigits`: convert Amharic worded numbers (e.g., “ሁለት ሺህ ሶስት መቶ”) to Arabic digits, including millions+
- `DigitsToWordNumber`: turn Arabic digit sequences into Amharic worded numbers (supports up to trillions)
- `OldPhoneMapper`: convert legacy phone representations to modern forms via a predefined mapping
- `EthiopicNumberSpacer`: insert spaces between Ethiopic letters and adjacent digits (e.g., "ዜና11" -> "ዜና 11")
- `RegexFilter`: run a configurable regex substitution with counts

---

## 🧧 Custom Processor Example

```python
from amharic_text_processor import BaseProcessor


class ExampleProcessor(BaseProcessor):
    def apply(self, data):
        text = BaseProcessor._extract_text(data)
        processed = text.replace("old", "new")
        return {"text": processed, "modified": True}
```

Add it to a pipeline just like the built-ins.

---

## 🧪 Testing

```bash
pytest -q
```

## 🤝 Contributing

See CONTRIBUTING.md for guidelines on adding processors, running tests, and coding style.

## 📦 Publishing

GitHub Actions workflows are included:
- `CI` runs tests on pushes/PRs.
- `Publish to PyPI` builds and publishes on release creation (requires `PYPI_API_TOKEN` secret).
- See CHANGELOG.md for release notes.

---

## 📜 License

MIT License.
