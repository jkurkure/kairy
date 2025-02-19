import random, sys, platformdirs, pickle, os
from nicegui import app


if app.is_started:
    try:
        from nltk.corpus import brown
    except:
        import nltk

        nltk.download("brown")

data_dir = platformdirs.user_data_dir(appname="uname-generator", appauthor="kairy")
if not os.path.exists(data_dir):
    os.makedirs(data_dir)
file_path = os.path.join(data_dir, "tokens-archive.dat")

if os.path.exists(file_path):
    with open(file_path, "rb") as f:
        tokens = pickle.load(f)
else:
    # Filter out words shorter than 5 characters and those with non-alphabetic
    # characters
    tokens = [w for w in brown.words() if len(w) > 4 and w.istitle()]
    with open(file_path, "wb") as f:
        pickle.dump(tokens, f)

SECRET_KEY = """
Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Sed odio morbi quis commodo odio aenean sed. Malesuada pellentesque elit eget gravida cum. Ut lectus arcu bibendum at varius vel pharetra vel turpis. Tempus imperdiet nulla malesuada pellentesque elit eget. Massa enim nec dui nunc mattis enim. Nulla facilisi etiam dignissim diam quis enim lobortis scelerisque fermentum. Sed nisi lacus sed viverra. Nibh sit amet commodo nulla facilisi nullam vehicula. Augue lacus viverra vitae congue. Mi proin sed libero enim. Senectus et netus et malesuada fames ac turpis egestas integer.
"""

# Replace the above with your own string of similar length on your local
# copy to further perplex brute-force attempts.


def simple_hasher(s):
    return sum([ord(c) for c in s])


def easy_hasher(s):
    return eval("*".join([str(ord(c)) for c in s]))


def generate_uname(input_string, length):
    random.seed(
        simple_hasher(SECRET_KEY) * simple_hasher(input_string)
        + easy_hasher(input_string)
    )  # Set a fixed seed value

    uname = []

    for _ in range(length):
        uname.append(random.choice(tokens))

    return "-".join(uname)


if __name__ == "__main__":
    print(generate_uname(sys.argv[1], int(sys.argv[2])))
