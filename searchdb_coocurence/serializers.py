from rest_framework import serializers
from .models import *




class CoocurenceSerializer(serializers.ModelSerializer):

    class Meta:

        model = Coocurence
        fields = ['gene1', 'gene2', 'together','first_only','second_only','neither','pvalue']

# LEGIONELLA
class LegionellaSpecSerializer(serializers.ModelSerializer):

    class Meta:

        model = ColapsedOnSpeciesLevel
        fields = ['gene1', 'gene2', 'together','first_only','second_only','neither','pvalue']

class LegionellaStrSerializer(serializers.ModelSerializer):

    class Meta:

        model = ColapsedOnLegionellaStrains
        fields = ['gene1', 'gene2', 'together','first_only','second_only','neither','pvalue']

class LegionellaSwsSerializer(serializers.ModelSerializer):

    class Meta:

        model = ColapsedOnLegionellaStrainWithingSpecies
        fields = ['gene1', 'gene2', 'together','first_only','second_only','neither','pvalue']

# ESCHERICHIA
class EscherichiaSpecSerializer(serializers.ModelSerializer):

    class Meta:

        model = ColapsedOnEscherichiaSpeciesLevel
        fields = ['gene1', 'gene2', 'together','first_only','second_only','neither','pvalue']

class EscherichiaStrSerializer(serializers.ModelSerializer):

    class Meta:

        model = ColapsedOnEscherichiaStrains
        fields = ['gene1', 'gene2', 'together','first_only','second_only','neither','pvalue']

class EscherichiaSwsSerializer(serializers.ModelSerializer):

    class Meta:

        model = ColapsedOnEscherichiaStrainWithingSpecies
        fields = ['gene1', 'gene2', 'together','first_only','second_only','neither','pvalue']


