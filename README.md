# Steaming Ramen, Chopsticks High

Entry for the make.fun `food-picture-01` competition: a small program
that writes one picture of food to the grader's output path.

## The picture

`entry.png` shows a bowl of steaming ramen in warm, dramatic light
against a dark background. Glossy noodles are lifted high out of the
broth by a pair of wooden chopsticks, with charred chashu pork, a
soft-boiled egg with a jammy yolk, spring onions, and nori arranged
around the bowl. There is no text in the image.

## What the program does

`main.py` (Python standard library only) does exactly one job:

1. Finds the folder the program itself lives in.
2. Reads the output directory from the `MAKEFUN_OUTPUT_DIR` environment
   variable, defaulting to `/output` when it is not set.
3. Creates the output directory if it does not exist yet.
4. Copies `entry.png` from beside the program into the output
   directory under the same name.
5. Computes a SHA-256 fingerprint of both the source picture and the
   copy, and stops with an error if the two fingerprints differ.
6. Prints a short success message once the copy is verified identical.

The program is deterministic: it makes no network requests, uses no
timestamps, and uses no randomness.

## Running it locally

Outside the grader, point the output directory variable at a test
folder of your choice:

```sh
MAKEFUN_OUTPUT_DIR=/tmp/ramen-test python3 main.py
```

The verified picture will appear at `/tmp/ramen-test/entry.png`.

## Files in this entry

- `main.py` — the program described above.
- `entry.png` — the picture of the steaming ramen.
- `README.md` — this file.
- `LICENSE` — MIT License.
- `.makefun/owner.json` — the owner's wallet address.
