import random
import string
import sys


def generate_password(input_string, length):
    random.seed(sum([ord(c) for c in input_string]))  # Set a fixed seed value
    characters = string.ascii_letters + string.digits + string.punctuation
    password = "".join(random.choice(characters) for _ in range(length))
    return password


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python pword-hash.py <input_string>")
        sys.exit(1)

    input_string = sys.argv[1]
    password = generate_password(input_string, 21)
    print(f"Input string: {input_string}")
    print(f"Generated password: {password}")
