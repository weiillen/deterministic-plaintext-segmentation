# Verification Record

The featured implementation was executed without modification using Python 3 and the included `data/words.txt` dictionary.

## Commands

```bash
cd data
printf 'MEETMEATTHEPARK\n' | python3 ../src/hw1.py
printf 'MEETMEAT\n' | python3 ../src/hw1.py
printf 'MEAT\n' | python3 ../src/hw1.py
printf 'ABCD\n' | python3 ../src/hw1.py
printf 'IATTHEPARK\n' | python3 ../src/hw1.py
printf 'meetme\n' | python3 ../src/hw1.py
printf '\n' | python3 ../src/hw1.py
python3 -m py_compile ../src/hw1.py
```

## Observed output

```text
MEETMEATTHEPARK -> MEET ME AT THE PARK
MEETMEAT        -> MEET ME AT
MEAT            -> MEAT
ABCD            -> Nonsense
IATTHEPARK      -> I AT THE PARK
meetme          -> Nonsense
(empty input)   -> Nonsense
```

`python3 -m py_compile` completed successfully.

## Scope

This is a reproducibility check, not a comprehensive correctness proof. The result depends on the active dictionary and the deterministic scoring rules embedded in the preserved source.
