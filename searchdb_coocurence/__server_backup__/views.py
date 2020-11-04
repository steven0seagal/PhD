from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from searchdb_coocurence.choices import cutoff_choices, colapsing_choices, colapsing_choices_escherichia
from .models import *

def searchdbcooc(request):

    return render(request, 'tools/input/coocurence_menu.html')


#
# def searchdbcooc_menu(request):
#
#     context = {
#         'cutoff_choices':cutoff_choices,
#         'colapsing_choices': colapsing_choices
#     }
#
#     return render(request, 'tools/input/coocurence.html',context)
#
# def searchresult(request):
#
#     colapsing  = request.GET['colapsing']
#
#     if colapsing == '':
#         queryset_list = Coocurence.objects.order_by('pvalue')
#
#         if 'gene1' in request.GET:
#             gene1 = request.GET['gene1']
#             if gene1:
#                 queryset_list = queryset_list.filter(gene1__icontains = gene1)
#         elif 'gene1' not in request.GET:
#             gene1 = ''
#
#         if 'gene2' in request.GET:
#             gene2 = request.GET['gene2']
#             if gene2:
#                 queryset_list = queryset_list.filter(gene2__icontains = gene2)
#         else:
#             gene2=''
#
#         if 'pvalue' in request.GET:
#             pvalue = request.GET['pvalue']
#             if pvalue:
#                 queryset_list = queryset_list.filter(pvalue__lte=pvalue)
#         else:
#             pvalue= ''
#
#
#     elif colapsing == 'Collapsed on species level':
#
#         queryset_list = ColapsedOnSpeciesLevel.objects.order_by('pvalue')
#
#         if 'gene1' in request.GET:
#             gene1 = request.GET['gene1']
#             if gene1:
#                 queryset_list = queryset_list.filter(gene1__icontains = gene1)
#         elif 'gene1' not in request.GET:
#             gene1 = ''
#
#         if 'gene2' in request.GET:
#             gene2 = request.GET['gene2']
#             if gene2:
#                 queryset_list = queryset_list.filter(gene2__icontains = gene2)
#         else:
#             gene2=''
#
#         if 'pvalue' in request.GET:
#             pvalue = request.GET['pvalue']
#             if pvalue:
#                 queryset_list = queryset_list.filter(pvalue__lte=pvalue)
#         else:
#             pvalue= ''
#
#     elif colapsing == 'Collapsed on Legionella strains':
#
#         queryset_list = ColapsedOnLegionellaStrains.objects.order_by('pvalue')
#
#         if 'gene1' in request.GET:
#             gene1 = request.GET['gene1']
#             if gene1:
#                 queryset_list = queryset_list.filter(gene1__icontains = gene1)
#         elif 'gene1' not in request.GET:
#             gene1 = ''
#
#         if 'gene2' in request.GET:
#             gene2 = request.GET['gene2']
#             if gene2:
#                 queryset_list = queryset_list.filter(gene2__icontains = gene2)
#         else:
#             gene2=''
#
#         if 'pvalue' in request.GET:
#             pvalue = request.GET['pvalue']
#             if pvalue:
#                 queryset_list = queryset_list.filter(pvalue__lte=pvalue)
#         else:
#             pvalue= ''
#
#     elif colapsing == 'Collapsed on species within Legionella':
#
#         queryset_list = ColapsedOnLegionellaStrainWithingSpecies.objects.order_by('pvalue')
#
#         if 'gene1' in request.GET:
#             gene1 = request.GET['gene1']
#             if gene1:
#                 queryset_list = queryset_list.filter(gene1__icontains = gene1)
#         elif 'gene1' not in request.GET:
#             gene1 = ''
#
#         if 'gene2' in request.GET:
#             gene2 = request.GET['gene2']
#             if gene2:
#                 queryset_list = queryset_list.filter(gene2__icontains = gene2)
#         else:
#             gene2=''
#
#         if 'pvalue' in request.GET:
#             pvalue = request.GET['pvalue']
#             if pvalue:
#                 queryset_list = queryset_list.filter(pvalue__lte=pvalue)
#         else:
#             pvalue= ''
#
#
#
#
#
#     page = request.GET.get('page',1)
#     paginator = Paginator(queryset_list, 100)
#
#     query = paginator.get_page(page)
#
#     context = {
#          'gene1':gene1,
#          'gene2':gene2,
#          'pvalue':pvalue,
#          'colapsing':colapsing,
#          'query':query,
#          'cutoff_choices':cutoff_choices,
#          'colapsing_choices': colapsing_choices,
#
#      }
#     return render(request, 'tools/output/coocurence_result_legionella.html' ,context)
#
#
#     #return render(request, 'tools/output/coocurence_result_legionella.html', context)




def legionella(request):

    context = {
        'cutoff_choices':cutoff_choices,
        'colapsing_choices': colapsing_choices
    }



    return render(request, 'tools/input/cocurence_legionella.html',context)


def legionella_result(request):
    colapsing = request.GET['colapsing']

    if colapsing == '':
        queryset_list = Coocurence.objects.order_by('pvalue')
        print(len(queryset_list))
        if 'gene1' in request.GET:
            gene1 = request.GET['gene1']
            if gene1:
                queryset_list = queryset_list.filter(gene1__icontains=gene1)
        elif 'gene1' not in request.GET:
            gene1 = ''

        if 'gene2' in request.GET:
            gene2 = request.GET['gene2']
            if gene2:
                queryset_list = queryset_list.filter(gene2__icontains=gene2)
        else:
            gene2 = ''

        if 'pvalue' in request.GET:
            pvalue = request.GET['pvalue']
            if pvalue:
                queryset_list = queryset_list.filter(pvalue__lte=pvalue)
        else:
            pvalue = ''

    elif colapsing == 'Collapsed on species level':

         queryset_list = ColapsedOnSpeciesLevel.objects.order_by('pvalue')

         if 'gene1' in request.GET:
             gene1 = request.GET['gene1']
             if gene1:
                 queryset_list = queryset_list.filter(gene1__icontains = gene1)
         elif 'gene1' not in request.GET:
             gene1 = ''

         if 'gene2' in request.GET:
             gene2 = request.GET['gene2']
             if gene2:
                 queryset_list = queryset_list.filter(gene2__icontains = gene2)
         else:
             gene2=''

         if 'pvalue' in request.GET:
             pvalue = request.GET['pvalue']
             if pvalue:
                 queryset_list = queryset_list.filter(pvalue__lte=pvalue)
         else:
             pvalue= ''

    elif colapsing == 'Collapsed on Legionella strains':

        queryset_list = ColapsedOnLegionellaStrains.objects.order_by('pvalue')

        if 'gene1' in request.GET:
            gene1 = request.GET['gene1']
            if gene1:
                queryset_list = queryset_list.filter(gene1__icontains=gene1)
        elif 'gene1' not in request.GET:
            gene1 = ''

        if 'gene2' in request.GET:
            gene2 = request.GET['gene2']
            if gene2:
                queryset_list = queryset_list.filter(gene2__icontains=gene2)
        else:
            gene2 = ''

        if 'pvalue' in request.GET:
            pvalue = request.GET['pvalue']
            if pvalue:
                queryset_list = queryset_list.filter(pvalue__lte=pvalue)
        else:
            pvalue = ''

    elif colapsing == 'Collapsed on species within Legionella':

        queryset_list = ColapsedOnLegionellaStrainWithingSpecies.objects.order_by('pvalue')

        if 'gene1' in request.GET:
            gene1 = request.GET['gene1']
            if gene1:
                queryset_list = queryset_list.filter(gene1__icontains=gene1)
        elif 'gene1' not in request.GET:
            gene1 = ''

        if 'gene2' in request.GET:
            gene2 = request.GET['gene2']
            if gene2:
                queryset_list = queryset_list.filter(gene2__icontains=gene2)
        else:
            gene2 = ''

        if 'pvalue' in request.GET:
            pvalue = request.GET['pvalue']
            if pvalue:
                queryset_list = queryset_list.filter(pvalue__lte=pvalue)
        else:
            pvalue = ''

    page = request.GET.get('page', 1)
    paginator = Paginator(queryset_list, 100)

    query = paginator.get_page(page)

    context = {
        'gene1': gene1,
        'gene2': gene2,
        'pvalue': pvalue,
        'colapsing': colapsing,
        'query': query,
        'cutoff_choices': cutoff_choices,
        'colapsing_choices': colapsing_choices,

    }
    print(len(context))
    return render(request, 'tools/output/coocurence_result_legionella.html', context)




def escherichia(request):

    context = {
        'cutoff_choices':cutoff_choices,
        'colapsing_choices': colapsing_choices_escherichia
    }


    return render(request, 'tools/input/cocurence_ecoli.html',context)

def escherichia_result(request):
    colapsing = request.GET['colapsing']

    if colapsing == '':
        queryset_list = Coocurence.objects.order_by('pvalue')

        if 'gene1' in request.GET:
            gene1 = request.GET['gene1']
            if gene1:
                queryset_list = queryset_list.filter(gene1__icontains=gene1)
        elif 'gene1' not in request.GET:
            gene1 = ''

        if 'gene2' in request.GET:
            gene2 = request.GET['gene2']
            if gene2:
                queryset_list = queryset_list.filter(gene2__icontains=gene2)
        else:
            gene2 = ''

        if 'pvalue' in request.GET:
            pvalue = request.GET['pvalue']
            if pvalue:
                queryset_list = queryset_list.filter(pvalue__lte=pvalue)
        else:
            pvalue = ''


    elif colapsing == 'Collapsed on species level':

        queryset_list = ColapsedOnEscherichiaSpeciesLevel.objects.order_by('pvalue')

        if 'gene1' in request.GET:
            gene1 = request.GET['gene1']
            if gene1:
                queryset_list = queryset_list.filter(gene1__icontains=gene1)
        elif 'gene1' not in request.GET:
            gene1 = ''

        if 'gene2' in request.GET:
            gene2 = request.GET['gene2']
            if gene2:
                queryset_list = queryset_list.filter(gene2__icontains=gene2)
        else:
            gene2 = ''

        if 'pvalue' in request.GET:
            pvalue = request.GET['pvalue']
            if pvalue:
                queryset_list = queryset_list.filter(pvalue__lte=pvalue)
        else:
            pvalue = ''

    elif colapsing == 'Collapsed on Escherichia strains':

        queryset_list = ColapsedOnEscherichiaStrains.objects.order_by('pvalue')

        if 'gene1' in request.GET:
            gene1 = request.GET['gene1']
            if gene1:
                queryset_list = queryset_list.filter(gene1__icontains=gene1)
        elif 'gene1' not in request.GET:
            gene1 = ''

        if 'gene2' in request.GET:
            gene2 = request.GET['gene2']
            if gene2:
                queryset_list = queryset_list.filter(gene2__icontains=gene2)
        else:
            gene2 = ''

        if 'pvalue' in request.GET:
            pvalue = request.GET['pvalue']
            if pvalue:
                queryset_list = queryset_list.filter(pvalue__lte=pvalue)
        else:
            pvalue = ''

    elif colapsing == 'Collapsed on species within Escherichia':

        queryset_list = ColapsedOnEscherichiaStrainWithingSpecies.objects.order_by('pvalue')

        if 'gene1' in request.GET:
            gene1 = request.GET['gene1']
            if gene1:
                queryset_list = queryset_list.filter(gene1__icontains=gene1)
        elif 'gene1' not in request.GET:
            gene1 = ''

        if 'gene2' in request.GET:
            gene2 = request.GET['gene2']
            if gene2:
                queryset_list = queryset_list.filter(gene2__icontains=gene2)
        else:
            gene2 = ''

        if 'pvalue' in request.GET:
            pvalue = request.GET['pvalue']
            if pvalue:
                queryset_list = queryset_list.filter(pvalue__lte=pvalue)
        else:
            pvalue = ''

    page = request.GET.get('page', 1)
    paginator = Paginator(queryset_list, 100)

    query = paginator.get_page(page)

    context = {
        'gene1': gene1,
        'gene2': gene2,
        'pvalue': pvalue,
        'colapsing': colapsing,
        'query': query,
        'cutoff_choices': cutoff_choices,
        'colapsing_choices': colapsing_choices_escherichia,

    }
    return render(request, 'tools/output/coocurence_result_escherichia.html', context)


from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from .models import Coocurence
from .serializers import *
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

@csrf_exempt
def coocurence_list(request):

    if request.method =="GET":
        coocurences = Coocurence.objects.all()
        serializer = CoocurenceSerializer(coocurences, many = True)
        return JsonResponse(serializer.data, safe = False)
    elif request.method =="POST":
        data = JSONParser().parse(request)
        serializer = CoocurenceSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def coocurence_details(request,gene1,gene2):

    try:
        coocurence = Coocurence.objects.get(gene1=gene1, gene2=gene2)
    except Coocurence.DoesNotExist:
        return HttpResponse(status=404)

    if request.method =="GET":
        serializer = CoocurenceSerializer(coocurence)
        return JsonResponse(serializer.data)

    elif request.method =="PUT":
        data = JSONParser().parse(request)
        serializer = CoocurenceSerializer(coocurence, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == "DELETE":
        coocurence.delete()
        return HttpResponse(status=204)

@api_view(['GET', 'POST'])
def cooc_list(request):

    if request.method =="GET":
        coocurences = Coocurence.objects.all()

        serializer = CoocurenceSerializer(coocurences, many = True)
        return Response(serializer.data)
    elif request.method =="POST":
        serializer = CoocurenceSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET","PUT","DELETE"])
def cooc_details(request,gene1,gene2):

    try:
        coocurence = Coocurence.objects.get(gene1=gene1, gene2=gene2)

    except Coocurence.DoesNotExist:
        return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

    if request.method =="GET":
        serializer = CoocurenceSerializer(coocurence)
        return Response(serializer.data)

    elif request.method =="PUT":
        serializer = CoocurenceSerializer(coocurence, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        coocurence.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CoocurenceAPIView(APIView):

    def get(self, request):
        coocurences = Coocurence.objects.all()
        serializer = CoocurenceSerializer(coocurences, many = True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CoocurenceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CoocurenceListApiView(APIView):

    def get_object(self,gene1):

        try:
            return Coocurence.objects.get(gene1=gene1)
        except Coocurence.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    def get(self, request,gene1):
        coocurence = self.get_object(gene1)
        serializer = CoocurenceSerializer(coocurence)
        return Response(serializer.data)

    def put(self,request,gene1, gene2):
        coocurence = self.get_object(gene1, gene2)
        serializer = CoocurenceSerializer(coocurence, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,gene1, gene2):

        coocurence = self.get_object(gene1, gene2)
        coocurence.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CoocurenceGetResult(APIView):

    def get(self, request,gene1):

        querylist = Coocurence.objects.all()
        coocurences = querylist.filter(gene1__icontains=gene1)
        serializer = CoocurenceSerializer(coocurences, many = True)
        print(len(querylist))
        return Response(serializer.data)

# LEGIONELLA

class LegSpecResult(APIView):

    def get(self, request,gene1):

        querylist = ColapsedOnSpeciesLevel.objects.all()
        coocurences = querylist.filter(gene1__icontains=gene1)
        serializer = LegionellaSpecSerializer(coocurences, many = True)
        print(len(querylist))
        return Response(serializer.data)

class LegStrResult(APIView):

    def get(self, request,gene1):

        querylist = ColapsedOnLegionellaStrains.objects.all()
        coocurences = querylist.filter(gene1__icontains=gene1)
        serializer = LegionellaStrSerializer(coocurences, many = True)
        print(len(querylist))
        return Response(serializer.data)

class LegSwsResult(APIView):

    def get(self, request,gene1):

        querylist = ColapsedOnLegionellaStrainWithingSpecies.objects.all()
        coocurences = querylist.filter(gene1__icontains=gene1)
        serializer = LegionellaSwsSerializer(coocurences, many = True)
        print(len(querylist))
        return Response(serializer.data)

# ESCHERICHIA
class EschSpecResult(APIView):

    def get(self, request,gene1):

        querylist = ColapsedOnEscherichiaSpeciesLevel.objects.all()
        coocurences = querylist.filter(gene1__icontains=gene1)
        serializer = EscherichiaSpecSerializer(coocurences, many = True)
        print(len(querylist))
        return Response(serializer.data)

class EschStrResult(APIView):

    def get(self, request,gene1):

        querylist = ColapsedOnEscherichiaStrains.objects.all()
        coocurences = querylist.filter(gene1__icontains=gene1)
        serializer = EscherichiaStrSerializer(coocurences, many = True)
        print(len(querylist))
        return Response(serializer.data)

class EschSwsResult(APIView):

    def get(self, request,gene1):

        querylist = ColapsedOnEscherichiaStrainWithingSpecies.objects.all()
        coocurences = querylist.filter(gene1__icontains=gene1)
        serializer = EscherichiaSwsSerializer(coocurences, many = True)
        print(len(querylist))
        return Response(serializer.data)

