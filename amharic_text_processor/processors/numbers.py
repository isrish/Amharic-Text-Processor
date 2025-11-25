"""Numeric processors."""

from __future__ import annotations

import re
from typing import Dict, List, Tuple

from amharic_text_processor.base import BaseProcessor, ProcessorInput, ProcessorOutput


class NumberToGeez:
    """Transform Arabic digits into their Ethiopic (Geez) numeral representation."""

    DIGIT_MAP: Dict[int, str] = {
        1: "፩",
        2: "፪",
        3: "፫",
        4: "፬",
        5: "፭",
        6: "፮",
        7: "፯",
        8: "፰",
        9: "፱",
    }

    TENS_MAP: Dict[int, str] = {
        1: "፲",
        2: "፳",
        3: "፴",
        4: "፵",
        5: "፶",
        6: "፷",
        7: "፸",
        8: "፹",
        9: "፺",
    }

    MARKERS = ["", "፻", "፼", "፼፻", "፼፼"]

    # Match integers, allowing comma as a thousands separator (requires at least one comma when present).
    number_pattern = re.compile(r"-?\d{1,3}(?:,\d{3})+|-?\d+")

    def apply(self, data: ProcessorInput) -> ProcessorOutput:
        text = BaseProcessor._extract_text(data)
        replaced = self.number_pattern.sub(self._replace_match, text)
        return {"text": replaced, "numbers_converted": text != replaced}

    def _replace_match(self, match: re.Match[str]) -> str:
        raw = match.group(0).replace(",", "")
        if raw.startswith("-"):
            return "-" + self._to_geez(int(raw[1:]))
        return self._to_geez(int(raw))

    def _to_geez(self, number: int) -> str:
        if number == 0:
            return "0"
        parts = self._split_into_pairs(abs(number))
        segments: List[str] = []
        for idx in range(len(parts) - 1, -1, -1):
            pair = parts[idx]
            if pair == 0:
                continue
            segment = self._convert_sub_100(pair)
            marker = self._marker_for_index(idx)
            segments.append(segment + marker)
        return "".join(segments)

    def _split_into_pairs(self, n: int) -> List[int]:
        pairs: List[int] = []
        while n > 0:
            pairs.append(n % 100)
            n //= 100
        return pairs or [0]

    def _convert_sub_100(self, n: int) -> str:
        tens, ones = divmod(n, 10)
        out = ""
        if tens:
            out += self.TENS_MAP[tens]
        if ones:
            out += self.DIGIT_MAP[ones]
        return out

    def _marker_for_index(self, idx: int) -> str:
        if idx < len(self.MARKERS):
            return self.MARKERS[idx]
        # Fallback for very large numbers: repeat ፼ for every two extra groups and append ፻ for odd idx.
        extra = idx - (len(self.MARKERS) - 1)
        blocks = "፼" * (extra // 2 + 1)
        return blocks + ("፻" if idx % 2 else "")


class GeezToNumber:
    """Transform Ethiopic (Geez) numerals into Arabic digits."""

    DIGIT_MAP: Dict[str, int] = {
        "፩": 1,
        "፪": 2,
        "፫": 3,
        "፬": 4,
        "፭": 5,
        "፮": 6,
        "፯": 7,
        "፰": 8,
        "፱": 9,
    }

    TENS_MAP: Dict[str, int] = {
        "፲": 10,
        "፳": 20,
        "፴": 30,
        "፵": 40,
        "፶": 50,
        "፷": 60,
        "፸": 70,
        "፹": 80,
        "፺": 90,
    }

    MARKERS = {"፻": 100, "፼": 10000}

    geez_pattern = re.compile(r"-?[፩፪፫፬፭፮፯፰፱፲፳፴፵፶፷፸፹፺፻፼]+")

    def apply(self, data: ProcessorInput) -> ProcessorOutput:
        text = BaseProcessor._extract_text(data)
        replaced = self.geez_pattern.sub(self._replace_match, text)
        return {"text": replaced, "numbers_converted": text != replaced}

    def _replace_match(self, match: re.Match[str]) -> str:
        raw = match.group(0)
        negative = raw.startswith("-")
        numeral = raw[1:] if negative else raw
        value = self._from_geez(numeral)
        return f"-{value}" if negative else str(value)

    def _from_geez(self, geez: str) -> int:
        total = 0
        current = 0
        last_marker_value = 1

        for ch in geez:
            if ch in self.DIGIT_MAP:
                current += self.DIGIT_MAP[ch]
            elif ch in self.TENS_MAP:
                current += self.TENS_MAP[ch]
            elif ch == "፻":
                current = max(current, 1) * self.MARKERS["፻"]
            elif ch == "፼":
                current = max(current, 1) * self.MARKERS["፼"]
                total += current
                last_marker_value = self.MARKERS["፼"]
                current = 0
            else:
                # Should never happen due to regex
                continue

        total += current
        return total


class WordNumberToDigits:
    """Transform Amharic worded numbers into Arabic digits."""

    UNITS: Dict[str, int] = {
        "ዜሮ": 0,
        "አንድ": 1,
        "ሁለት": 2,
        "ሶስት": 3,
        "አራት": 4,
        "አምስት": 5,
        "ስድስት": 6,
        "ሰባት": 7,
        "ስምንት": 8,
        "ዘጠኝ": 9,
    }

    TENS: Dict[str, int] = {
        "አስር": 10,
        "አስራ": 10,
        "ሃያ": 20,
        "ሰላሳ": 30,
        "አርባ": 40,
        "አምሳ": 50,
        "ስልሳ": 60,
        "ሰባ": 70,
        "ሰባስድስ": 70,  # alternate rare spelling
        "ሰማንያ": 80,
        "ዘጠና": 90,
    }

    HUNDRED = {"መቶ"}
    SCALES: Dict[str, int] = {
        "ሺህ": 1_000,
        "ሚሊዮን": 1_000_000,
        "ቢሊዮን": 1_000_000_000,
        "ትሪሊዮን": 1_000_000_000_000,
        "ኳድሪሊየን": 1_000_000_000_000_000, # rare in the vocabulary
    }

    WORD_PATTERN = re.compile(r"[^\s]+")

    def apply(self, data: ProcessorInput) -> ProcessorOutput:
        text = BaseProcessor._extract_text(data)
        converted = self._replace_in_text(text)
        return {"text": converted, "numbers_converted": converted != text}

    def _replace_in_text(self, text: str) -> str:
        parts = re.split(r"(\s+)", text)
        out: List[str] = []
        idx = 0

        while idx < len(parts):
            token = parts[idx]
            if idx % 2 == 1:  # separator
                out.append(token)
                idx += 1
                continue

            prefix, core, suffix = self._split_token(token)
            if core and self._is_number_word(core):
                words, consumed_seps = [core], []
                end_idx = idx

                # Extend sequence across whitespace-separated tokens while all are number words
                j = idx + 1
                while j + 1 < len(parts):
                    sep, nxt = parts[j], parts[j + 1]
                    if j % 2 == 1 and sep.strip() == "":
                        n_prefix, n_core, n_suffix = self._split_token(nxt)
                        if n_core and self._is_number_word(n_core):
                            consumed_seps.append(sep)
                            words.append(n_core)
                            end_idx = j + 1
                            suffix = n_suffix  # trailing punctuation from last word
                            j += 2
                            continue
                    break

                number_value = self._words_to_number(words)
                if number_value is not None:
                    out.append(f"{prefix}{number_value}{suffix}")
                    idx = end_idx + 1
                    continue

            # default path
            out.append(token)
            idx += 1

        return "".join(out)

    def _split_token(self, token: str) -> Tuple[str, str, str]:
        match = re.match(r"([^\u1200-\u137F]*)([\u1200-\u137F]+)([^\u1200-\u137F]*)$", token)
        if not match:
            return "", "", ""
        return match.group(1), match.group(2), match.group(3)

    def _is_number_word(self, word: str) -> bool:
        return word in self.UNITS or word in self.TENS or word in self.HUNDRED or word in self.SCALES

    def _words_to_number(self, words: List[str]) -> int | None:
        total = 0
        current = 0
        for word in words:
            if word in self.UNITS:
                current += self.UNITS[word]
            elif word in self.TENS:
                current += self.TENS[word]
            elif word in self.HUNDRED:
                current = max(current, 1) * 100
            elif word in self.SCALES:
                scale_value = self.SCALES[word]
                current = max(current, 1)
                total += current * scale_value
                current = 0
            else:
                return None
        return total + current


class DigitsToWordNumber:
    """Transform Arabic digit sequences into Amharic worded numbers."""

    UNITS = [
        "",
        "አንድ",
        "ሁለት",
        "ሶስት",
        "አራት",
        "አምስት",
        "ስድስት",
        "ሰባት",
        "ስምንት",
        "ዘጠኝ",
    ]
    TENS = [
        "",
        "አስር",
        "ሃያ",
        "ሰላሳ",
        "አርባ",
        "አምሳ",
        "ስልሳ",
        "ሰባ",
        "ሰማንያ",
        "ዘጠና",
    ]
    HUNDRED = "መቶ"
    SCALES = ["", "ሺህ", "ሚሊዮን", "ቢሊዮን", "ትሪሊዮን"]

    number_pattern = re.compile(r"-?\d{1,3}(?:,\d{3})+(?:\.\d+)?|-?\d+(?:\.\d+)?")

    def apply(self, data: ProcessorInput) -> ProcessorOutput:
        text = BaseProcessor._extract_text(data)
        converted = self.number_pattern.sub(self._replace_match, text)
        return {"text": converted, "numbers_converted": converted != text}

    def _replace_match(self, match: re.Match[str]) -> str:
        raw = match.group(0).replace(",", "")
        negative = raw.startswith("-")
        body = raw[1:] if negative else raw

        if "." in body:
            integer_part, decimal_part = body.split(".", 1)
            integer_words = self._to_words(int(integer_part)) if integer_part else "ዜሮ"
            decimal_words = self._decimal_digits_to_words(decimal_part)
            words = f"{integer_words} ነጥብ {decimal_words}"
        else:
            words = self._to_words(int(body))

        return f"- {words}" if negative else words

    def _to_words(self, n: int) -> str:
        if n == 0:
            return "ዜሮ"
        chunks = self._split_thousands(n)
        parts: List[str] = []
        for idx in range(len(chunks) - 1, -1, -1):
            chunk = chunks[idx]
            if chunk == 0:
                continue
            chunk_words = self._chunk_to_words(chunk)
            scale = self.SCALES[idx] if idx < len(self.SCALES) else ""
            if scale:
                parts.append(f"{chunk_words} {scale}".strip())
            else:
                parts.append(chunk_words)
        return " ".join(parts)

    def _split_thousands(self, n: int) -> List[int]:
        chunks: List[int] = []
        while n > 0:
            chunks.append(n % 1000)
            n //= 1000
        return chunks or [0]

    def _chunk_to_words(self, n: int) -> str:
        words: List[str] = []
        hundreds, rem = divmod(n, 100)
        tens, ones = divmod(rem, 10)

        if hundreds:
            if hundreds == 1:
                words.append(self.HUNDRED)
            else:
                words.append(f"{self.UNITS[hundreds]} {self.HUNDRED}")

        if tens > 1:
            words.append(self.TENS[tens])
            if ones:
                words.append(self.UNITS[ones])
        elif tens == 1:
            if ones:
                words.append(f"አስራ {self.UNITS[ones]}")
            else:
                words.append("አስር")
        else:
            if ones:
                words.append(self.UNITS[ones])

        return " ".join(words)

    def _decimal_digits_to_words(self, digits: str) -> str:
        digit_words = []
        for ch in digits:
            if ch.isdigit():
                idx = int(ch)
                digit_words.append("ዜሮ" if idx == 0 else self.UNITS[idx])
        return " ".join(digit_words)
