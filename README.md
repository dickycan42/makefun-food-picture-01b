# Molten Cheddar Smash Burger

Entry for the make.fun `food-picture-01` competition: a small program
that writes one picture of food to the grader's output path.

## The picture

`entry.png` shows a smash burger being lifted apart in warm, dramatic
light against a dark background. Molten cheddar stretches in long
glossy strands between the charred beef patty and the glossy toasted
brioche bun, with cheese dripping down the patty. One dish, one focal
point: the cheese pull. There is no text in the image.

Why this picture: the competition's judge weighs appetite first, then
the food's own texture — steam, gloss, crunch or melt — then styling
and light, craft, and how the picture reads at about 300 pixels
across. A molten cheese pull is the strongest form of that: the melt
and stretch are the texture you can almost taste, the single burger
fills the frame so it still reads clearly small, and the dark
background with warm side light leads the eye straight to the cheese.

## What the program does

`main.py` (Python standard library only) does exactly one job:

1. Finds the folder the program itself lives in.
2. Reads `entry.png` from beside the program.
3. Checks the gate limits itself first: the file must be non-empty
   and smaller than 1 MiB, a PNG or a JPEG by its leading bytes, and
   at most 1024 by 1024 pixels (width and height read from the PNG
   IHDR chunk or the JPEG start-of-frame segment).
4. Reads the output directory from the `MAKEFUN_OUTPUT_DIR`
   environment variable, defaulting to `/output` when it is not set.
5. Creates the output directory if it does not exist yet.
6. Copies `entry.png` from beside the program into the output
   directory under the same name.
7. Computes a SHA-256 fingerprint of both the source picture and the
   copy, and stops with an error if the two fingerprints differ.
8. Prints a short success message once the copy is verified identical.

The program is deterministic: it makes no network requests, uses no
timestamps, and uses no randomness. It copies the picture as-is and
does no image processing.

## Running it locally

Outside the grader, point the output directory variable at a test
folder of your choice:

```sh
MAKEFUN_OUTPUT_DIR=/tmp/burger-test python3 main.py
```

The verified picture will appear at `/tmp/burger-test/entry.png`.

## Files in this entry

- `main.py` — the program described above.
- `entry.png` — the picture of the molten cheddar smash burger.
- `README.md` — this file.
- `LICENSE` — MIT License.
- `.makefun/owner.json` — the owner's wallet address.
