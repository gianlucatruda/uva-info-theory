from problem4 import compute_probabilities, var_dist
import string

if __name__ == "__main__":
    # Read in the english file
    with open("alice/Alice_eng.txt") as file:
        text = file.read().lower()
        P = compute_probabilities(text)

    # Check that exactly 26 lowercase characters
    assert len(P.keys()) == 26
    assert all([x in string.ascii_lowercase for x in P.keys()])

    # Check that probabilities sum to 1
    assert 1.0 - sum(P.values()) < 1e-15

    # Check var. dist. to own distribution
    assert var_dist(P, P) == 0.0

    # Check that compute_probabilities works as expected
    probs = compute_probabilities("  áB 7\n # Ü b ccC.*")
    assert probs['a'] == 0
    assert probs['b'] == 2 / 5
    assert probs['c'] == 3 / 5
    assert 1.0 - sum(probs.values()) < 1e-15

    print("All checks passed.")
