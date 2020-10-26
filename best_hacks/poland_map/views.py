from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from math import radians, cos, sin, asin, sqrt, atan2

import data.polish_cities.data_parser as parser


def display_map_poland(request):
    cities_dictionary = parser.get_cities_data()
    cities = list(cities_dictionary.keys())
    return render(request, 'poland.html', {'cities': cities})


@require_http_methods(["GET", "POST"])
def count_co2(request):
    cities_dictionairy = parser.get_cities_data()
    cities = list(cities_dictionairy.keys())
    fromX = cities_dictionairy[request.GET['fromP']][0]
    fromY = cities_dictionairy[request.GET['fromP']][0]
    toX = cities_dictionairy[request.GET['toP']][1]
    toY = cities_dictionairy[request.GET['toP']][1]

    # approximate radius of earth in km
    R = 6373.0

    lat1 = radians(fromX)
    lon1 = radians(fromY)
    lat2 = radians(toX)
    lon2 = radians(toY)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    result = ""
    result = result + ("Results:" + str(distance))
    result = result + ("\nCar emission: " + str(122.3 * distance / 1000) + "kg of CO2")
    result = result + ("\nPlane emission: " + str(50 * distance) + " kg of CO2")
    data = dict()
    data['result'] = result
    return render(request, 'poland.html', context={"data": data, "cities": cities})
