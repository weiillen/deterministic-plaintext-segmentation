#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NTHU Cryptography — HW1
Problem: Given an uppercase A–Z string (no spaces/symbols), segment into a
meaningful English sentence. Output ALL-CAPS words separated by single spaces;
output "NONSENSE" if no valid segmentation exists.

Approach (simple & rigorous, no AI):
- Dynamic Programming (word-break) with backpointers.
- Dictionary-first: fast O(n * W) where W is #candidate word-ends from each i.
- Tie-breaks (kept tiny & deterministic):
  1) Prefer more (shorter) words when costs tie (ME AT > MEAT).
  2) Prefer common/function words slightly via a small handcrafted cost.
- No punctuation; single-letter words allowed only for A and I (standard English).

Dictionary source:
- If a local "words.txt" is present (one word per line), it will be used.
- Otherwise, fall back to a compact built-in list of common words & verbs.
  (This keeps the program runnable without extra files.)

I/O:
- Read one line from stdin (A–Z only).
- Print the reconstructed sentence in ALL CAPS or "Nonsense".

This program is intentionally straightforward to match the course’s
"ME AT over MEAT" preference and avoid over-engineering.
"""

import sys
import math
from pathlib import Path

# ---------- Minimal but useful built-in lexicon ----------
# NOTE: All words are stored UPPERCASE; only "A" and "I" allowed as single-letter words.
BUILTIN_WORDS = {
    # Function words
    "A","I","AN","AND","ARE","AS","AT","BE","BY","DO","FOR","FROM","HAS","HAVE","HE",
    "HER","HERS","HIM","HIS","IF","IN","INTO","IS","IT","ITS","ME","MY","OF","ON",
    "OR","OUR","OUT","SHE","THE","THEIR","THEM","THEN","THERE","THESE","THEY","THIS",
    "THOSE","TO","UP","US","WE","WITH","YOU","YOUR",
    # Common verbs (base/imperative or present)
    "MEET","GO","COME","SEE","TAKE","MAKE","GIVE","GET","PUT","SAY","TELL","CALL",
    "WANT","LIKE","MOVE","PARK","WALK","RUN","EAT","DRINK","PLAY","OPEN","CLOSE",
    "READ","WRITE","WATCH","HELP","TURN","SEND","KEEP","FIND","WORK",
    # Nouns / places
    "PARK","HOME","SCHOOL","OFFICE","STATION","STORE","ROOM","LAB","CLASS","ROAD",
    "BUS","TRAIN","AIRPORT","LIBRARY","CAFE","MEAL",
    # Time / misc
    "NOW","SOON","LATER","TODAY","TONIGHT","TOMORROW","NOON","MORNING","EVENING",
    "NIGHT","ATOP","OVER","UNDER","NEAR","AFTER","BEFORE",
}

# Small list of "very common" words to gently prefer in tie-breaks.
FUNCTION_WORDS = {
    "A","I","AN","AND","ARE","AS","AT","BE","BY","FOR","FROM","HAS","HAVE","HE",
    "HER","HIM","HIS","IF","IN","INTO","IS","IT","ME","MY","OF","ON","OR","OUR",
    "OUT","SHE","THE","THEIR","THEM","THEN","THERE","THESE","THEY","THIS","THOSE",
    "TO","UP","US","WE","WITH","YOU","YOUR",
}

def load_dictionary():
    """
    Load an uppercase word dictionary.
    Priority: local 'words.txt' (if present), else BUILTIN_WORDS.
    Only allow single-letter words 'A' and 'I'; others must be length >= 2.
    """
    path = Path("words.txt")
    words = set()
    if path.exists():
        for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
            w = line.strip().upper()
            if not w.isalpha():
                continue
            if len(w) == 1 and w not in {"A", "I"}:
                continue
            if len(w) >= 2 or w in {"A", "I"}:
                words.add(w)
    else:
        words = set(BUILTIN_WORDS)

    # Ensure A and I are present; and remove other single letters if any slipped in.
    base = set()
    for w in words:
        if len(w) == 1 and w not in {"A", "I"}:
            continue
        base.add(w)
    return base

def word_cost(w: str) -> float:
    """
    A tiny, deterministic, hand-crafted cost so that:
      - Function words (THE, AT, ME, TO, ...) are a bit cheaper.
      - Very long uncommon words are a bit more expensive.
    This is intentionally simple (no external data).
    Lower cost = preferred.
    """
    L = len(w)
    base = math.log(L + 2.0)  # gentle length penalty
    if w in FUNCTION_WORDS:
        base *= 0.6  # prefer function words in ties
    return base

def reconstruct(s: str, dict_words: set[str]) -> list[str] | None:
    """
    Dynamic programming word break with backpointers.
    dp[i] = (cost, prev_index, chosen_word)
    """
    n = len(s)
    if n == 0:
        return None

    # Precompute max word length to prune inner loop.
    max_len = max((len(w) for w in dict_words), default=0)

    # dp[0] = start (cost 0)
    dp_cost = [math.inf] * (n + 1)
    dp_prev = [-1] * (n + 1)
    dp_word = [""] * (n + 1)
    dp_cost[0] = 0.0

    # Standard DP
    for i in range(n):
        if dp_cost[i] == math.inf:
            continue
        # Try all next words up to max_len
        end_limit = min(n, i + max_len)
        # Iterate shorter words first to bias toward more words in exact ties
        for j in range(i + 1, end_limit + 1):
            w = s[i:j]
            if w not in dict_words:
                continue
            cost = dp_cost[i] + word_cost(w)
            # Strictly better cost ⇒ take it
            if cost < dp_cost[j] - 1e-12:
                dp_cost[j] = cost
                dp_prev[j] = i
                dp_word[j] = w
            # Near-tie: prefer the split with MORE WORDS (i.e., shorter steps)
            elif abs(cost - dp_cost[j]) <= 1e-12:
                # Prefer path that comes from a nearer i (more segments)
                current_span = j - i
                prev_span = j - dp_prev[j] if dp_prev[j] != -1 else current_span + 1
                if current_span < prev_span:
                    dp_prev[j] = i
                    dp_word[j] = w

    if dp_cost[n] == math.inf:
        return None

    # Reconstruct words by backtracking
    words = []
    cur = n
    while cur > 0 and dp_prev[cur] != -1:
        words.append(dp_word[cur])
        cur = dp_prev[cur]
    words.reverse()

    # Sanity check: ensure concatenation equals input
    if "".join(words) != s:
        return None
    return words

def main():
    raw = sys.stdin.readline().strip()
    if not raw or not raw.isalpha() or not raw.isupper():
        print("Nonsense")
        return

    DICT = load_dictionary()

    # Quick accept shortcut: if the raw input itself is a known word, output it.
    if raw in DICT:
        print(raw)
        return

    words = reconstruct(raw, DICT)
    if not words:
        print("Nonsense")
        return

    # Output ALL CAPS with single spaces
    print(" ".join(words))

if __name__ == "__main__":
    main()
