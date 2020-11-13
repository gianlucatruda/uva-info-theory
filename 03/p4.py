import math


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
