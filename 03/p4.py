import math
import random


def compress(bitstring):
    """Efficiently compress a bitstring with very few 1s
    """
    # Find positions of all the 1s
    positions = [i for i, c in enumerate(bitstring) if c == "1"]
    # Determine zero padding depending on largest possible index
    pad = math.ceil(math.log2(len(bitstring)))
    encoding = ""
    # Encode the positions of the 1s as sequence of padded bitrings
    for pos in positions:
        encoding += format(pos, f"0{pad}b")
    return encoding


def uncompress(encoding, encode_len=10000):
    """Uncompress an encoding of the positions of 1s, with known output length
    """
    # Determine zero padding depending on known output length
    pad = math.ceil(math.log2(encode_len))
    # Split the encoded bitstring into chunks of `pad` length
    chunks = [encoding[i : i + pad] for i in range(0, len(encoding), pad)]
    # Decode the positions of the 1s from the encoded bitstring
    positions = [int(c, base=2) for c in chunks]
    # Reproduce the original bitstring by filling in zeros and ones
    bitstring = ""
    for p in range(encode_len):
        bitstring += "1" if p in positions else "0"
    return bitstring


def generate_random(length=10000, p=0.01):
    """Generate random binary sequence of length `length` with P(1) = `p`.
    """
    randstring = ""
    for i in range(length):
        if random.uniform(0, 1) <= p:
            randstring += "1"
        else:
            randstring += "0"
    return randstring


def verify_compression(text):
    """Check that decoding reproduces `text`. Return encoded length.
    """
    encoding = compress(text)
    lc = len(encoding)
    decoded = uncompress(encoding, encode_len=len(text))
    assert text == decoded
    return lc

def calc_source_entropy(bitstring):
    l = len(bitstring)
    probs = {c: bitstring.count(c)/l for c in ['0', '1']}
    assert 1.0 - sum(probs.values()) < 1e-15
    return -1 * sum(probs[c] * math.log2(probs[c]) for c in probs.keys())


if __name__ == "__main__":
    # Generate and verify performance on random texts.
    print("Running tests...")
    for i in range(10):
        text = generate_random(length=10000)
        lc = verify_compression(text)
        print(f"l_C: {lc}\tl_C/N: {lc/len(text):.3f}\tCR: {len(text)/lc: .3f}")
    # Check specified text
    with open("random01.txt") as file:
        text = file.read()
    print(f"\nrandom01.txt:")
    lc = verify_compression(text)
    print(f"Source entropy: {calc_source_entropy(text): .3f}")
    print(f"l_C: {lc}\tl_C/N: {lc/len(text):.3f}\tCR: {len(text)/lc: .3f}")

