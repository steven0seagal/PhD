from django.urls import path
from . import views

urlpatterns = [
    path('',views.ffas_main, name = 'ffas_main'),
    path('ffas_analysis', views.ffas_analysis, name='ffas_analysis'),
]