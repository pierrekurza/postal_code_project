import argparse

from postal_city_search import CityOrPostalCodeSearch

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog="Search City", description="Search cities by postal code")
    parser.add_argument('-c', '--city')
    parser.add_argument('-p', '--postalcode')
    args = parser.parse_args()
    city_or_postal_code_search = CityOrPostalCodeSearch()
    city_or_postal_code_search.manage_options(args)
