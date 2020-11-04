from django.contrib import admin

# Register your models here.
from .models import *

class CoocurenceAdmin(admin.ModelAdmin):
    list_display = ('id', 'gene1', 'gene2')
    list_display_links = ('id','gene1', 'gene2' ) 
    
    list_per_page = 100
    search_fields = ('gene1', 'gene2', 'pvalue')
admin.site.register(Coocurence, CoocurenceAdmin )


# LEGIONELLA

class ColapsedOnSpeciesLevelAdmin(admin.ModelAdmin):
    list_display = ('id', 'gene1', 'gene2')
    list_display_links = ('id','gene1', 'gene2' ) 
    
    list_per_page = 100
    search_fields = ('gene1', 'gene2', 'pvalue')
admin.site.register(ColapsedOnSpeciesLevel, ColapsedOnSpeciesLevelAdmin )

class ColapsedOnLegionellaStrainsAdmin(admin.ModelAdmin):
    list_display = ('id', 'gene1', 'gene2')
    list_display_links = ('id','gene1', 'gene2' ) 
    
    list_per_page = 100
    search_fields = ('gene1', 'gene2', 'pvalue')
admin.site.register(ColapsedOnLegionellaStrains, ColapsedOnLegionellaStrainsAdmin )

class ColapsedOnLegionellaStrainWithingSpeciesAdmin(admin.ModelAdmin):
    list_display = ('id', 'gene1', 'gene2')
    list_display_links = ('id','gene1', 'gene2' ) 
    
    list_per_page = 100
    search_fields = ('gene1', 'gene2', 'pvalue')
admin.site.register(ColapsedOnLegionellaStrainWithingSpecies, ColapsedOnLegionellaStrainWithingSpeciesAdmin )

#ESCHERICHIA

class ColapsedOnEscherichiaSpeciesLevelAdmin(admin.ModelAdmin):
    list_display = ('id', 'gene1', 'gene2')
    list_display_links = ('id','gene1', 'gene2' )

    list_per_page = 100
    search_fields = ('gene1', 'gene2', 'pvalue')
admin.site.register(ColapsedOnEscherichiaSpeciesLevel, ColapsedOnEscherichiaSpeciesLevelAdmin )

class ColapsedOnEscherichiaStrainsAdmin(admin.ModelAdmin):
    list_display = ('id', 'gene1', 'gene2')
    list_display_links = ('id','gene1', 'gene2' )

    list_per_page = 100
    search_fields = ('gene1', 'gene2', 'pvalue')
admin.site.register(ColapsedOnEscherichiaStrains, ColapsedOnEscherichiaStrainsAdmin )

class ColapsedOnEscherichiaStrainWithingSpeciesAdmin(admin.ModelAdmin):
    list_display = ('id', 'gene1', 'gene2')
    list_display_links = ('id','gene1', 'gene2' )

    list_per_page = 100
    search_fields = ('gene1', 'gene2', 'pvalue')
admin.site.register(ColapsedOnEscherichiaStrainWithingSpecies, ColapsedOnEscherichiaStrainWithingSpeciesAdmin )
