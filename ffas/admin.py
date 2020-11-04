from django.contrib import admin

# Register your models here.

from .models import FFASDatabase

class FFASDatabaseAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'analysis_name')
    list_display_links = ('user_id','analysis_name')
    list_per_page = 25
    search_fields = ('user_id','analysis_name')


admin.site.register(FFASDatabase, FFASDatabaseAdmin)