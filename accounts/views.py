from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from neighborhood_analysis.models import NeighAnalyzDatabase
from alignments_tools.models import ColapserDatabase, StretcherDatabase
from hmmer_fixer.models import HmmerFixerDatabase
from datetime import datetime
from scripts import check_link_existance
from .models import PeekUserData
from .models import CompleteQueue
from .models import QueForFfas
from .models import QueForPCH
from scripts.data_from_script import feedMe
from scripts.check_link_existance import new_file_checker
import os
import datetime

def register(request):
    if request.method == "POST":
        #Get form values
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        #Check if password match
        if password == password2:
            #check username
            if User.objects.filter(username=username).exists():
                messages.error(request, 'That username is taken')
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'That email is being used')
                    return redirect('register')
                else:
                    user = User.objects.create_user(username=username,email=email, password=password, first_name=first_name, last_name=last_name)
                    query = PeekUserData(username=username,email=email, password=password, first_name=first_name, last_name=last_name)
                    #Login after register 
                    # auth.login(request, user)
                    # messages.success(request, 'You are now registered')
                    # return redirect('index')
                    user.save()
                    query.save()
                    messages.success(request, 'You are now registered and can log in ')
                    return redirect('login')
        else:
            messages.error(request, 'Passwords do not match')
            return redirect('register')
    else:
        return render(request, 'user_panel/register.html')

def login(request):
    if request.method == "POST":
        username=request.POST['username']
        password=request.POST['password']

        user = auth.authenticate(username=username, password=password)
       
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now logged in')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('login')
    else:
        return render(request, 'user_panel/login.html')

def logout(request):
    if request.method == "POST":
        auth.logout(request)
        messages.success(request, 'You are now logout')

        return redirect('login')

def dashboard_neigh(request):

    current_time = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    all_jobs = CompleteQueue.objects.order_by('-id').filter(user_id=request.user.id)
    neigh_domain_jobs = feedMe(all_jobs, 'NA')
    neigh_gene_jobs = feedMe(all_jobs, 'NAG')
    neigh_domain_family_jobs = feedMe(all_jobs, "NAF")
    neigh_domain_jobs_all = feedMe(all_jobs, "NAD")
    neigh_jobs = neigh_domain_jobs + neigh_gene_jobs + neigh_domain_family_jobs + neigh_domain_jobs_all
    neigh_jobs_sorted = sorted(neigh_jobs, key=lambda k: k['id'], reverse=True)

    context = {
        'current_time': current_time,
        'neigh_example_jobs': neigh_jobs_sorted,
    }
    return render(request, 'user_panel/dashboard_neigh.html',context)

def dashboard_ffas(request):

    current_time = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    ffas_database_jobs = QueForFfas.objects.order_by('-id').filter(user_id=request.user.id)
    ffas_jobs = feedMe(ffas_database_jobs, 'FFAS')

    context = {
        'current_time': current_time,
        'ffas_jobs': ffas_jobs,
    }
    return render(request, 'user_panel/dashboard_ffas.html', context)

def dashboard_stretch(request):
    
    all_jobs = CompleteQueue.objects.order_by('-id').filter(user_id = request.user.id)

    current_time = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    stretch_example_jobs = feedMe(all_jobs,'M3A')

    context = {
	    'current_time' : current_time,
        'stretch_example_jobs' :stretch_example_jobs,

    }
    return render(request, 'user_panel/dashboard_stretch.html', context)

def dashboard_collaps(request):
    current_time = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    colapser_jobs = ColapserDatabase.objects.order_by('-id').filter(user_id = request.user.id)
    checked_data_colapser = check_link_existance.link_ready(colapser_jobs)

    context = {
	    'current_time' : current_time,
        'checked_data_colapser' : checked_data_colapser,
    }

    return render(request, 'user_panel/dashboard_colaps.html', context)

def dashboard_hmmer(request):

    current_time = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    hmmer_jobs = HmmerFixerDatabase.objects.order_by('-id').filter(user_id = request.user.id)
    checked_hmmer_jobs = check_link_existance.link_ready(hmmer_jobs)

    context = {
        'current_time': current_time,
        'checked_hmmer_jobs': checked_hmmer_jobs,
    }
    return render(request, 'user_panel/dashboard_hmmer.html', context)

def dashboard_pch(request):

    current_time = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    pch_database_jobs = QueForPCH.objects.order_by('-id').filter(user_id = request.user.id)
    pch_jobs = feedMe(pch_database_jobs,'PCH')

    context = {
	    'current_time' : current_time,
        'pch_jobs':pch_jobs,
    }

    return render(request, 'user_panel/dashboard_pch.html', context)

def dashboard(request):
    current_time = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


    colapser_jobs = ColapserDatabase.objects.order_by('-id').filter(user_id = request.user.id)
    stretcher_jobs = StretcherDatabase.objects.order_by('-id').filter(user_id = request.user.id)
    hmmer_jobs = HmmerFixerDatabase.objects.order_by('-id').filter(user_id = request.user.id)
    all_jobs = CompleteQueue.objects.order_by('-id').filter(user_id = request.user.id)
    ffas_database_jobs = QueForFfas.objects.order_by('-id').filter(user_id = request.user.id)
    pch_database_jobs = QueForPCH.objects.order_by('-id').filter(user_id = request.user.id)

    neigh_domain_jobs = feedMe(all_jobs, 'NA')
    neigh_gene_jobs = feedMe(all_jobs,'NAG')
    neigh_domain_family_jobs = feedMe(all_jobs,"NAF")
    neigh_domain_jobs_all = feedMe(all_jobs, "NAD")
    neigh_jobs = neigh_domain_jobs + neigh_gene_jobs +neigh_domain_family_jobs+neigh_domain_jobs_all
    neigh_jobs_sorted = sorted(neigh_jobs, key=lambda k: k['id'],reverse=True)
    stretch_example_jobs = feedMe(all_jobs,'M3A')
    ffas_jobs = feedMe(ffas_database_jobs, 'FFAS')
    pch_jobs = feedMe(pch_database_jobs,'PCH')

    checked_data_colapser = check_link_existance.link_ready(colapser_jobs)
    checked_strecher_jobs = check_link_existance.link_ready(stretcher_jobs)
    checked_hmmer_jobs = check_link_existance.link_ready(hmmer_jobs)


    context = {
	    'current_time' : current_time,
        'stretch_example_jobs' :stretch_example_jobs,
        'checked_data_colapser' : checked_data_colapser,
        'checked_hmmer_jobs' : checked_hmmer_jobs,
        'neigh_example_jobs':neigh_jobs_sorted,
        'ffas_jobs':ffas_jobs,
        'pch_jobs':pch_jobs,
    }

#    context = {
#        'neigh_jobs' : neigh_jobs,
#        'colapser_jobs' : colapser_jobs,
#        'stretcher_jobs' : stretcher_jobs,
#	    'current_time' : current_time,
#        'hmmer_jobs' : hmmer_jobs,
#    }
    return render(request, 'user_panel/dashboard.html',context)