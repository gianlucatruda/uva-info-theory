import math
import string
from copy import deepcopy
from itertools import product

alph = string.ascii_uppercase
mapping = {c: i + 1 for i, c in enumerate(alph)}


class Element:
    def __init__(self, c):
        self.char = c
        self.value = mapping[c]

    def neg(self):
        self.value = -1 * self.value
        return self

    def __add__(self, other):
        out_val = (self.value + other.value) % len(alph)
        out_char = alph[out_val - 1]
        return Element(out_char)

    def __repr__(self):
        return self.char


class Text:
    def __init__(self, s, l=None):
        self.text = s
        self.elements = [Element(c) for c in s]
        if l is not None:
            self.elements = [Element(s[c % len(s)]) for c in range(l)]

    def neg(self):
        neg_me = deepcopy(self)
        neg_me.elements = [e.neg() for e in neg_me.elements]
        return neg_me

    def __repr__(self):
        return self.text

    def __add__(self, other):
        out = [a + b for a, b in zip(self.elements, other.elements)]
        out_text = ""
        for c in out:
            out_text += c.char
        return Text(out_text)

    def __sub__(self, other):
        neg_other = other.neg()
        return self.__add__(neg_other)


def encrypt(message, key):
    m = Text(message)
    k = Text(key, l=len(message))
    c = m + k
    return c.text


def decrypt(ciphertext, key):
    c = Text(ciphertext)
    k = Text(key, l=len(ciphertext))
    m = c - k
    return m.text


def coll_prob(text, alph=string.ascii_uppercase):
    counts = {c: text.count(c) for c in alph}
    total = sum(counts.values())
    freqs = {c: v / total for c, v in counts.items()}
    cp = sum([p ** 2 for p in freqs.values()])
    return cp


def kappa_test(coll_PM, coll_PK, coll_PC):
    return (coll_PM - coll_PK) / (coll_PC - coll_PK)


if __name__ == "__main__":
    C = "QMIXFFKFMVPZSVYGOMAPOTTCUUBGIIPPOTPZEVNVJHIUBGSCDCIPXBKDBRSIXFMVIUVJBCWYNPMVNSDFNDZDWQCVFLKZCGMXYJNJBAQPXISUEFVGGITFMQNOEIATBWG"
    # Calculate collision prob. of ciphertext
    coll_PC = coll_prob(C)
    print(coll_PC)
    # We know coll_PM and coll_PK
    coll_PM = 0.0655
    coll_PK = 0.0385
    # Figure out k, the length of K
    k = round(kappa_test(coll_PM, coll_PK, coll_PC))
    print("Key length:", k)
    # We already know some likely words from M
    likelies = ["CLEOPATRA", "CAESAR", "QUEEN", "GRACE", "ALEXANDRIA"]

    possible_keys = []
    for word in likelies:
        for K in product(alph, repeat=k):
            K = "".join(K)
            query = encrypt(word, K)
            if query in C:
                possible_keys.append(K)
                print(K, word)
    # Now try decode whole message with each candidate key
    for K in possible_keys:
        print(K, decrypt(C, K))
