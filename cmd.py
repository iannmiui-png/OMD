import os
import sys
import time
import random
import base64
import re

# ------------------ slash engine ------------------

succ_table = {
    ("/", "/"): "/",
    ("/", "\\"): "\\/",
    ("\\", "/"): "/\\",
    ("\\", "\\"): "\\",
    ("/\\", "/"): "//",
    ("/\\", "\\"): "\\",
    ("\\/", "/"): "/",
    ("\\/", "\\"): "\\\\",
}

fail_states = {"//", "\\\\", "/\\", "\\/"}

def slash(S, P):
    I = S
    for c in P:
        if c not in "/\\":
            continue
        key = (I, c)
        I = succ_table.get(key, random.choice(list(fail_states)))
    return I

# ------------------ random chunk parser ------------------

def random_chunk_parse(text, max_chunk=12):
    n = len(text)
    while True:
        center = random.randint(0, n - 1)
        radius = random.randint(1, max_chunk)
        left = max(0, center - radius)
        right = min(n, center + radius)
        chunk = text[left:right]
        c = text[center]

        if c in "/\\":
            continue

        if c.islower():
            left_window = text[max(0, center - 2):center]
            if any(ch.isupper() for ch in left_window):
                for _ in range(16):
                    S = random.choice(["/", "\\", "//", "\\\\", "/\\", "\\/"])
                    I = slash(S, chunk)
                    if I not in fail_states:
                        return chunk, S

        if c.isupper():
            left_upper = center > 0 and text[center - 1].isupper()
            right_upper = center + 1 < n and text[center + 1].isupper()
            if not (left_upper or right_upper):
                continue
            for _ in range(16):
                S = random.choice(["/", "\\", "//", "\\\\", "/\\", "\\/"])
                I = slash(S, chunk)
                if I not in fail_states:
                    return chunk, S

# ------------------ INFINITE UNARY FILE FOLLOWER ------------------

target_dir = r"C:\!" + "\\"

current_length = 1  # start at "!"

while True:
    fname = "!" * current_length
    full = os.path.join(target_dir, fname)

    # Wait until the file exists
    while not os.path.exists(full):
        time.sleep(0.1)

    # Try to read it
    try:
        with open(full, "r", encoding="utf-8", errors="replace") as f:
            text = f.read()
    except PermissionError:
        # File exists but Windows blocks it → treat as not ready yet
        time.sleep(0.1)
        continue

    # Process the file
    P, S = random_chunk_parse(text)
    programForm = re.sub(r"\s+", " ", P.replace("#", "")).strip()
    print(S)
    print(programForm)

    # Move to next unary file
    current_length += 1
