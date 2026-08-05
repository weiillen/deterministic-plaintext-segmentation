# Deterministic Plaintext Segmentation for Cryptanalytic Workflows

A compact Python implementation that reconstructs readable English word boundaries from an uppercase letter stream with no spaces or punctuation.

The project is useful as a **post-processing step** in cryptanalysis: after a cipher procedure produces a candidate plaintext such as `MEETMEATTHEPARK`, the program tests whether it can be segmented into a plausible sequence of dictionary words. It is not itself an encryption or decryption algorithm.

## Project focus

The implementation demonstrates:

- dynamic programming for the word-break problem;
- backpointer-based reconstruction of the selected sentence;
- deterministic tie-breaking for ambiguous segmentations;
- dictionary-based validation with a built-in fallback lexicon;
- bounded search using the maximum dictionary word length; and
- reproducible behavior without machine learning or external packages.

## Example

```text
Input:  MEETMEATTHEPARK
Output: MEET ME AT THE PARK
```

The intended preference is `ME AT` rather than `MEAT` when both are valid within a longer reconstruction.

## How it works

For an input string of length `n`, the program stores the best known reconstruction cost for every prefix position.

1. Validate that the input contains uppercase alphabetic characters only.
2. Load `words.txt` from the current working directory when available; otherwise use the built-in lexicon.
3. Starting from every reachable position, test dictionary words that could end at later positions.
4. Record the lower-cost path and its backpointer.
5. Backtrack from the end of the string to reconstruct the selected sequence.
6. Print the words separated by single spaces, or print `Nonsense` when no valid path exists.

The scoring function uses `log(length + 2)` as a base word cost and applies a small preference to common function words. Near-equal paths prefer shorter individual spans, which tends to produce more word boundaries.

## Complexity

Let:

- `n` be the input length; and
- `L` be the maximum word length in the dictionary.

The implementation performs approximately **O(nL)** substring and set-membership checks and uses **O(n)** dynamic-programming storage, in addition to the dictionary.

## Repository structure

```text
.
├── src/
│   └── hw1.py                         # Featured original implementation
├── data/
│   └── words.txt                      # Small example dictionary
├── docs/
│   ├── technical-report/              # Original written explanation
│   └── cryptography-reflection/       # Supplementary historical reflection
├── development/
│   ├── referenced-version/            # Alternate documented variant
│   └── ascii-compatible-version/      # Alternate punctuation-compatible copy
├── verification/
│   └── VERIFICATION.md                # Reproduced test results
└── ORIGINAL_FILE_MANIFEST.tsv         # SHA-256 preservation record
```

## Running the featured implementation

The program uses only the Python standard library.

```bash
cd data
printf 'MEETMEATTHEPARK\n' | python3 ../src/hw1.py
```

Expected output:

```text
MEET ME AT THE PARK
```

Additional examples:

```bash
printf 'MEETMEAT\n' | python3 ../src/hw1.py
printf 'ABCD\n' | python3 ../src/hw1.py
printf 'IATTHEPARK\n' | python3 ../src/hw1.py
```

## Verified behavior

Using the included dictionary:

| Input | Observed output |
|---|---|
| `MEETMEATTHEPARK` | `MEET ME AT THE PARK` |
| `MEETMEAT` | `MEET ME AT` |
| `MEAT` | `MEAT` |
| `IATTHEPARK` | `I AT THE PARK` |
| `ABCD` | `Nonsense` |
| lowercase or empty input | `Nonsense` |

The featured file also passes Python bytecode compilation with `python3 -m py_compile`.

## Cryptography connection

A cipher solver can produce many candidate uppercase plaintext streams. A deterministic segmenter provides one interpretable signal for ranking or inspecting those candidates: strings that form known word sequences are more plausible than strings with no valid segmentation.

The supplementary reflection in `docs/cryptography-reflection/` discusses cryptanalysis as a pipeline involving intercepted traffic, cribs, constraint pruning, candidate testing, and operational decisions. It is included as background showing the conceptual motivation for studying cryptography, not as part of the executable system.

## Limitations

- Plausibility is limited by dictionary coverage.
- A valid sequence of words is not necessarily a semantically coherent sentence.
- The handcrafted score is not a statistical language model.
- The small included `words.txt` is designed for demonstration, not broad English coverage.
- The implementation does not decrypt ciphertext, identify keys, or evaluate cipher security.
- The source uses the exact output spelling `Nonsense`; this README documents observed behavior rather than changing it.

## Source preservation

All Python source files and supporting artifacts included from the upload are preserved byte-for-byte. No implementation, comments, identifiers, formatting, constants, or behavior were changed.

The featured file was copied only to a clearer repository path. Alternate uploaded variants are retained under `development/` instead of being merged or rewritten. See `ORIGINAL_FILE_MANIFEST.tsv` for original paths, portfolio paths, file sizes, and SHA-256 hashes.

## Academic origin

This work began as a cryptography-course exercise and is presented here as a focused algorithmic portfolio artifact. The portfolio framing, repository organization, verification record, and root documentation were added later; the original implementation remains unchanged.
