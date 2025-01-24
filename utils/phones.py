from phone_iso3166.country import *
import pycountry 
  
def where(number):
    c = phone_country(number) 
    
    country = pycountry.countries.get(alpha_2 = c) 
    return (country.flag, country.name)