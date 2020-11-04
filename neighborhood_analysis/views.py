from django.shortcuts import render, redirect
from django.http import HttpResponse
from accounts.models import CompleteQueue
from .models import NeighAnalyzDatabase
from scripts.create_cron_task import CreateCronTaskNeighborhood
import random
import string
from scripts.PfamValidate import PfamValidator
from scripts.pfam_input import retype_domain, check_if_domain_can_be_reachable
from django.core.files.storage import FileSystemStorage
import json


def neighana_menu(request):
    return (render(request, 'tools/input/neighborhood_analyzer_menu.html'))


def geneana(request):
    return (render(request, 'tools/input/neighborhood_analyzer_gene.html'))


def neighana(request):
    return render(request, 'tools/input/neighborhood_analyzer_domain.html')


def neighana_fam(request):
    return render(request, 'tools/input/neighborhood_analyzer_domain_fam.html')


def neighana_all(request):
    return render(request, 'tools/input/neighborhood_analyzer_domain_all.html')

# NA
def count_from_domain(request):
    #    fulltext = request.GET['fulltext']
    pfam_domain = request.GET['pfam_domain']
    range_search = request.GET['range_search']
    cut_off = request.GET['cut_off']
    database_taxa = request.GET['database_taxa']
    strand_select = request.GET['strand_select']
    out_name = request.GET['out_name']
    test_correction = request.GET['test_correction']
    # out_time = '12:34:56.789012'
    user_id = request.user.id
    skip_negative = "yes"

    pfam = PfamValidator(pfam_domain)
    pfam_value = pfam.Validate()
    domain_for_database, domain_to_search = retype_domain(pfam_domain)

    if pfam_value is True:
        if check_if_domain_can_be_reachable(database_taxa, domain_to_search) is True:
            letters = string.ascii_lowercase
            end_end = ''.join(random.choice(letters) for i in range(15))
            link_down = '/media/results/' + end_end + '.txt'

            ############################################################################################################
            # Local
            # ready_script ='python3 /mnt/d/45.76.38.24/final_site-project/scripts/execute_order_66.py {} {} {} ' \
            #              '{} {} {} {} {}'.format(domain_to_search ,range_search, database_taxa, cut_off, test_correction,
            #                                 strand_select, link_down, skip_negative)
            ############################################################################################################
            # Vultr
            ready_script = '/home/djangoadmin/final_site_venv/bin/python3 /home/djangoadmin/final_site-project/scripts/execute_order_66.py ' \
                           '{} {} {} {} {} {} {} {}'.format(domain_to_search, range_search, database_taxa, cut_off,
                                                         test_correction, strand_select, link_down, skip_negative)
            ############################################################################################################

            job = CompleteQueue(user_id=user_id, tool='NA', status='Queue', analysis_name=out_name,
                                script=ready_script, file=link_down)
            job.save()

            return redirect('dashboard')
        else:
            return render(request, 'tools/error/heavy_calculation.html')
    else:
        return render(request, 'tools/error/wrong_pfam.html')

# NAF
def count_from_domain_family(request):
    pfam_domain = request.GET['pfam_domain']
    range_search = request.GET['range_search']
    cut_off = request.GET['cut_off']
    database_taxa = request.GET['database_taxa']
    strand_select = request.GET['strand_select']
    out_name = request.GET['out_name']
    test_correction = request.GET['test_correction']
    user_id = request.user.id
    skip_negative = "no"
    pfam = PfamValidator(pfam_domain)
    pfam_value = pfam.Validate()
    domain_for_database, domain_to_search = retype_domain(pfam_domain)

    letters = string.ascii_lowercase
    end_end = ''.join(random.choice(letters) for i in range(15))

    link_down = '/media/results/' + end_end + '.txt'

    ####################################################################################################################
    # VULTR
    with open('/home/djangoadmin/final_site-project/important_files/database.json', "r") as handler:
    ####################################################################################################################
    # LOCAL
    # with open('/mnt/d/45.76.38.24/final_site-project/important_files/database.json', "r") as handler:
    ####################################################################################################################

        taxonomy = json.load(handler)
    files_for_analysis = []
    if pfam_value == True:

        genus_database = list(taxonomy[database_taxa].keys())
        ready_script=""

        for genus in genus_database:
            new_tax= "_".join(genus.split(' '))
            files_for_analysis.append(new_tax)
            temp_data_link = '/media/results/temp/' + new_tax
            ############################################################################################################
            # VULTR
            ready_script += '/home/djangoadmin/final_site_venv/bin/python3 /home/djangoadmin/final_site-project/scripts/execute_order_66.py ' \
                            '{} {} {} {} {} {} {} {} && '.format(domain_to_search, range_search, new_tax, 'none',
                                                              test_correction, strand_select, temp_data_link, skip_negative)
            ############################################################################################################
            # LOCAL
            # ready_script += ' python3 /mnt/d/45.76.38.24/final_site-project/scripts/execute_order_66.py {} {} {} {} {} ' \
            #                 '{} {} {} && '. format(domain_to_search, range_search, new_tax, 'none',test_correction,
            #                                        strand_select, temp_data_link, skip_negative)
            ############################################################################################################

        ################################################################################################################
        # VULTR
        ready_script += '/home/djangoadmin/final_site_venv/bin/python3 /home/djangoadmin/final_site-project/scripts/execute_order_96.py ' \
                        '{} {} {} {}'.format(cut_off, link_down, database_taxa, ",".join(files_for_analysis))
        ################################################################################################################
        # LOCAL
        # ready_script += 'python3 /mnt/d/45.76.38.24/final_site_venv/bin/python3 /home/djangoadmin/final_site-project/' \
        #                 'scripts/execute_order_96.py {} {} {} {}'.format(cut_off, link_down, database_taxa, ",".join(files_for_analysis))
        ################################################################################################################
        # print(",".join(files_for_analysis))

        job = CompleteQueue(user_id=user_id, tool='NAF', status='Queue', analysis_name=out_name,
                            script=ready_script, file=link_down)
        job.save()

        return redirect('dashboard')

    else:
        return render(request, 'tools/error/wrong_pfam.html')

# NAG
def count_from_gene(request):
    # file upload
    if request.method == 'POST':
        context = {}
        uploaded_file = request.FILES['gene_list']
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        context['url'] = fs.url(name)
        link_do_pliku = context['url']

    range_search = request.POST['range_search']
    cut_off = request.POST['cut_off']

    strand_select = request.POST['strand_select']
    out_name = request.POST['out_name']
    test_correction = request.POST['test_correction']
    user_id = request.user.id

    letters = string.ascii_lowercase
    end_end = ''.join(random.choice(letters) for i in range(15))
    link_down = '/media/results/' + end_end + '.txt'

    ####################################################################################################################
    # VULTR
    ready_script = '/home/djangoadmin/final_site_venv/bin/python3 /home/djangoadmin/final_site-project/scripts/execute_order_99.py ' \
                   '{} {} {} {} {} {} {}'.format(link_do_pliku, range_search, "Whole_database", cut_off,
                                                 test_correction, strand_select, link_down)
    ####################################################################################################################
    # LOCAL
    # ready_script = 'python3 /mnt/d/45.76.38.24/final_site-project/scripts/execute_order_99.py {} {} {} {} {} {} ' \
    #                '{}'.format(link_do_pliku, range_search, "Whole_database", cut_off,test_correction, strand_select, link_down)
    ####################################################################################################################
    job = CompleteQueue(user_id=user_id, tool='NAG', status='Queue', analysis_name=out_name,
                        script=ready_script, file=link_down)
    job.save()

    return redirect('dashboard')

# NAA
def count_from_domain_all(request):

    pfam_domain = request.GET['pfam_domain']
    range_search = request.GET['range_search']
    cut_off = request.GET['cut_off']
    strand_select = request.GET['strand_select']
    out_name = request.GET['out_name']
    test_correction = request.GET['test_correction']
    user_id = request.user.id
    method_average = request.GET["method_average"]

    if method_average == "no":
        database_taxa = "all_genomes"
        skip_negative = "yes"
        pfam = PfamValidator(pfam_domain)
        pfam_value = pfam.Validate()
        domain_for_database, domain_to_search = retype_domain(pfam_domain)

        if pfam_value is True:

            if check_if_domain_can_be_reachable(database_taxa, domain_to_search) is True:
                letters = string.ascii_lowercase
                end_end = ''.join(random.choice(letters) for i in range(15))
                link_down = '/media/results/' + end_end + '.txt'

                ########################################################################################################
                # Local
                # ready_script ='python3 /mnt/d/45.76.38.24/final_site-project/scripts/execute_order_66.py {} {} {} ' \
                #              '{} {} {} {} '.format(domain_to_search ,range_search, database_taxa, cut_off, test_correction,
                #                                 strand_select, link_down)
                ########################################################################################################
                # Vultr
                ready_script = '/home/djangoadmin/final_site_venv/bin/python3 /home/djangoadmin/final_site-project/scripts/execute_order_66.py ' \
                               '{} {} {} {} {} {} {} {}'.format(domain_to_search, range_search, database_taxa, cut_off,
                                                             test_correction, strand_select, link_down, skip_negative)
                ########################################################################################################

                job = CompleteQueue(user_id=user_id, tool='NAD', status='Queue', analysis_name=out_name,
                                    script=ready_script, file=link_down)
                job.save()
                return redirect('dashboard')
            else:
                return render(request, 'tools/error/heavy_calculation.html')
        else:
            return render(request, 'tools/error/wrong_pfam.html')
    elif method_average != "no":
        skip_negative = "no"
        database_taxa = "all_genomes"
        pfam = PfamValidator(pfam_domain)
        pfam_value = pfam.Validate()
        domain_for_database, domain_to_search = retype_domain(pfam_domain)

        if pfam_value is True:

            if check_if_domain_can_be_reachable(database_taxa, domain_to_search) is True:
                letters = string.ascii_lowercase
                end_end = ''.join(random.choice(letters) for i in range(15))
                link_down = '/media/results/' + end_end + '.txt'

                # GET NAMES OF ORGANISMS GROUPS

                if method_average == "genus":

                    ####################################################################################################
                    # VULTR
                    with open('/home/djangoadmin/final_site-project/important_files/genus_level.json', "r") as handler:
                    ####################################################################################################
                    # LOCAL
                    # with open('/mnt/d/45.76.38.24/final_site-project/important_files/genus_level.json', "r") as handler:
                        taxonomy = json.load(handler)
                    ####################################################################################################

                elif method_average == "family":
                    ####################################################################################################
                    # VULTR
                    with open('/home/djangoadmin/final_site-project/important_files/family_level.json', "r") as handler:
                    ####################################################################################################
                    # LOCAL
                    # with open('/mnt/d/45.76.38.24/final_site-project/important_files/family_level.json', "r") as handler:
                        taxonomy = json.load(handler)
                    ####################################################################################################

                elif method_average == "order":
                    ####################################################################################################
                    # VULTR
                    with open('/home/djangoadmin/final_site-project/important_files/order_level.json', "r") as handler:
                    ####################################################################################################
                    # LOCAL
                    # with open('/mnt/d/45.76.38.24/final_site-project/important_files/order_level.json', "r") as handler:
                        taxonomy = json.load(handler)
                    ####################################################################################################

                elif method_average == "class":
                    ####################################################################################################
                    # VULTR
                    with open('/home/djangoadmin/final_site-project/important_files/class_level.json', "r") as handler:
                    ####################################################################################################
                    # LOCAL
                    # with open('/mnt/d/45.76.38.24/final_site-project/important_files/class_level.json', "r") as handler:
                        taxonomy = json.load(handler)
                    ####################################################################################################

                elif method_average == "phylum":
                    ####################################################################################################
                    # VULTR
                    with open('/home/djangoadmin/final_site-project/important_files/phylum_level.json', "r") as handler:
                    ####################################################################################################
                    # LOCAL
                    # with open('/mnt/d/45.76.38.24/final_site-project/important_files/phylum_level.json', "r") as handler:
                        taxonomy = json.load(handler)
                    ####################################################################################################
                genus_database = list(taxonomy.keys())

                ready_script = ""

                files_for_analysis = []

                for genus in genus_database:
                    new_tax = "_".join(genus.split(' '))
                    files_for_analysis.append(new_tax)
                    temp_data_link = '/media/results/temp/' + new_tax

                    ####################################################################################################
                    # VULTR
                    ready_script += '/home/djangoadmin/final_site_venv/bin/python3 /home/djangoadmin/final_site-project' \
                                    '/scripts/execute_order_20.py {} {} {} {} {} {} {} {} {} && '.format(
                        domain_to_search, range_search, new_tax, 'none',test_correction, strand_select, temp_data_link,
                        method_average, skip_negative)
                    ####################################################################################################
                    # LOCAL
                    # ready_script += ' python3 /mnt/d/45.76.38.24/final_site-project/scripts/execute_order_20.py ' \
                    #                 '{} {} {} {} {} {} {} {} {}'.format(domain_to_search, range_search, new_tax, 'none',
                    #                         test_correction, strand_select, temp_data_link,method_average, skip_negative)
                ########################################################################################################
                # VULTR
                ready_script += '/home/djangoadmin/final_site_venv/bin/python3 /home/djangoadmin/final_site-project/scripts/execute_order_96.py ' \
                                '{} {} {} {}'.format(cut_off, link_down,database_taxa, ",".join(files_for_analysis))
                ########################################################################################################
                # LOCAL
                # ready_script += 'python3 /mnt/d/45.76.38.24/final_site-project/scripts/execute_order_96.py {} {] {} ' \
                #                 '{}'.format(cut_off, link_down,database_taxa, ",".join(files_for_analysis))
                ########################################################################################################

                # print(",".join(files_for_analysis))

                job = CompleteQueue(user_id=user_id, tool='NAD', status='Queue', analysis_name=out_name,
                                    script=ready_script, file=link_down)
                job.save()

                return redirect('dashboard')

            else:
                return render(request, 'tools/error/heavy_calculation.html')


        return redirect("dashboard")