from geopy.geocoders import Nominatim
from numpy import arange
import pickle

geolocator = Nominatim(user_agent="kairy")
countries = [
    {"Singapore": (arange(1.249187, 1.471469, 1e-5), arange(103.612408, 104.03, 1e-5))},
    {"India": (arange(8, 37.2, 1e-5), arange(68, 97.42, 1e-5))},
]

addresses = {}
for country in countries:
    for name, (lats, lons) in country.items():
        addresses[name] = set()
        for lat, lon in zip(lats, lons):
            if (
                geolocator.reverse(f"{lat}, {lon}")
                and geolocator.reverse(f"{lat}, {lon}").address not in addresses[name]
            ):
                addresses[name].add(geolocator.reverse(f"{lat}, {lon}").address)

    with open("../resources/data/addresses.pkl", "wb") as f:
        pickle.dump(addresses, f)

print(addresses)
