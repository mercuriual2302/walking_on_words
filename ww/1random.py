import random

def is_lyndon(word):
    """
    Check if the given word is a Lyndon word.
    A word is Lyndon if it is strictly lexicographically smaller than all of its rotations.
    """
    n = len(word)
    for i in range(1, n):
        rotated = word[i:] + word[:i]
        if rotated < word:
            return False
    return True

def is_debruijn(word, k, n):
    """
    Check if the given word is a de Bruijn sequence for alphabet size k and subsequences of length n.
    
    A de Bruijn sequence (in its minimal cyclic representation) must have length k**n,
    and every possible substring of length n (taken cyclically) appears exactly once.
    """
    L = len(word)
    if L != k ** n:
        return False  # The length is not correct.
    
    seen = {}
    # Check cyclically for every starting position.
    for i in range(L):
        # Construct the substring of length n in a cyclic manner.
        if i + n <= L:
            substring = word[i:i+n]
        else:
            substring = word[i:] + word[:(i+n - L)]
        seen[substring] = seen.get(substring, 0) + 1

    # A proper de Bruijn sequence has exactly k^n distinct substrings and each appears once.
    return (len(seen) == k ** n) and all(count == 1 for count in seen.values())

def generate_random_word(length, alphabet):
    """Return a random word (string) of the given length using symbols from the alphabet."""
    return "".join(random.choice(alphabet) for _ in range(length))

def main():
    print("Random Word Generator for Lyndon and de Bruijn Words")
    
    # Get alphabet size from user.
    try:
        k = int(input("Enter alphabet size (e.g., 2 for binary, 3, etc.): "))
    except ValueError:
        print("Invalid input for alphabet size.")
        return

    # Build a simple alphabet.
    if k <= 10000:
        # Use digits 0,1,...,k-1
        alphabet = [str(i) for i in range(k)]
    elif k <= 26:
        # Use the first k lowercase letters.
        alphabet = list("abcdefghijklmnopqrstuvwxyz"[:k])
    else:
        # For larger k, use string representations of numbers.
        alphabet = [str(i) for i in range(k)]
    
    # Get number of random words to generate.
    try:
        num_words = int(input("Enter number of random words to generate: "))
    except ValueError:
        print("Invalid input for number of words.")
        return

    # Get word length for Lyndon word check.
    try:
        word_length = int(input("Enter word length for Lyndon word check: "))
    except ValueError:
        print("Invalid input for word length.")
        return

    # For de Bruijn check, get parameter n.
    # (A de Bruijn sequence for parameters (k,n) must have length k**n.)
    try:
        n_for_debruijn = int(input("Enter n for de Bruijn word check (word length will be k^n): "))
    except ValueError:
        print("Invalid input for n.")
        return

    debruijn_length = k ** n_for_debruijn

    # Generate random words for the Lyndon check.
    lyndon_count = 0
    for _ in range(num_words):
        word = generate_random_word(word_length, alphabet)
        if is_lyndon(word):
            lyndon_count += 1

    proportion_lyndon = lyndon_count / num_words

    # Generate random words for the de Bruijn check.
    debruijn_count = 0
    for _ in range(num_words):
        word = generate_random_word(debruijn_length, alphabet)
        if is_debruijn(word, k, n_for_debruijn):
            debruijn_count += 1

    proportion_debruijn = debruijn_count / num_words

    print("\nRESULTS:")
    print(f"Out of {num_words} random words of length {word_length},")
    print(f"  proportion that are Lyndon words: {proportion_lyndon:.6f}")
    print(f"Out of {num_words} random words of length {debruijn_length} (for de Bruijn check),")
    print(f"  proportion that are de Bruijn sequences: {proportion_debruijn:.6f}")

if __name__ == "__main__":
    main()
