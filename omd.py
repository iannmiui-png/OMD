import os
import sys
import random
import base64
import re
import time

# ------------------ unary file reader ------------------

def unary_files_in(dirpath):
    files = [f for f in os.listdir(dirpath) if set(f) == {"!"}]
    files.sort(key=len)
    return files

target_dir = r"C:\!" + "\\"   # safe, correct Windows 7 path

# Load the LAST unary file safely
text = None
for fname in unary_files_in(target_dir):
    full = os.path.join(target_dir, fname)
    try:
        with open(full, "r", encoding="utf-8", errors="replace") as f:
            text = f.read()
    except PermissionError:
        # unary EOF — ignore and continue
        continue

# If nothing loaded, stop
if text is None:
    print("No unary files found.")
    sys.exit(0)

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
        if not I:
            break
        if c not in "/\\":
            continue
        key = (I, c)
        if key in succ_table:
            I = succ_table[key]
        else:
            I = random.choice(list(fail_states))
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

        # lowercase letter
        if c.isalpha() and c.islower():
            left_window = text[max(0, center - 2):center]
            if any(ch.isupper() for ch in left_window):
                cleaned = re.sub(r"[\\/]", "", chunk)
                left_slash = text[center - 1] if center - 1 >= 0 and text[center - 1] in "/\\" else ""
                right_slash = text[center + 1] if center + 1 < n and text[center + 1] in "/\\" else ""
                blob = (left_slash + c + right_slash).encode("utf-8")
                b64 = base64.b64encode(blob).decode("ascii")

                for _ in range(16):
                    S = random.choice(["/", "\\", "//", "\\\\", "/\\", "\\/"])
                    I = slash(S, chunk)
                    if I and I not in fail_states:
                        return chunk, S

        # uppercase letter
        if c.isalpha() and c.isupper():
            left_upper = center > 0 and text[center - 1].isupper()
            right_upper = center + 1 < n and text[center + 1].isupper()

            if not (left_upper or right_upper):
                continue

            cleaned = re.sub(r"[\\/]", "", chunk)
            blob = c.encode("utf-8")
            b64 = base64.b64encode(blob).decode("ascii")

            for _ in range(16):
                S = random.choice(["/", "\\", "//", "\\\\", "/\\", "\\/"])
                I = slash(S, chunk)
                if I and I not in fail_states:
                    return chunk, S

# ------------------ main engine loop ------------------

try:
    while True:
        result = random_chunk_parse(text)
        if result:
            P, S = result
            programForm = re.sub(r"\s+", " ", P.replace("#", "")).strip()
            print(S)
            print(programForm)

        time.sleep(0.12)

except KeyboardInterrupt:
    print("\nStopped by user")
