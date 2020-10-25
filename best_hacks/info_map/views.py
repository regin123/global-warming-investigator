from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from matplotlib import pyplot as plt
import json
import itertools
import io
import PIL
import pylab
from math import radians, cos, sin, asin, sqrt, atan2

# Create your views here.
from django.template import loader


import re

def getCities():
    with open('/data', 'r') as file:
        dic = {}
        lines = file.readlines()
        for line in lines:
            line = line.strip("\n")
            values = re.split("  +", line)

            if len(values) == 3:
                if values[2][-1] == 'N' or values[2][-1] == 'S':
                    lat = values[1]
                    deg, minutes, direction = re.split('[°\']', lat)
                    lat_n = (float(deg) + float(minutes)/60) * (-1 if direction in ['W', 'S'] else 1)
                    longt = values[2]
                    deg, minutes, direction = re.split('[°\']', lat)
                    longt_n = (float(deg) + float(minutes)/60) * (-1 if direction in ['W', 'S'] else 1)
                    dic[values[0]] = [lat_n, longt_n]

        print(dic)








def display_map(request):
    data = read_json('data/original_data.json')
    context = generate_graphs_dict(get_countries(data), data)
    for k, v in context.items():
        print(k, v)
    return render(request=request,
                  template_name="only_map.html",
                  context=context)

def display_map_poland(request):
    return render(request, 'Poland.html', {})


def consequences(request):
    return render(request, 'consequences.html')


def prevention(request):
    return render(request, 'prevention.html')


def country_graph(request, country_alpha2):
    data = read_json('data/original_data.json')
    x, y = get_data_country(data, country_alpha2)
    plt.plot(x, y)
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
    for year in data:
        value = float(data[year]["areas"][country_alpha2.upper()]["value"])
        x.append(year), y.append(value)
    return x, y

def get_countries(data):
    return union_sets([set(data[k]['areas'].keys()) for k in list(data.keys())])


def union_sets(args):
    return set(frozenset(itertools.chain.from_iterable(args)))

@require_http_methods(["GET"])
def count_co2(request):
    wspolrzedneX = {
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
    }
    fromX= wspolrzedneX[request.GET.get('fromP')]
    fromY = wspolrzedneY[request.GET.get('fromP')]
    toX= wspolrzedneX[request.GET.get('toP')]
    toY = wspolrzedneY[request.GET.get('toP')]

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

    print("Results:", distance)
    print("emisja samochodu: ", 122.3*distance/1000," kilogramów CO2")
    print("emisja samolotu: ", 50*distance," kilogramów CO2")

    return 0
