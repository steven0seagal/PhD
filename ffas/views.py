from django.shortcuts import render, redirect
from .models import FFASDatabase
from django.core.files.storage import FileSystemStorage
from django.utils.datastructures import MultiValueDictKeyError
import random
import string
from accounts.models import QueForFfas

def ffas_main(request):
    title = "FFAS03"
    return render(request, 'tools/input/ffas_start.html')

def ffas_analysis(request):
    out_name = request.POST['out_name']
    user_id = request.user.id

    context = {}
    uploaded_file = request.FILES['input']
    fs = FileSystemStorage()
    name = fs.save(uploaded_file.name, uploaded_file)
    context['url'] = fs.url(name)
    server_results_file = "/media/"
    server_filestore = "/media/results/"
    link_do_pliku = context['url']


    letters = string.ascii_lowercase
    end_end = ''.join(random.choice(letters) for i in range(10))
    link_down = '/media/results/' + end_end + '.ff'
    db_initial = 'profile'

    ready_script = '/home/djangoadmin/final_site_venv/bin/python3 /home/djangoadmin/final_site-project/scripts/execute_order_101.py ' \
                           '{0} {1} {2} '.format(db_initial, link_do_pliku, link_down)


    boxes = ['PDB', 'SCOP', 'PFAM', 'Hsapiens', 'COG','VFDB','VFdbcustom']
    databases = ['profile']
    for box in boxes:
        try:
            request.POST[box+"_box"]
            databases.append(box)
        except MultiValueDictKeyError :
            continue
    if len(databases) > 1:
        for db in databases[1:]:
            new_file_url = link_down
            new_result_file = '/media/results/' + end_end + "_" + db.lower() + ".fft"
            ready_script += " && /home/djangoadmin/final_site_venv/bin/python3 /home/djangoadmin/final_site-project" \
                            "/scripts/execute_order_101.py {0} {1} {2} ".format(db, new_file_url, new_result_file )

    job = QueForFfas(user_id = user_id, status = 'Queue', analysis_name = out_name, script = ready_script, tool = "FFAS", )
    job.save()



    return redirect('dashboard')