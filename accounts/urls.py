from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login, name = 'login'),
    # path('register', views.register, name = 'register'),
    path('logout', views.logout, name = 'logout'),
    path('dashboard', views.dashboard, name = 'dashboard'),
    path('dashboard/neighborhood',views.dashboard_neigh, name = 'dash_neigh'),
    path('dashboard/ffas',views.dashboard_ffas, name = 'dash_ffas'),
    path('dashboard/colapser',views.dashboard_collaps, name = 'dash_collaps'),
    path('dashboard/stretcher',views.dashboard_stretch, name = 'dash_stretch'),
    path('dashboard/hhmer',views.dashboard_hmmer, name = 'dash_hmmer'),
    path('dashboard/human-prot',views.dashboard_pch, name = 'dash_human'),

]