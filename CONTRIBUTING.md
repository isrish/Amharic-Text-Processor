# Contributing

Thank you for helping improve **Amharic Text Processor**! This project aims to provide clean, predictable, and composable text processing utilities for Amharic and related scripts.

## Ground rules
- Keep processors pure and side-effect free.
- Preserve the I/O contract: `apply` accepts `str` or `{"text": str}` and returns a `dict` with at least `"text": str`.
- Validate inputs and fail fast with clear errors.
- Use Python 3.10+ type hints and PEP 8 style.
- Add or update tests for any new logic.

## Development setup
```bash
git clone <your-fork-url>
cd AmharicTextProcessor  # adjust if your folder differs
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e .[dev]  # if you add extras in the future
```

## Running tests
```bash
pytest -q
```

## Adding a processor
1. Implement a class with an `apply(self, data)` method in `amharic_text_processor/processors/`.
2. Use `BaseProcessor._extract_text` for input handling and return a dict with `"text"` plus any flags/metadata.
3. Export it in `amharic_text_processor/processors/__init__.py` and `amharic_text_processor/__init__.py`.
4. Add tests in `tests/` covering normal, edge, and error cases.
5. Update `README.md` and examples if the processor is user-facing.

## Coding style
- Type hints everywhere; prefer small, composable functions.
- Keep comments brief and purposeful; avoid noise.
- Default to ASCII unless existing files require otherwise.

## Commit hygiene
- Keep commits focused; describe what and why.
- Include tests for new functionality.

## Reporting issues / requesting features
- Use clear titles, describe the context, expected vs actual behavior, and include minimal repro snippets.

## Release checklist (maintainers)
- All tests pass.
- README and docs updated.
- Version bumped (pyproject.toml) when publishing.
