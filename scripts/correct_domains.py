# -*- coding: utf-8 -*-
"""
Created on Tue Sep  3 14:05:28 2019

@author: bartek
"""
from collections import Counter
def Create6Lists(file):
    """ Open single genome file chew it and return 6 lists -> GENE, START_COORD, END_COORDS ,ORIENTATION, DOMAINS """

    data = OpenDatabaseFile(file)
    start_coord = []
    end_coord = []
    orientation = []
    domains = []
    genes = []
    contig = []
    for bit in data :
        genes.append(int(bit[0]))
        start_coord.append(int(bit[1]))
        end_coord.append(int(bit[2]))
        orientation.append(bit[3])
        domains.append(bit[4])
        contig.append(bit[5])
    return genes, start_coord,end_coord, orientation, domains, contig

def OpenDatabaseFile(file_name):
    """ Opens file that contains data about single genome """

    plik=[]
    with open(file_name+".txt") as inputfile:
        for line in inputfile:
            plik.append(line.strip().split())
    return plik

def OpenDirectory( file_name):
    """ Opens file that contain 1 column and strip it by space. """

    file_names=[]
    with open(file_name +'.txt', 'r') as f:
        file_names = [line.strip() for line in f]
    return file_names

def SaveOutput(file,all_together):
    with open("temp\\"+file , 'w') as output_file:
        for line in all_together:
            output_file.write(" ".join([str(i) for i in line]))
            output_file.write("\n")
user_OrganismsValues = ["escherichia","salmonella","pseudomonas","staphylococcus",
                       "streptococcus","mycobacterium","acinetobacter","vibrio",
                       "bacillus","klebsiella",
                       "enterococcus","burkholderia","lactobacillus","campylobacter",
                       "helicobacter","shigella","rhizobium", "brucella", "mesorhizobium"]




complete_dictionary = {}

for user_OrganismValue in user_OrganismsValues:

    if user_OrganismValue   == "escherichia":
        tax = "Escherichia"
      
    elif user_OrganismValue == "salmonella":
        tax ="Salmonella"
    elif user_OrganismValue ==  "pseudomonas":
        tax = "Pseudomonas"
    elif user_OrganismValue ==  "staphylococcus":
        tax = "Staphylococcus"
    elif user_OrganismValue ==  "streptococcus":
        tax = "Streptococcus"
    elif user_OrganismValue ==  "mycobacterium":
        tax = "Mycobacterium"
    elif user_OrganismValue ==  "acinetobacter":
        tax = "Acinetobacter"
    elif user_OrganismValue ==  "vibrio":
        tax = "Vibrio"
    elif user_OrganismValue ==  "bacillus":
        tax = "Bacillus"
    elif user_OrganismValue ==  "streptomyces":
        tax = "Streptomyces"
    elif user_OrganismValue == "porphyromonas":
        tax = "Porphyromonas"
    elif user_OrganismValue ==  "klebsiella":
        tax = "Klebsiella"
    elif user_OrganismValue ==  "enterococcus":
        tax = "Enterococcus"
    elif user_OrganismValue ==  "burkholderia":
        tax = "Burkholderia"        
    elif user_OrganismValue ==  "lactobacillus":
        tax = "Lactobacillus"
    elif user_OrganismValue ==  "campylobacter":
        tax = "Campylobacter"
    elif user_OrganismValue ==  "helicobacter":
        tax = "Helicobacter"
    elif user_OrganismValue ==  "shigella":
        tax = "Shigella"
    elif user_OrganismValue == "sinorhizobium":
        tax = "Sinorhizobium"
    elif user_OrganismValue == "brucella":
        tax = "Brucella"
    elif user_OrganismValue == "rhizobium":
        tax = "Rhizobium"
    elif user_OrganismValue == "mesorhizobium":
        tax = "Mesorhizobium"


    print(user_OrganismValue)
    complete_dictionary[user_OrganismValue] = [] 
    zliczanie_genome = Counter()
    zliczanie_wystapien = Counter()
    file_names = OpenDirectory('/home/djangoadmin/final_site-project/important_files/'+tax)

    for file in file_names:
        try:
            genes, start_coord,end_coord, orientation, domains, contig = Create6Lists(file)
        except FileNotFoundError:
            continue
        wystapnienie = set(domains)   
        zliczanie_wystapien += Counter(wystapnienie)
        zliczanie_genome += Counter(domains)
        
    ready_data_new = []


    for k,v in zliczanie_genome.items():
        if v/zliczanie_wystapien[k] < 11:
#            ready_data_new.append((k,v/zliczanie_wystapien[k]))
            complete_dictionary[user_OrganismValue].append(k)

import json
with open('test.json', 'w', encoding='utf-8') as f:
    json.dump(complete_dictionary, f, ensure_ascii=False, indent=4)