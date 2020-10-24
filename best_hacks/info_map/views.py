from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
from django.template import loader


def display_map(request):
    template = loader.get_template('only_map.html')
    response_body = template.render({'current_user': request.user})
    return HttpResponse(response_body)
