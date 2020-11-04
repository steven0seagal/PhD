from django.urls import path, include
from django.contrib import admin
from . import views
from rest_framework import routers



urlpatterns = [
    path('', views.searchdbcooc, name = 'searchdbcooc'),

    # path('result', views.searchresult, name = 'searchresult'),
    # path('coocurence', views.searchdbcooc_menu, name = 'searchdbcooc_menu'),


    path('legionella', views.legionella, name ='legionella'),
    path('legionella-result',views.legionella_result, name='legionella_result'),

    path('escherichia', views.escherichia, name='escherichia'),
    path('escherichia-result',views.escherichia_result, name='escherichia_result'),


    # path('api',views.cooc_list),
    # path('api_info/<str:gene1>+<str:gene2>',views.cooc_details),
    # path('api_class', views.CoocurenceAPIView.as_view()),
    # path('api_class_detail/<str:gene1>', views.CoocurenceListApiView.as_view()),
    path('api_cooc/<str:gene1>', views.CoocurenceGetResult.as_view()),
    # ESCHERICHIA
    path('esch-spec/<str:gene1>', views.EschSpecResult.as_view()),
    path('esch-str/<str:gene1>', views.EschStrResult.as_view()),
    path('esch-sws/<str:gene1>', views.EschSwsResult.as_view()),
    # LEGIONELLA
    path('leg-spec/<str:gene1>', views.LegSpecResult.as_view()),
    path('leg-str/<str:gene1>', views.LegStrResult.as_view()),
    path('leg-sws/<str:gene1>', views.LegSwsResult.as_view()),
]