from django.urls import path
from . import views


urlpatterns = [
    path("login/", views.login_or_register, name="login_or_register"),
    path("", views.index, name="index"),
    path("visit/<str:point_id>/", views.visit_point, name="visit_point"),
    path("graph/", views.graph, name="graph"),
    path("players/", views.players, name="players"),
    # api
    path('graph/json/', views.graph_json, name='graph-json'),
    path('graph/save/', views.graph_save, name='graph-save'),
]