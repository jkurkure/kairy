import sys
from utils.common import simple_hasher, easy_hasher, SECRET_KEY, load_tokens


def generate_uname(input_string, length):
    # Import random here to avoid circular imports
    import random

    # Set a fixed seed value
    random.seed(
        simple_hasher(SECRET_KEY) * simple_hasher(input_string)
        + easy_hasher(input_string)
    )

    tokens = load_tokens()
    uname = []

    for _ in range(length):
        uname.append(random.choice(tokens))

    return "-".join(uname)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python username.py <input_string> <length>")
        sys.exit(1)

    input_string = sys.argv[1]
    length = int(sys.argv[2])
    username = generate_uname(input_string, length)
    print(f"Input string: {input_string}")
    print(f"Generated username: {username}")
