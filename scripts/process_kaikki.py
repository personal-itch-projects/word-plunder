#!/usr/bin/env python3
"""Download kaikki.org JSONL dictionaries and produce frequency CSVs."""

import json
import re
import unicodedata
import urllib.request
from collections import Counter
from pathlib import Path

SOURCES = {
    "en": "https://kaikki.org/dictionary/English/kaikki.org-dictionary-English.jsonl",
    "ru": "https://kaikki.org/dictionary/Russian/kaikki.org-dictionary-Russian.jsonl",
}

VALID_RE = {
    "en": re.compile(r"^[a-z]+$"),
    "ru": re.compile(r"^[а-яё]+$"),
}

MIN_LEN = 3
OUT_DIR = Path(__file__).resolve().parent.parent / "assets" / "data"


def strip_accents(text: str) -> str:
    nfkd = unicodedata.normalize("NFKD", text)
    return "".join(c for c in nfkd if not unicodedata.combining(c))


def process_lang(lang: str) -> None:
    url = SOURCES[lang]
    valid = VALID_RE[lang]
    counts: Counter = Counter()
    print(f"[{lang}] Streaming {url} ...")
    with urllib.request.urlopen(url, timeout=300) as resp:
        buf = b""
        while True:
            chunk = resp.read(1024 * 1024)  # 1MB chunks
            if not chunk:
                break
            buf += chunk
            while b"\n" in buf:
                raw_line, buf = buf.split(b"\n", 1)
                line = raw_line.decode("utf-8", errors="replace").strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                except json.JSONDecodeError:
                    continue
                word = obj.get("word", "").lower()
                if lang == "ru":
                    word = strip_accents(word)
                if len(word) >= MIN_LEN and valid.match(word):
                    counts[word] += 1
        # process remaining buffer
        if buf.strip():
            line = buf.decode("utf-8", errors="replace").strip()
            try:
                obj = json.loads(line)
                word = obj.get("word", "").lower()
                if lang == "ru":
                    word = strip_accents(word)
                if len(word) >= MIN_LEN and valid.match(word):
                    counts[word] += 1
            except json.JSONDecodeError:
                pass
    out_path = OUT_DIR / f"kaikki.{lang}.csv"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("Word,FREQcount\n")
        for word, freq in counts.most_common():
            f.write(f"{word},{freq}\n")
    print(f"[{lang}] Wrote {len(counts)} words to {out_path}")


if __name__ == "__main__":
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for lang in SOURCES:
        process_lang(lang)
