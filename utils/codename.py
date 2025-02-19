import geonamescache
from .username import easy_hasher, simple_hasher, generate_uname

# Initialize the GeonamesCache object
gc = geonamescache.GeonamesCache()

# Get all cities
cities = gc.get_cities()

# Filter cities and towns in India
indian_cities = [
    city["name"] for city in cities.values() if city["countrycode"] == "IN"
]


def get(seed):
    combhasher = lambda s: easy_hasher(s) + simple_hasher(s)
    return f"{indian_cities[combhasher(seed) % len(indian_cities)]}-{generate_uname(seed, 1)}"
