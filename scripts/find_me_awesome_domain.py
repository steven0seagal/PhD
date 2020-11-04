from collections import Counter
import numpy as np
def OpenDatabaseFile(file_name):
    plik = []
    with open(file_name + ".txt") as inputfile:
        for line in inputfile:
            plik.append(line.strip().split())
    return plik

def Create6Lists(file):
    data = OpenDatabaseFile(file)
    start_coord = []
    end_coord = []
    orientation = []
    domains = []
    genes = []
    contig = []
    for bit in data:
        genes.append(int(bit[0]))
        start_coord.append(int(bit[1]))
        end_coord.append(int(bit[2]))
        orientation.append(bit[3])
        domains.append(bit[4])
        contig.append(bit[5])
    return genes, start_coord, end_coord, orientation, domains, contig

def OpenFile(file_name):
    plik=[]
    with open(file_name+".txt") as inputfile:
        for line in inputfile:
            plik.append(line.strip().split())
    return plik

def OpenDirectory(file_name):
    file_names=[]
    with open(file_name +'.txt', 'r') as f:
        file_names = [line.strip() for line in f]
    return file_names

tax = "Escherichia"
file_names = OpenDirectory('/home/djangoadmin/final_site-project/important_files/'+tax)
mighty_domains= OpenDirectory('/home/djangoadmin/final_site-project/important_files/LISTA_DOMEN')
data = []


for file in file_names:
    #print(file)
    try:
        genes, start_coord, end_coord, orientation, domains, contig = Create6Lists(file)

    except FileNotFoundError:
        continue
    data.append(Counter(domains))

mean_data = []

for domain in mighty_domains:
    counter = 0
    #print(domain)
    part = []
    for genome in data:
        try:
            part.append(genome[domain])
            counter +=1
        except KeyError:
            continue

    print((np.mean(part), domain,len([x for x in part if x > 0  ])))