#!/usr/bin/env python3
"""Download and build frequency word lists for English and Russian.

English: FrequencyWords (OpenSubtitles 2018) from hermitdave/FrequencyWords on GitHub.
Russian: FrequencyWords + OpenCorpora lemma cross-reference.
"""

import argparse
import bz2
import re
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path

OUT_DIR = Path(__file__).resolve().parent.parent / "assets" / "data"
MIN_LEN = 3
CUMULATIVE_CUTOFF = 0.95  # keep top 95% of total frequency mass

EN_RE = re.compile(r"^[a-z]+$")
RU_RE = re.compile(r"^[а-яё]+$")

FREQ_EN_URL = "https://raw.githubusercontent.com/hermitdave/FrequencyWords/master/content/2018/en/en_full.txt"
ENABLE_URL = "https://raw.githubusercontent.com/dolph/dictionary/master/enable1.txt"
FREQ_RU_URL = "https://raw.githubusercontent.com/hermitdave/FrequencyWords/master/content/2018/ru/ru_full.txt"
OPENCORPORA_URL = "https://opencorpora.org/files/export/dict/opcorpora-dict.xml.bz2"


def _download(url: str) -> bytes:
    """Download a URL using curl (respects system proxy settings)."""
    result = subprocess.run(
        ["curl", "-sL", url],
        capture_output=True,
        timeout=600,
    )
    if result.returncode != 0:
        raise RuntimeError(f"curl failed for {url}: {result.stderr.decode()}")
    return result.stdout


def _parse_freq_lines(raw: str, pattern: re.Pattern, normalise=None) -> list[tuple[str, int]]:
    """Parse 'word freq' lines, filtering by regex."""
    words: list[tuple[str, int]] = []
    for line in raw.splitlines():
        parts = line.split()
        if len(parts) != 2:
            continue
        word = parts[0].lower()
        if normalise:
            word = normalise(word)
        try:
            count = int(parts[1])
        except ValueError:
            continue
        if len(word) >= MIN_LEN and pattern.match(word):
            words.append((word, count))
    return words


def _apply_cumulative_cutoff(words: list[tuple[str, int]]) -> list[tuple[str, int]]:
    """Sort by frequency desc and keep top CUMULATIVE_CUTOFF of total mass."""
    words.sort(key=lambda x: x[1], reverse=True)
    total = sum(c for _, c in words)
    cumulative = 0
    keep: list[tuple[str, int]] = []
    for word, count in words:
        keep.append((word, count))
        cumulative += count
        if cumulative / total >= CUMULATIVE_CUTOFF:
            break
    return keep


def _write_csv(words: list[tuple[str, int]], path: Path) -> None:
    with open(path, "w", encoding="utf-8") as f:
        f.write("Word,FREQcount\n")
        for word, count in words:
            f.write(f"{word},{count}\n")
    print(f"  Wrote {len(words)} words to {path}")


# --- English ---

def _load_enable_words() -> set[str]:
    """Download ENABLE word list (standard word-game dictionary)."""
    print("[en] Downloading ENABLE word list ...")
    raw = _download(ENABLE_URL).decode("utf-8")
    words = {w.strip().lower() for w in raw.splitlines() if w.strip()}
    print(f"[en] Loaded {len(words)} ENABLE dictionary words")
    return words


def build_english() -> None:
    enable = _load_enable_words()

    print("[en] Downloading FrequencyWords English list ...")
    raw = _download(FREQ_EN_URL).decode("utf-8")
    all_words = _parse_freq_lines(raw, EN_RE)
    words = [(w, c) for w, c in all_words if w in enable]
    print(f"[en] Parsed {len(all_words)} valid words, {len(words)} in ENABLE")
    keep = _apply_cumulative_cutoff(words)
    _write_csv(keep, OUT_DIR / "words.en.csv")


# --- Russian ---

def _load_opencorpora_lemmas() -> set[str]:
    print("[ru] Downloading OpenCorpora dictionary (bz2) ...")
    compressed = _download(OPENCORPORA_URL)
    print("[ru] Decompressing ...")
    xml_bytes = bz2.decompress(compressed)
    print("[ru] Parsing XML ...")
    root = ET.fromstring(xml_bytes)
    lemmas: set[str] = set()
    for lemma_el in root.iter("lemma"):
        l_el = lemma_el.find("l")
        if l_el is not None:
            word = l_el.get("t", "").lower().replace("ё", "е")
            if word:
                lemmas.add(word)
    print(f"[ru] Loaded {len(lemmas)} OpenCorpora lemmas")
    return lemmas


def build_russian(skip_opencorpora: bool = False) -> None:
    lemmas: set[str] | None = None
    if not skip_opencorpora:
        try:
            lemmas = _load_opencorpora_lemmas()
        except Exception as e:
            print(f"[ru] WARNING: OpenCorpora download failed ({e}), skipping cross-reference")

    print("[ru] Downloading FrequencyWords Russian list ...")
    raw = _download(FREQ_RU_URL).decode("utf-8")
    normalise_ru = lambda w: w.replace("ё", "е")
    all_words = _parse_freq_lines(raw, RU_RE, normalise=normalise_ru)
    if lemmas is not None:
        words = [(w, c) for w, c in all_words if w in lemmas]
        print(f"[ru] Parsed {len(all_words)} valid words, {len(words)} in OpenCorpora")
    else:
        words = all_words
        print(f"[ru] Parsed {len(words)} valid words (no OpenCorpora filter)")
    keep = _apply_cumulative_cutoff(words)
    _write_csv(keep, OUT_DIR / "words.ru.csv")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build word frequency lists")
    parser.add_argument("--lang", choices=["en", "ru", "all"], default="all")
    parser.add_argument("--skip-opencorpora", action="store_true",
                        help="Skip OpenCorpora cross-reference for Russian")
    args = parser.parse_args()

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    if args.lang in ("en", "all"):
        build_english()
    if args.lang in ("ru", "all"):
        build_russian(skip_opencorpora=args.skip_opencorpora)
