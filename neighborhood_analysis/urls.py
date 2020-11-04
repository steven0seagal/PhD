from django.urls import path
from . import views

urlpatterns = [
    path('', views.neighana_menu, name = 'neighana_menu'),

    path('pfam_domain',views.neighana, name = 'neighana'),
    path('gene', views.geneana, name = 'geneana'),
    path('pfam_domain_fam', views.neighana_fam, name='neighana_fam'),
    path('pfam_domain_all', views.neighana_all, name='neighana_all'),

    path('count_from_domain', views.count_from_domain, name = 'count_from_domain'),
    path('count_from_gene', views.count_from_gene, name='count_from_gene'),
    path('count_from_domain_family', views.count_from_domain_family, name='count_from_domain_family'),
    path('count_from_domain_all', views.count_from_domain_all, name='count_from_domain_all'),
]