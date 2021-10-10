'''
Additional classes to give the list of
countries, languages, cities etc.
'''


import csv


'''
Function, returning the list of all cities.
Uses 'cities.csv' file data.
'''
def get_cities():
    # Creating cities list
    city_list = []
    cities = csv.reader(open('cities.csv', 'r', newline=''), delimiter=';')
    for city in list(cities)[1:]:
        city_data = {
            'name': city[2],
            'city_id': int(city[0]),
            'country_id': int(city[1]),
        }
        city_list.append((city_data, city_data['name']))
    return city_list


'''
Function, returning the list of all countries.
Uses 'countries.csv' file data.
'''
def get_countries():
    #Creating countries list
    country_list = []
    city_list = get_cities()
    countries = csv.reader(open('countries.csv', 'r', newline=''), delimiter=';')
    for country in list(countries)[1:]:
        country_data = {
            'name': country[1],
            'country_id': int(country[0]),
            'city_list': [city[0] for city in city_list if city[0]['country_id'] == int(country[0])],
        }
        country_list.append((country_data, country_data['name']))
    return country_list


'''
Function, returning the list of all languages.
Uses 'languages.csv' file data.
'''
def get_languages():
    #Creating language list
    language_list = []
    languages = csv.reader(open('languages.csv', 'r', newline=''), delimiter=',')
    for language in list(languages)[1:]:
        language_data = {
            'name': language[3],
            'language_id': language[0],
        }
        language_list.append((language_data, language_data['name']))
    return language_list


'''
Function, returning the list of all universities.
Uses 'universities.csv' file data.
'''
def get_universities():
    #Creating university list
    university_list = []
    universities = csv.reader(open('universities.csv', 'r', newline=''), delimiter=',')
    for university in universities:
        university_data = {
            'name': university[1],
            'country': university[0],
            'site_url': university[2],
        }
        university_list.append((university_data, university_data['name']))
    return university_list
