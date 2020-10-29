import string
import sys
from pathlib import Path


# Get all 26 lowercase letters of English
alph = string.ascii_lowercase

print("Alphabet:", alph)


def compute_probabilities(text, X=alph):
    """Compute dictionary of letter probabilities of text for alphabet X
    """

    # Convert to lowercase (just to be sure)
    text = text.lower()

    # Make empty dictionary with letters as keys
    counts = {k: 0 for k in X}

    # Keep track of total length of legitimate characters
    total = 0

    # Loop through text and update counts only for alphabet
    for c in text:
        if c in X:
            total += 1
            counts[c] += 1

    # Normalise the counts and return
    return {k: c / total for k, c in counts.items()}


def var_dist(P, Q, X=alph):
    """Compute variational distance between P and Q for alphabet X
    """

    dist = 0.5 * sum([abs(P[x] - Q[x]) for x in X])

    return dist


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Please provide a path to data files as argument.")

    path = Path(sys.argv[1])

    # Read in all the files and compute probability distributions
    langs = {}
    for filename in path.glob("Alice_*"):
        with open(filename) as file:
            text = file.read().lower()
            lang = filename.name.split("_")[1].split(".")[0]
            langs[lang] = compute_probabilities(text)

    # Compute variational distance in pairwise fashion
    results = {}
    for lang1, P in langs.items():
        for lang2, Q in langs.items():
            if lang1 != lang2:
                variational_dist = var_dist(P, Q)
                results[f"{lang1}-{lang2}"] = variational_dist

    # Sort results by var. dist. (descending)
    results = {
        k: v for k, v in sorted(results.items(), key=lambda x: x[1], reverse=True)
    }

    # Print results
    for k, v in results.items():
        print(k, v, sep="\t")
