"""best_hacks URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from best_hacks.world_map import views
from django.urls import path, include

urlpatterns = [
    path('', views.display_map, name='map'),
    path('world_map/', views.display_map, name='map'),
    path('graph/<str:country_alpha2>', views.country_graph, name='graph'),
]
