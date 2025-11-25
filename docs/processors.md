# Built-in Processors

Below is a quick reference with links to the source. All processors accept `str` or `{"text": str}` and return a dict with at least `"text"` plus extras.

- [`HtmlStripper`](../amharic_text_processor/processors/html.py): remove HTML tags and script/style content.
- [`WhitespaceNormalizer`](../amharic_text_processor/processors/whitespace.py): collapse repeated whitespace and trim.
- [`PunctuationNormalizer`](../amharic_text_processor/processors/normalize.py): unify Ethiopic/ASCII punctuation, collapse repeats, preserve decimals.
- [`UnicodeNormalizer`](../amharic_text_processor/processors/normalize.py): normalize Unicode (default NFC) and strip control chars.
- [`AmharicCharacterFilter`](../amharic_text_processor/processors/filters.py): keep Ethiopic characters plus safe punctuation/digits.
- [`CharacterRemapper`](../amharic_text_processor/processors/normalize.py): normalize variant Ethiopic glyphs to canonical forms.
- [`DottedAbbreviationNormalizer`](../amharic_text_processor/processors/abbreviations.py): convert dotted abbreviations (e.g., እ.ኤ.አ) into slash form before expansion.
- [`AbbreviationExpander`](../amharic_text_processor/processors/abbreviations.py): expand slash/dot Amharic abbreviations to full forms (e.g., ዓ.ም. -> ዓመተ ምሕረት).
- [`CommonNoiseRemover`](../amharic_text_processor/processors/filters.py): remove noisy tokens like `IMG_1124` or non-Ethiopic bracketed text `(FlyDubai)`.
- [`RegexFilter`](../amharic_text_processor/processors/filters.py): configurable regex substitution with counts.
- [`NumberToGeez`](../amharic_text_processor/processors/numbers.py): convert Arabic digits in text to Ethiopic (Geez) numerals.
- [`GeezToNumber`](../amharic_text_processor/processors/numbers.py): convert Ethiopic (Geez) numerals back to Arabic digits.
- [`WordNumberToDigits`](../amharic_text_processor/processors/numbers.py): convert Amharic worded numbers to Arabic digits (supports millions+).
- [`DigitsToWordNumber`](../amharic_text_processor/processors/numbers.py): turn Arabic digit sequences into Amharic worded numbers (up to trillions).
- [`EthiopicNumberSpacer`](../amharic_text_processor/processors/tokenize.py): insert spaces between Ethiopic letters and adjacent digits.
- [`SentenceLineFormatter`](../amharic_text_processor/processors/tokenize.py): place each sentence on its own line after end punctuation.
- [`SentenceDeduplicator`](../amharic_text_processor/processors/deduplication.py): drop exact or near-duplicate sentences with RapidFuzz similarity.
- [`OldPhoneMapper`](../amharic_text_processor/processors/phonetic.py): convert legacy phone representations to modern forms via a predefined mapping.
