from django.shortcuts import render,redirect
from django.http import HttpResponse
from scripts.colapsing_script import ColapsingSeq
from django.core.files.storage import FileSystemStorage
from scripts.streching3alignments import ThreeAlignmentColapser
from .models import ColapserDatabase, StretcherDatabase
from scripts.create_cron_task import CreateCronTaskStreching

def match3align(request):
    return render(request, 'tools/input/match_3_alignment.html')


def squezealign(request):
    return render(request, 'tools/input/colapsing_alignment.html')




def makeitsimple(request):
    context = {}
    #WINDOWS
    #linki = 'E:/project_site/final_site-project'
    #LINUX
    linki = '/home/djangoadmin/final_site-project'
    results_link = '/media/'
    
    if request.user.is_authenticated:
        
        if request.method =='POST':
            out_name = request.POST['out_name']
            uploaded_file = request.FILES['document']
            fs = FileSystemStorage()
            name= fs.save(uploaded_file.name, uploaded_file)
            context['url'] = fs.url(name)
            link_do_pliku = context['url']


            a = ColapsingSeq(multifasta_sequences = linki + link_do_pliku)
            output = a.Go()
            guide_to_file = a.CreateLink()
            
            
            link_ready = results_link+guide_to_file  
            user_id  = request.user.id
            query = ColapserDatabase(insert_file = name, user_id = user_id, out_time = 'NOW', link = link_ready,anal_name = out_name)
            query.save()

            return render(request, 'tools/output/colapsed.html', {'output':output, 'link_ready':link_ready})

    else:
         if request.method =='POST':
            out_name = request.POST['out_name']
            uploaded_file = request.FILES['document']
            fs = FileSystemStorage()
            name= fs.save(uploaded_file.name, uploaded_file)
            context['url'] = fs.url(name)
            link_do_pliku = context['url']


            a = ColapsingSeq(multifasta_sequences = linki + link_do_pliku)
            output = a.Go()
            guide_to_file = a.CreateLink()       
            
             
            link_ready = results_link+guide_to_file  
            user_id  = request.user.id
            query = ColapserDatabase(insert_file = name, user_id = 2, out_time = 'NEVER', link = link_ready,anal_name = out_name)
            query.save()



            return render(request, 'tools/output/colapsed.html', {'output':output, 'link_ready':link_ready})




def strechitout(request):
    #Skoro to jest slownik to mo¿na to za³atwiæ jednym a nie trzema
    context_master = {}
    context_slave1 = {}
    context_slave2 = {}
    linki = '/home/djangoadmin/final_site-project/media/'
    
    results_link = '/media/'
    if request.method =='POST':
        out_name = request.POST['out_name']
        uploaded_file_master = request.FILES['master']
        uploaded_file_slave1 = request.FILES['slave1']
        uploaded_file_slave2 = request.FILES['slave2']
        fs = FileSystemStorage()
        name_master = fs.save(uploaded_file_master.name, uploaded_file_master)
        name_slave1 = fs.save(uploaded_file_slave1.name, uploaded_file_slave1)
        name_slave2 = fs.save(uploaded_file_slave2.name, uploaded_file_slave2)
        context_master['url'] = fs.url(name_master)
        context_slave1['url'] = fs.url(name_slave1)
        context_slave2['url'] = fs.url(name_slave2)
        link_do_master = context_master['url']
        link_do_slave1 = context_slave1['url']
        link_do_slave2 = context_slave2['url']
        #########################################################################################################################
        create_task = CreateCronTaskStreching(name_master, name_slave1, name_slave2, out_name)
        
        pre_end = create_task.Task()
        end_end = pre_end.replace(' ','_')
        link_down = '/media/' + end_end +'.txt'
        
        #
        #a = ThreeAlignmentColapser(reference_multifasta = name_master , first_multifasta = name_slave1, second_multifasta = name_slave2)
        #a.Go()
        #guide_to_file = a.CreateDownloadableLink()
        
        
        ##########################################################################################################################
        user_id  = request.user.id
        
        
        #link_ready = results_link+guide_to_file

        query = StretcherDatabase(insert_file_master_master = name_master , insert_file_master_slave_one = name_slave1, insert_file_master_slave_two= name_slave2, user_id = user_id, out_time = end_end, link = link_down, anal_name = out_name)
        query.save()

    return redirect('dashboard')