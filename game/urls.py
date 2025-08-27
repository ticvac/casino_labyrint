from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("visit/<str:point_id>/", views.visit_point, name="visit_point"),
    path("graph/", views.graph, name="graph"),
]