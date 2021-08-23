from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name="index"),
    path('abg.html', views.abg, name="abg"),
    path('index.html', views.index, name="index"),
    path('broke.html', views.broken, name="broke"),
    path('charts.html', views.charts, name="charts"),
    path('tables.html', views.tables, name="tables"),
    path('cards.html', views.cards, name="cards"),
    path('buttons.html', views.buttons, name="buttons"),
    path('utilities-animation.html', views.ua, name="ua"),
    path('utilities-border.html', views.ub, name="ub"),
    path('utilities-color.html', views.uc, name="uc"),
    path('utilities-other.html', views.uo, name="uo"),
]
