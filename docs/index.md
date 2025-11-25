# Amharic Text Processor – Documentation

This repo provides modular processors for cleaning and normalizing Amharic (and generic) text. Every processor implements `.apply(data)` and can be chained with `Pipeline`.

## Getting Started

```bash
pip install amharic-text-processor
```

```python
from amharic_text_processor import Pipeline
from amharic_text_processor.processors import HtmlStripper, UnicodeNormalizer, CharacterRemapper

pipeline = Pipeline([HtmlStripper(), UnicodeNormalizer(), CharacterRemapper()])
result = pipeline.apply("<p>ሰላም</p>")
print(result["text"])  # ሰላም
```

## API References

- [Pipeline](../amharic_text_processor/pipeline.py)
- [BaseProcessor contract](../amharic_text_processor/base.py)
- [Built-in processors overview](processors.md)

## Generate HTML API docs locally

If you want rendered API docs, install `pdoc` (one-time):

```bash
pip install pdoc
```

Then from the repo root:

```bash
pdoc -o docs amharic_text_processor
```

This will generate HTML files under `docs/` that you can open in a browser.
