# Run before first run of the app

import pickle
from names_dataset import NameDataset

try:
    from nltk.corpus import brown
except:
    import nltk

    nltk.download("brown")


nd = NameDataset()
lastNames = list(
    nd.get_top_names(n=100, use_first_names=False, country_alpha2="SG")["SG"]
)
firstNames = list(nd.get_top_names(n=100, country_alpha2="SG")["SG"]["M"]) + list(
    nd.get_top_names(n=100, country_alpha2="SG")["SG"]["F"]
)

with open("resources/data/names.pkl", "wb") as f:
    pickle.dump((firstNames, lastNames), f)

file_path = "resources/data/tokens.pkl"

tokens = [w for w in brown.words() if len(w) > 4 and w.istitle()]
with open(file_path, "wb") as f:
    pickle.dump(tokens, f)
