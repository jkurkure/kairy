import pickle


# Load tokens only when needed
def load_tokens():
    return pickle.load(open("resources/data/tokens.pkl", "rb"))


# Common hashing functions
def simple_hasher(s):
    return sum([ord(c) for c in s])


def easy_hasher(s):
    return eval("*".join([str(ord(c)) for c in s]))


# Secret key for username generation
SECRET_KEY = """
Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Sed odio morbi quis commodo odio aenean sed. Malesuada pellentesque elit eget gravida cum. Ut lectus arcu bibendum at varius vel pharetra vel turpis. Tempus imperdiet nulla malesuada pellentesque elit eget. Massa enim nec dui nunc mattis enim. Nulla facilisi etiam dignissim diam quis enim lobortis scelerisque fermentum. Sed nisi lacus sed viverra. Nibh sit amet commodo nulla facilisi nullam vehicula. Augue lacus viverra vitae congue. Mi proin sed libero enim. Senectus et netus et malesuada fames ac turpis egestas integer.
"""
# Replace the above with your own string of similar length on your local
# copy to further perplex brute-force attempts.
