from django.http import HttpResponse
from django.shortcuts import render
from matplotlib import pyplot as plt
import json
import itertools
import io
import PIL
import pylab


def display_map(request):
    data = read_json('data/co2_emission_ton_per_person.json')
    context = generate_graphs_dict(get_countries(data), data)
    return render(request=request,
                  template_name="only_map.html",
                  context={"data": context})


def display_map_poland(request):
    return render(request, 'Poland.html', {})


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
