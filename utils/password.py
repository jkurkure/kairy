import string
import sys
from utils.common import simple_hasher


def generate_password(input_string, length):
    # Import random here to avoid circular imports
    import random

    # Set a fixed seed value
    random.seed(simple_hasher(input_string))

    characters = string.ascii_letters + string.digits + string.punctuation
    password = "".join(random.choice(characters) for _ in range(length))
    return password


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python password.py <input_string>")
        sys.exit(1)

    input_string = sys.argv[1]
    password = generate_password(input_string, 21)
    print(f"Input string: {input_string}")
    print(f"Generated password: {password}")
