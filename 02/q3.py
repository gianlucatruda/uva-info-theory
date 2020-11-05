from collections import Counter
import math
import string
import re

## parse input file, convert to lowercase, remove punctuation
f = open("Jack.txt")
data = f.read().lower()
regex = re.compile("[^a-z ]")
data = regex.sub("", data)

## create a dictionary containing the frequencies for all characters (incl. space)
alphabet = "abcdefghijklmnopqrstuvwxyz "
frequencies = {c: data.count(c) for c in alphabet}
total = sum(frequencies.values())

P = {k: v / total for k, v in frequencies.items()}
# print(P, sum(P.values()))

# Calculate upper bound
ub = math.log2(len(alphabet))
print("Trivial upper bound:", ub)

# Calculate entropy
ent = -1 * sum([P[c] * math.log2(P[c]) for c in P.keys()])
print("Entropy of 1 letter:", ent)

# Make dictionary of 2-letter combos and normalise
freqs_2 = {f"{c1}{c2}": data.count(f"{c1}{c2}") for c1 in alphabet for c2 in alphabet}
total = sum(freqs_2.values())
P2 = {k: v / total for k, v in freqs_2.items()}
ent2 = -1 * sum([P2[k] * math.log2(P2[k]) for k in P2.keys() if P2[k] > 0])
print("Entropy of 2 letters:", ent2)

# Calculate conditional entropy
# H(Y|X) = H(YX) - H(X)
H_X = ent
H_YX = ent2
print(f"H(Y|X) = {H_YX} - {H_X} = {H_YX - H_X: .3f}")

print("\n\nQuestion 3a - calculate entropy at word-level")

# Find all unique words
words = list(set([w for w in data.split()]))
print("Unique words:", len(words))

# Count word frequencies
word_freqs = {k: data.count(k) for k in words}
total = sum(word_freqs.values())
P_word = {
    k: v / total
    for k, v in sorted(word_freqs.items(), key=lambda x: x[1], reverse=True)
}

# Calculate entropy
ent = -1 * sum([P_word[w] * math.log2(P_word[w]) for w in P_word.keys()])
print("Word-level entropy:", ent)


print("\n\nQuestion 3d - calculate cross entropy")
# HC(P_XY, P_X·P_Y)
cross_ent = -1 * sum(
    [P2[c1 + c2] * math.log2(P[c1] * P[c2]) for c1 in alphabet for c2 in alphabet]
)
print("Cross-entropy:", cross_ent)
