from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from matplotlib import pyplot as plt
import json
import itertools
import io
import PIL
import pylab
from math import radians, cos, sin, asin, sqrt, atan2
import data.polish_cities.data_parser as parser

# Create your views here.
from django.template import loader


def display_map(request):
    data = read_json('data/co2_emission_ton_per_person.json')
    context = generate_graphs_dict(get_countries(data), data)
    return render(request=request,
                  template_name="only_map.html",
                  context={"data": context})


def display_map_poland(request):
    cities_dictionairy = parser.get_cities_data()
    cities = list(cities_dictionairy.keys())
    return render(request, 'Poland.html', {'cities': cities})


def consequences(request):
    return render(request, 'consequences.html')


def prevention(request):
    return render(request, 'prevention.html')


def country_graph(request, country_alpha2):
    data = read_json('data/co2_emission_ton_per_person.json')
    x, y = get_data_country(data, country_alpha2)
    plt.plot(x, y)
    plt.xticks(rotation=90)
    buffer = io.BytesIO()
    canvas = pylab.get_current_fig_manager().canvas
    canvas.draw()
    graphIMG = PIL.Image.frombytes('RGB', canvas.get_width_height(), canvas.tostring_rgb())
    graphIMG.save(buffer, "PNG")
    pylab.close()
    return HttpResponse(buffer.getvalue(), content_type="Image/png")


def generate_graphs_dict(countries_alphas2, data):
    d = dict()
    for x in countries_alphas2:
        d[x] = (get_data_country(data, x))
    return d


def read_json(file):
    with open(file) as json_file:
        data = json.load(json_file)
        return data


def get_data_country(data, country_alpha2):
    x, y = [], []
    years = set()
    for year in data:
        value = float(data[year]["areas"][country_alpha2.upper()]["value"])
        x.append(int(year)), y.append(value)
        years.add(year)
    return x, y


def get_countries(data):
    return union_sets([set(data[k]['areas'].keys()) for k in list(data.keys())])


def union_sets(args):
    return set(frozenset(itertools.chain.from_iterable(args)))


@require_http_methods(["GET", "POST"])
def count_co2(request):
    cities_dictionairy = parser.get_cities_data()
    cities = list(cities_dictionairy.keys())
    """wspolrzedneX = {
        "Warsaw": 52.12,
        "Wroclaw": 51.07,
        "Krakow": 50.04,
        "Moscow": 55.45,
        "Sydney": 39.54,
        "Chicago": 41.54
    }
    wspolrzedneY = {
        "Warsaw": 21.02,
        "Wroclaw": 17.2,
        "Krakow": 19.56,
        "Moscow": 37.37,
        "Sydney": 116.23,
        "Chicago":  86.39
    }"""
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
    return render(request, 'Poland.html', context={"data": data, "cities": cities})
