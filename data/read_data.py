import json
import pprint
import pandas as pd

pp = pprint.PrettyPrinter(indent=4)
with open('map_dictionary.json') as json_file:
    map_dictionary = json.load(json_file)

with open('countries_dictionary.json') as json_file:
    countries_dict = json.load(json_file)

important_countries_name = []
"""
for country in data['2003']:
    if country in countries_dict:
        important_countries_name.append(country)
"""

data = pd.read_csv('data.csv')
print(data.head())

super_clean_data = {}
for year in data.columns[2:]: 
    super_clean_data[str(year)] = {"areas":{}}
    for country_name in data["country_name"]:
        # print(country_name)
        if country_name in countries_dict:
            country_code = countries_dict[country_name]
            if country_code in map_dictionary:
                super_clean_data[str(year)]["areas"][country_code] = {}
                super_clean_data[str(year)]["areas"][country_code]['href'] = map_dictionary[country_code]['href']
                super_clean_data[str(year)]["areas"][country_code]['tooltip'] = map_dictionary[country_code]['tooltip']
                super_clean_data[str(year)]["areas"][country_code]['name'] = country_name
                super_clean_data[str(year)]["areas"][country_code]['value'] = float(data.loc[data['country_name'] == country_name][str(year)].values) #data.loc[0:, ['country_code',str(1960)]] #data[str(year)][country_name]

pp.pprint(super_clean_data['2003'])
print(len(super_clean_data['2004']))
with open('super_clean_data.json', 'w') as outfile:
    json.dump(super_clean_data, outfile)