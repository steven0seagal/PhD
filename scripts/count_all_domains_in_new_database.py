from collections import Counter
import json

def open_singleline(path_to_file):
    """ Opens file that contain 1 column and strip it by space. """

    with open(path_to_file, 'r') as f:
        file_names = [line.strip() for line in f]
    return file_names

def create_domain_lists(file):
    # data = self.open_multiple_column_file(file)

    domains = []

    # NOWA BAZA DANYCH, KLASTER
    # with open("nowa_baza_danych/"+file) as inputfile:
    # STARA BAZA DANYCH, local
    with open("/home/djangoadmin/final_site-project/important_files/nowa_baza_danych/" + file) as inputfile:
        for line in inputfile:
            bit = line.strip().split()


            domains.append(bit[4])

    return domains

file_names = open_singleline('/home/djangoadmin/final_site-project/important_files/all_genomes')
counter = 0
all_counter = Counter()
for file in file_names:
    counter += 1
    try:
        domain_file = create_domain_lists(file)
        lista_domen_plik = Counter(domain_file)
        all_counter += lista_domen_plik
    except ValueError:
        continue
    except IndexError:
        continue

for k,v in all_counter.items():
    print(k,v)