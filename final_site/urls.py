"""final_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('mainsite.urls')),
    path('accounts/', include('accounts.urls')),
    path('alignments_tools/', include('alignments_tools.urls')),
    path('neighborhood_analysis/', include('neighborhood_analysis.urls')),
    path('news/', include('news.urls')),
    path('searchdb_coocurence/', include('searchdb_coocurence.urls')),
    path('hmmer_fixer/', include('hmmer_fixer.urls')),
    path('admin/', admin.site.urls),
    path('ffas/',include('ffas.urls')),
    path('accounts2/', include('allauth.urls')),
] + static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)
