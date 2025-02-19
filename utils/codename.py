import geonamescache
import username

# Initialize the GeonamesCache object
gc = geonamescache.GeonamesCache()

# Get all cities
cities = gc.get_cities()

# Filter cities and towns in India
indian_cities = [city['name'] for city in cities.values() if city['countrycode'] == 'IN']

def get(seed):
    combhasher = lambda s: username.easy_hasher(s) + username.simple_hasher(s)
    return f'{indian_cities[combhasher(seed) % len(indian_cities)]}-{username.generate_uname(seed, 1)}'