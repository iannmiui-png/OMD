import os
import random

def randomize_slashes(text):
    return "".join(
        random.choice(['/','\\']) if ch in "/\\" else ch
        for ch in text
    )

def next_unary_filename():
    name = "!"
    while os.path.exists(name):
        name += "!"
    return name

# read source
with open("source.txt", "r", encoding="utf-8") as f:
    data = f.read()

# randomize slashes
rand = randomize_slashes(data)

# pick unary filename
outname = next_unary_filename()

# write
with open(outname, "w", encoding="utf-8") as f:
    f.write(rand)

print("Wrote:", outname)
