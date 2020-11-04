"""
Script created Wednesday October 9th 2019

@uthor: BP Baranowsky
"""

"""
Main goals of this script:
--> Analyzing gene neighborhood by gene list insert + separate script for regular yet superspeed 
--> Firstly by insert data directly to form
--> Next by file import 

Steps:
--> take list of gene id from BLAST
--> iterate through id 
--> check which id is in which genome and collect it
--> open selected genome and find target gene
--> collect all genes that are in range and in one scaffold
--> discard genes that dont contain pfam
--> count rest like ProFaNA 
"""

#################################################################################
""" Importing libraries that will be used. """  #
from collections import Counter  #
from scipy.stats import wilcoxon as test  #
import numpy as np  #
import pandas as pd  #
from statsmodels.stats.multitest import multipletests as correction  #
import statistics  #
import pdb  #
import datetime
import subprocess
import os
import json
#################################################################################


class NeighborhoodAnalyzerFromGene:

    def __init__(self, user_list_of_genes, user_distance_value,user_database, user_cutoff, user_correction, user_strand_value,
                 user_output):
        self.user_list_of_genes = user_list_of_genes
        self.user_distance_value = user_distance_value
        self.user_database = user_database
        self.user_cutoff = user_cutoff
        self.user_correction = user_correction
        self.user_strand_value = user_strand_value
        self.user_output = user_output

    def open_single_column_file(self, file_name):
        """ Opens file that contains one column of data """
        plik = []
        with open(file_name) as inputfile:
            for line in inputfile:
                plik.append(line.strip())
        return plik

    def open_multiple_column_file(self, file_name, split_mark=" "):
        """ Opens file that contain more than one column and split it by space. """
        plik = []
        with open(file_name) as inputfile:
            for line in inputfile:
                plik.append(line.strip().split(split_mark))
        return plik

    def open_singleline_num(self, path_to_file):
        """ Opens file that contain 1 column and strip it by space. """

        with open(path_to_file, 'r') as f:
            file_names = [float(line.strip()) for line in f]
        return file_names

    def open_json_file(self,file_name):
        with open(file_name, 'r') as fp:
            data = json.load(fp)
        all_data = []
        for key,values in data.items():
            all_data.append([key,values[0],values[1]])
        return all_data

    def open_query(self, path_to_file):

        with open(path_to_file, 'r') as f:
            file_names = [line.strip() for line in f]
        return file_names

    def save_complete(self, file, message_for_additional_data, complete_data):
        """ Saves all stuff together as one file """
        # KLASTER
        # with open('results/' + file, 'w') as output_file:
        # LOCAL 
        # with open('/mnt/d/45.76.38.24/final_site-project/results/' + file + '.txt', 'w') as output_file:

        # VULTR
        with open('/home/djangoadmin/final_site-project'+file, 'w') as output_file:
            output_file.write(message_for_additional_data)
            output_file.write("\n")
            # output_file.write(complete_data)
            for row in complete_data.iterrows():
                index, data = row
                pre = data.tolist()
                output_file.write(index)
                output_file.write("\t")
                output_file.write("\t".join([str(i) for i in pre]))
                output_file.write("\n")

    def collect_pfam_domain_description(self, file):
        """ Opens file only to gather information"""

        data = {}
        with open(file) as inputfile:
            for line in inputfile:
                try:

                    one_line = line.strip().split("@")
                    domena = one_line[0]
                    pre_family = one_line[1][8:]
                    delete_this = "(" + domena.upper() + ")"
                    family = pre_family.replace(delete_this, "")
                    summary = one_line[2][9:]
                    data[domena] = (family, summary)

                except IndexError:
                    continue
        return data

    def create_6_lists(self, file):

        # data = self.open_multiple_column_file(file)
        start_coord = []
        end_coord = []
        orientation = []
        domains = []
        genes = []
        contig = []
        # NOWA BAZA DANYCH, KLASTER
        # with open("nowa_baza_danych/"+file) as inputfile:
        # STARA BAZA DANYCH, local
        with open("/home/djangoadmin/final_site-project/important_files/nowa_baza_danych/"+file) as inputfile:
            for line in inputfile:
                bit = line.strip().split()

                genes.append(int(bit[0]))
                start_coord.append(int(bit[1]))
                end_coord.append(int(bit[2]))
                orientation.append(bit[3])
                domains.append(bit[4])
                contig.append(bit[5])
        return genes, start_coord, end_coord, orientation, domains, contig

    def find_correct_genome(self, gene, reference_data):

        for line in reference_data:
            genome = line[0]
            starts = [x for x in line[1::2]]
            ends = [x for x in line[2::2]]
            counter = 0
            for start in starts:
                end = ends[counter]
                counter += 1
                if int(gene) in range(int(start),int(end)+1):
                    return genome

    def get_genome_size_in_gene(self, genome_id, list_of_genome, list_of_size):
        """ Takes genome's id, list of genome and lists with data about how much genes in genome"""
        indeks_genomu = list_of_genome.index(genome_id)
        genome_size_in_gene = list_of_size[indeks_genomu]
        return genome_size_in_gene

    def search_for_gene_in_genome(self,q_gene, genes, start_coords, end_coords, orients, contig ):
        result = []
        main_index = genes.index(int(q_gene))
        result.append(start_coords[main_index])
        result.append(end_coords[main_index])
        result.append(orients[main_index])
        result.append(contig[main_index])
        result.append(q_gene)
        return result

    def get_range_coordinates(self, target_gene, distance):
        """
        Based on how large neighbourhood user wants to analyze creates
        points FROM and TO, additionaly shows where main user's pfam begins and ENDS
        with orientation on strands
        """

        gene_id = target_gene[4]
        gene_beg = target_gene[0]
        gene_end = target_gene[1]
        searched_gene_orient = target_gene[2]
        last_coordinate = gene_end + int(distance)
        first_coordinate = gene_beg - int(distance)


        return last_coordinate, first_coordinate, gene_beg,gene_end, searched_gene_orient

    def get_domain_both_strands(self,start_coord,end_coord, last_coordinate, first_coordinate, gene_beg,
                                gene_end,contig,result):
        pfam_index_to_neigh = []
        s_coord_counter = 0
        for s_coord in start_coord:
            if s_coord <= last_coordinate and s_coord >= gene_beg and contig[s_coord_counter] == result[
                3] and s_coord_counter not in pfam_index_to_neigh:
                pfam_index_to_neigh.append(s_coord_counter)
                s_coord_counter += 1
            else:
                s_coord_counter += 1
                continue
        e_coord_counter = 0
        for e_coord in end_coord:
            if e_coord >= first_coordinate and e_coord <= gene_end and contig[e_coord_counter] == result[
                3] and e_coord_counter not in pfam_index_to_neigh:
                pfam_index_to_neigh.append(e_coord_counter)
                e_coord_counter += 1
            else:
                e_coord_counter += 1
                continue
        return pfam_index_to_neigh

    def get_domain_both_zeros(self, ref_gene, q_gene):

        index_list_gene = []
        counter = 0
        for gene in ref_gene:
            if gene == int(q_gene):
                index_list_gene.append(counter)
            counter +=1
        return index_list_gene

    def get_list_of_genes_in_neigh(self, list_of_genes, index_list):
        """ Takes overall gene's list in genome and creates complete list of genes in neighbourhood """

        list_of_genes_in_neigh = []
        for pfam_domain in index_list:
            list_of_genes_in_neigh.append(list_of_genes[pfam_domain])
        return list_of_genes_in_neigh

    def get_size_in_genes(self,genome_or_gene_list):
        """ Takes list of genes and returns size of neighbourhood """

        list_of_genes = []
        for gene in genome_or_gene_list:
            list_of_genes.append(gene)
        return len(set(list_of_genes))

    def get_list_of_domain_in_neigh(self, pfam_index, gene, domains):

        to_counter = []
        party = []
        party.append(gene)
        for part in pfam_index:
            party.append(domains[part])
            to_counter.append(domains[part])
        #        neighbourhood_complete.append(party)
        # pdb.set_trace()
        return to_counter

    def multiple_test_correction(self, some_dataframe, correction_met):

        if correction_met == 'none':
            return some_dataframe
        else:
            value_to_correct = [float(x) for x in some_dataframe.PVALUE.tolist()]
            reject, pvals_corrected, alphaSidak, alphaBonf = correction(pvals=value_to_correct,
                                                                        method=correction_met,
                                                                        is_sorted=False, returnsorted=False)
            pvals = pvals_corrected.tolist()
            some_dataframe.PVALUE = pvals
            return some_dataframe

    def cutoff_value(self, some_dataframe, cutoff):

        domain_list = list(some_dataframe.index)
        if cutoff == 'none':
            return some_dataframe
        elif cutoff == '0':
            for i in domain_list:
                diff = float(some_dataframe.loc[i, 'PVALUE'])
                if diff < 0 and diff > 0:
                    some_dataframe = some_dataframe.drop([i])
            return some_dataframe
        else:
            cutoff = float(cutoff)
            for i in domain_list:
                diff = float(some_dataframe.loc[i, 'PVALUE'])
                if diff > cutoff:
                    some_dataframe = some_dataframe.drop([i])
            return some_dataframe

    def sort_table(self, some_dataframe):

        sorted_data = some_dataframe.sort_values('PVALUE', ascending=True)
        return sorted_data

    def add_information(self, some_dataframe, dictionary):

        indeksy = list(some_dataframe.index)
        for i in indeksy:
            try:

                pfam = i[0:2] + i[4:]
                family = dictionary[pfam][0]
                summary = dictionary[pfam][1]

                some_dataframe.at[i, 'Family'] = family
                some_dataframe.at[i, 'Summary'] = summary
            except KeyError:
                continue
        return some_dataframe

    def pfam_for_pf(self, dataframe):
        indexy = dataframe.index
        for i in indexy:
            dataframe = dataframe.rename(index={i:i[:2].upper()+i[4:]})
        dataframe['PVALUE'] = dataframe['PVALUE'].map('{:.3e}'.format)
        return dataframe

    def go(self):

        query_data = self.open_query("/home/djangoadmin/final_site-project"+self.user_list_of_genes)
        # VULTR
        domain_information = self.collect_pfam_domain_description(
            "/home/djangoadmin/final_site-project/important_files/domain_information")
        genome_gene_reference = self.open_multiple_column_file(
            "/home/djangoadmin/final_site-project/important_files/genomes_map")
        genome_size_in_gene = self.open_multiple_column_file(
            "/home/djangoadmin/final_site-project/important_files/GENOME_ID_SIZE_IN_GENE.txt")
        # # LOCAL
        # domain_information = self.collect_pfam_domain_description(
        #     '/mnt/d/45.76.38.24/final_site-project/important_files/domain_information')
        # "Zip all functions"
        # # open file about gene in genomes [genome min(gene) max(gene)]
        # genome_gene_reference = self.open_multiple_column_file(
        #     '/mnt/d/45.76.38.24/final_site-project/important_files/genomes_map')
        # # open file about genome size in gene and split to 2 lists
        # genome_size_in_gene = self.open_multiple_column_file(
        #     '/mnt/d/45.76.38.24/final_site-project/important_files/GENOME_ID_SIZE_IN_GENE.txt')

        # # KLASTER

        # domain_information = self.collect_pfam_domain_description(
        #     '/home/klaster/ProFaNA v1.0/important_files/domain_information')
        # genome_gene_reference = self.open_multiple_column_file(
        #     '/home/klaster/ProFaNA v1.0/important_files/genomes_map')
        # genome_size_in_gene = self.open_multiple_column_file(
        #     '/home/klaster/ProFaNA v1.0/important_files/GENOME_ID_SIZE_IN_GENE.txt')
        print("Checkpoint #1 Data loaded", datetime.datetime.now())
        genome_ids = [x[0] for x in genome_size_in_gene]
        genome_size = [x[1] for x in genome_size_in_gene]
        genome_size_in_gene = None
        just_neigh_data = []
        genomes_with_domains = []
        neigh_genome_size = []
        print("DLOK TIME START", datetime.datetime.now())
        # Loop through list of genes and do all stuff

        percentage_counter = Counter()
        for gene in query_data:
            try:

                # pdb.set_trace()
                correct_genome = self.find_correct_genome(gene,genome_gene_reference)

                correct_size = self.get_genome_size_in_gene(correct_genome,genome_ids,genome_size)
                ref_gene, ref_start_coord, ref_end_coord, ref_orient, ref_domain, ref_contig = self.create_6_lists(correct_genome)
                # pdb.set_trace()
                search_result = self.search_for_gene_in_genome(gene, ref_gene, ref_start_coord,ref_end_coord, ref_orient,
                                                            ref_contig)
                if self.user_distance_value != 0:
                    last_coordiate, first_coordinate, gene_beg, gene_end, searched_gene_orientation, = \
                        self.get_range_coordinates(search_result,self.user_distance_value)
                    pfam_index_to_neigh = self.get_domain_both_strands(ref_start_coord, ref_end_coord, last_coordiate,
                                                                    first_coordinate, gene_beg,gene_end,ref_contig,
                                                                    search_result)
                else:
                    pfam_index_to_neigh = self.get_domain_both_zeros(ref_gene,search_result[4])

                genes_in_neigh = self.get_list_of_genes_in_neigh(ref_gene,pfam_index_to_neigh)
                number_of_genes_in_neigh = self.get_size_in_genes(genes_in_neigh)
                whole_neigh = self.get_list_of_domain_in_neigh(pfam_index_to_neigh,gene,ref_domain)
                just_neigh_data.append(whole_neigh)
                genomes_with_domains.append(correct_genome)
                neigh_genome_size.append((number_of_genes_in_neigh, correct_size))
                percentage_counter += Counter(set(whole_neigh))
                # print(gene, whole_neigh)
            except ValueError:
                # print("Error at {}".format(gene))
                continue
        print("DLOK TIME OVER", datetime.datetime.now())
        print("concatenate_domain")
        alls = []
        neigh_counter = Counter()

        for i in just_neigh_data:
            for j in i:
                if j not in alls:
                    alls.append(j)
        genome_counter = Counter()

        print("MATRIX CREATING",datetime.datetime.now())
        counter = 0
        big_data = []

        for domain_list, genome_in_domain, ng_size in zip(just_neigh_data, genomes_with_domains, neigh_genome_size):

            counter += 1
            part = []
            
            genes, start_coord, end_coord, orientation, domains, contig = self.create_6_lists(genome_in_domain)
            genome_domains_counter = Counter(domains)
            genome_counter += genome_domains_counter
            neigh_domains_counter = Counter(domain_list)
            neigh_counter += neigh_domains_counter

            if counter != 100 and domain_list !=just_neigh_data[-1]:

                temp_data = []
                for fine_domain in alls:
                    dlok = neigh_domains_counter[fine_domain] / int(ng_size[0])
                    dglob = genome_domains_counter[fine_domain] / int(ng_size[1])
                    diff = dlok - dglob
                    part.append(str(diff))
                big_data.append(part)

            if counter != 100  and domain_list ==just_neigh_data[-1]:
                # pdb.set_trace()

                for place,domain in enumerate(alls):
                    data_to_save = [x[place] for x in big_data]
                    with open('temp_data/' + domain, 'a+') as output:
                        for num in data_to_save:
                            if num != '0.0':

                                output.write(num)
                                output.write("\n")
                big_data = []
                counter = 0
            elif counter == 100:
                for fine_domain in alls:
                    dlok = neigh_domains_counter[fine_domain] / int(ng_size[0])
                    dglob = genome_domains_counter[fine_domain] / int(ng_size[1])
                    diff = dlok - dglob
                    part.append(str(diff))
                big_data.append(part)


                for place,domain in enumerate(alls):
                    data_to_save = [x[place] for x in big_data]
                    with open('/home/djangoadmin/final_site-project/scripts/temp_data/' + domain, 'a+') as output:
                        for num in data_to_save:
                            if num != '0.0':

                                output.write(num)
                                output.write("\n")
                big_data = []
                counter = 0
        print("MATRIX OVER", datetime.datetime.now())


        print("Wilcoxon start", datetime.datetime.now())

        counter = 0
        scores = []
        # percentage = []
        for i in alls:
            counter +=1
            data_to_calculate = self.open_singleline_num("/home/djangoadmin/final_site-project/scripts/temp_data/" + i)
            for_percentage = [float(x) for x in data_to_calculate if x > 0]
            # percentage.append(len(for_percentage) / len(just_neigh_data))
            wynik = test(data_to_calculate, zero_method="wilcox")
            mean = sum(data_to_calculate)/len(just_neigh_data)
            scores.append((wynik.pvalue, mean))

        print("Wilcoxon OVER", datetime.datetime.now())

        print("Collecting data START", datetime.datetime.now())
        najlepsze_dane = pd.DataFrame(columns=['PVALUE', 'occurence in neighborhoods',
                                               'average occurence in neighborhood', 'occurence genomes',
                                               'average occurence in genome', 'Density difference',
                                               'In what percentage',
                                               'Family', 'Summary'])
        for domena, wynik in zip(alls, scores):
            if self.user_distance_value == 0 :
                if wynik[1] > 0:
                    najlepsze_dane.at[domena,'PVALUE'] = wynik[0]
                    najlepsze_dane.at[domena,'Density difference'] = wynik[1]
                    najlepsze_dane.at[domena, 'In what percentage'] = percentage_counter[domena]/len(just_neigh_data)
                else:
                    najlepsze_dane.at[domena, 'PVALUE'] = 1.0
                    najlepsze_dane.at[domena, 'Density difference'] = wynik[1]
                    najlepsze_dane.at[domena, 'In what percentage'] = percentage_counter[domena]/len(just_neigh_data)

            else:

                if wynik[1] > 0:
                    najlepsze_dane.at[domena,'PVALUE'] = wynik[0]
                    najlepsze_dane.at[domena,'Density difference'] = wynik[1]
                    najlepsze_dane.at[domena, 'In what percentage'] = percentage_counter[domena]/len(just_neigh_data)

        for domain in najlepsze_dane.index.to_list():
            najlepsze_dane.at[domain, 'occurence genomes'] = genome_counter[domain]
            najlepsze_dane.at[domain, 'average occurence in genome'] = genome_counter[domain] / len(
                set(genomes_with_domains))
            najlepsze_dane.at[domain, 'occurence in neighborhoods'] = neigh_counter[domain]
            najlepsze_dane.at[domain, 'average occurence in neighborhood'] = neigh_counter[domain]/len(just_neigh_data)

        print("Collecting data OVER", datetime.datetime.now())

        print("Customizing_data START", datetime.datetime.now())
        after_test = self.multiple_test_correction(najlepsze_dane, self.user_correction)
        after_cutoff = self.cutoff_value(after_test, self.user_cutoff)
        sorted_table = self.sort_table(after_cutoff)
        added_information = self.add_information(sorted_table, domain_information)
        final_data = self.pfam_for_pf(added_information)
        print("Customizing_data OVER", datetime.datetime.now())
        message_for_additional_data = "Pfam domain , PVALUE,  occurence in neighbourhoods, " \
                                      "average occurence in neighbourhood ,occurence genomes, " \
                                      "average occurence in genome, avg DLOK-DGLOB, In what percentage?, " \
                                      "Family, Summary"

        self.save_complete(self.user_output, message_for_additional_data, final_data)


class SuperSpeedAnalysisFromDomain:

    def __init__(self, user_pfam, user_distance, user_organisms, user_cutoff, user_correction,
                 user_strand, user_output):
        """ Initializing input data
            Inputs:
                    user_pfam:  str (from pfam00000 to pfam99999)
                    user_distance: non negative integer 1-20000
                    user_organisms: str
                    user_cutoff: str (none, 0, 0.00001, 0.00005, 0.0001, 0.0005, 0.001, 0.005,
                                 0.01, 0.05, 0.1, 0.2, 0.5)
                    user_correction: str (none, bonferroni, fdr_bh)
                    user_strand: str (both)
                    user_output: str
         """
        self.user_pfam = user_pfam
        self.user_distance = user_distance
        self.user_organisms = user_organisms
        self.user_cutoff = user_cutoff
        self.user_correction = user_correction
        self.user_strand = user_strand
        self.user_output = user_output

    def open_singleline(self, path_to_file):
        """ Opens file that contain 1 column and strip it by space. """

        with open(path_to_file, 'r') as f:
            file_names = [line.strip() for line in f]
        return file_names

    def open_singleline_num(self, path_to_file):
        """ Opens file that contain 1 column and strip it by space. """

        with open(path_to_file, 'r') as f:
            file_names = [float(line.strip()) for line in f]
        return file_names

    def open_multiple_line(self,path_to_file):
        """ Opens file that contains data about single genome """

        plik=[]
        with open(path_to_file) as inputfile:
            for line in inputfile:
                plik.append(line.strip().split())
        return plik

    def open_multiple_line_two(self,path_to_file):
        """ Opens file that contains data about single genome """

        # plik=[]
        with open(path_to_file) as inputfile:
            for line in inputfile:
                plik = line.strip().split(sep ="\t")
        return plik

    def save_data(self,file_name, message_for_output,message_for_additional_data, message_down, complete_data):
        """ Saves all stuff together as one file """

        # # LOCAL
        # with open('/mnt/d/45.76.38.24/final_site-project/results/' + file_name + '.txt', 'w') as output_file:
        # VULTR
        with open('/home/djangoadmin/final_site-project'+file_name, 'w') as output_file:
            output_file.write(message_for_output)
            output_file.write("\n")
            output_file.write(message_down)
            output_file.write("\n")
            output_file.write(message_for_additional_data)
            output_file.write("\n")
            # output_file.write(complete_data)
            for row in complete_data.iterrows():
                index, data = row
                pre = data.tolist()
                output_file.write(index)
                output_file.write("\t")
                output_file.write("\t".join([str(i) for i in pre]))
                output_file.write("\n")

    def create_six_list(self, file):
        """ Open single genome file chew it and return 6 lists -> GENE, START_COORD,
        END_COORDS ,ORIENTATION, DOMAINS """

        # data = self.open_multiple_line("/home/klaster/ProFaNA v1.0/nowa_baza_danych/"+file)
        # data = self.open_multiple_line(file+".txt")
        data = self.open_multiple_line("/home/djangoadmin/final_site-project/important_files/nowa_baza_danych/"+file)
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

    def genome_size_in_gene(self, genome_id, list_of_genome,list_of_size):
        """ Takes genome's id, list of genome and lists with data about how much genes in genome"""

        index_genome = list_of_genome.index(genome_id)
        genome_size_in_gene = list_of_size[index_genome]
        return genome_size_in_gene

    def size_in_genes(self, genome_or_genes):
        """ Takes list of genes and returns size of neighbourhood """

        list_of_genes = []
        for gene in genome_or_genes:
            list_of_genes.append(gene)
        return len(set(list_of_genes))

    def list_of_genes_in_neigh(self, list_of_genes, index_list):
        """ Takes overall gene's list in genome and creates complete list of genes in neighbourhood """

        list_of_genes_in_neigh = []
        for pfam_domain in index_list:
            list_of_genes_in_neigh.append(list_of_genes[pfam_domain])
        return list_of_genes_in_neigh

    def searching_for_domain_in_genome(self, pfam, start_coord, end_coord, orient, domains, contig, genes):
        """
        Takes user's pfam domain searches through lists contains coordinates,
        orientation, domains, contigs and returns complete data about all
        users' domains in genome
        """
        coords = []
        coords_counter = 0
        for domain in domains:
            one_coords_part = []
            if domain == pfam:
                orientation_pfam_domain = orient[coords_counter]
                one_coords_part.append(start_coord[coords_counter])
                one_coords_part.append(end_coord[coords_counter])
                one_coords_part.append(orientation_pfam_domain)
                one_coords_part.append(contig[coords_counter])
                one_coords_part.append(genes[coords_counter])
                coords.append(one_coords_part)
                coords_counter += 1
            else:
                coords_counter += 1
                continue
        return coords

    def presence_confirmation(self,coords,file, pfam):
        """
                Just prints out information how many pfam domains is in each genome
                during analysis propably i will have to remove it before putting it to website ...
                """

        if len(coords) == 0:
            print("In genome  " + file + " pfam domain you have been searching do not exist")
        elif len(coords) == 1:
            print("In genome  " + file + " there is " + str(len(coords)) + " " + pfam + " domain")
        else:
            print("In genome  " + file + " there are " + str(len(coords)) + " " + pfam + " domains")

    def get_range_coordinates(self, target_pfam, distance):
        """
        Based on how large neighbourhood user wants to analyze creates
        points FROM and TO, additionaly shows where main user's pfam begins and ENDS
        with orientation on strands
        """

        last_coordinate = target_pfam[1] + int(distance)
        first_coordinate = target_pfam[0] - int(distance)
        pfam_beg = target_pfam[0]
        pfam_end = target_pfam[1]
        searched_pfam_orientation = target_pfam[2]
        return last_coordinate, first_coordinate, pfam_beg, pfam_end, searched_pfam_orientation

    def get_domain_both_zeros(self, ref_gene, q_gene):

        index_list_gene = []
        counter = 0
        for gene in ref_gene:
            if gene == int(q_gene):
                index_list_gene.append(counter)
            counter +=1
        return index_list_gene

    def get_domains_both_strands(self,start_coord, end_coord, last_coordinate, first_coordinate, pfam_beg,
                                  pfam_end, contig, point):

        pfam_index_to_neigh = []
        s_coord_counter = 0
        for s_coord in start_coord:
            if s_coord <= last_coordinate and s_coord >= pfam_beg and contig[s_coord_counter] == point[
                3] and s_coord_counter not in pfam_index_to_neigh:
                pfam_index_to_neigh.append(s_coord_counter)
                s_coord_counter += 1
            else:
                s_coord_counter += 1
                continue
        e_coord_counter = 0
        for e_coord in end_coord:
            if e_coord >= first_coordinate and e_coord <= pfam_end and contig[e_coord_counter] == point[
                3] and e_coord_counter not in pfam_index_to_neigh:
                pfam_index_to_neigh.append(e_coord_counter)
                e_coord_counter += 1
            else:
                e_coord_counter += 1
                continue
        return pfam_index_to_neigh

    def collect_pfam_domain_description(self, file):
        """ Opens file only to gather information"""

        data = {}
        with open(file) as inputfile:
            for line in inputfile:
                try:

                    one_line = line.strip().split("@")
                    domena = one_line[0]
                    pre_family = one_line[1][8:]
                    delete_this = "(" + domena.upper() + ")"
                    family = pre_family.replace(delete_this, "")
                    summary = one_line[2][9:]
                    data[domena] = (family, summary)

                except IndexError:
                    continue
        return data

    def get_domains_plus_minus_strand(self,start_coord, end_coord, last_coordinate, first_coordinate,
                                              pfam_beg, pfam_end, contig, point, orientation):

        pfam_index_to_neigh_same_strand = []
        pfam_index_to_neigh_oposite_strand = []
        s_coord_counter = 0
        for s_coord in start_coord:
            if s_coord <= last_coordinate and s_coord >= pfam_beg and orientation[s_coord_counter] == point[2] and \
                    contig[s_coord_counter] == point[3] and s_coord_counter not in pfam_index_to_neigh_same_strand:
                pfam_index_to_neigh_same_strand.append(s_coord_counter)
                s_coord_counter += 1
            elif s_coord <= last_coordinate and s_coord >= pfam_beg and orientation[s_coord_counter] != point[2] and \
                    contig[s_coord_counter] == point[
                3] and s_coord_counter not in pfam_index_to_neigh_oposite_strand:
                pfam_index_to_neigh_oposite_strand.append(s_coord_counter)
                s_coord_counter += 1
            else:
                s_coord_counter += 1
                continue
        e_coord_counter = 0
        for e_coord in end_coord:
            if e_coord >= first_coordinate and e_coord <= pfam_end and orientation[e_coord_counter] == point[2] and \
                    contig[e_coord_counter] == point[3] and e_coord_counter not in pfam_index_to_neigh_same_strand:
                pfam_index_to_neigh_same_strand.append(e_coord_counter)
                e_coord_counter += 1
            elif e_coord >= first_coordinate and e_coord <= pfam_end and orientation[e_coord_counter] != point[
                2] and contig[e_coord_counter] == point[
                3] and e_coord_counter not in pfam_index_to_neigh_oposite_strand:
                pfam_index_to_neigh_oposite_strand.append(e_coord_counter)
                e_coord_counter += 1
            else:
                e_coord_counter += 1
                continue
        return pfam_index_to_neigh_same_strand, pfam_index_to_neigh_oposite_strand

    def get_list_of_domain_in_neigh(self, pfam_index, file,domains):

        to_counter = []
        party = []
        party.append(file)
        for part in pfam_index:
            party.append(domains[part])
            to_counter.append(domains[part])
        #        neighbourhood_complete.append(party)

        return to_counter

    def counting_dlok_or_dglob(self,some_counter, genome_neigh_size, mighty_domains):
        dlok_glob = []
        for domain_mighty in mighty_domains:
            if domain_mighty in some_counter.keys():
                lok_glob = some_counter.get(domain_mighty) / int(genome_neigh_size)
                dlok_glob.append(lok_glob)
            else:
                dlok_glob.append(0)
        return dlok_glob

    def count_for_dlok(self,somecounter, neigh_size,tax_name,dlok_dataframe):
        for k,v in somecounter.items():
            dlok_dataframe.at[tax_name, k] = v/neigh_size

    def multiple_test_correction(self, some_dataframe, correction_met):

        if correction_met == 'none':
            return some_dataframe
        else:
            value_to_correct = [float(x) for x in some_dataframe.PVALUE.tolist()]
            reject, pvals_corrected, alphaSidak, alphaBonf = correction(pvals=value_to_correct,
                                                                        method=correction_met,
                                                                        is_sorted=False, returnsorted=False)
            pvals = pvals_corrected.tolist()
            some_dataframe.PVALUE = pvals
            return some_dataframe

    def cutoff_value(self, some_dataframe, cutoff):

        domain_list = list(some_dataframe.index)
        if cutoff == 'none':
            return some_dataframe
        elif cutoff == '0':
            for i in domain_list:
                diff = float(some_dataframe.loc[i, 'PVALUE'])
                if diff < 0 and diff > 0:
                    some_dataframe = some_dataframe.drop([i])
            return some_dataframe
        else:
            cutoff = float(cutoff)
            for i in domain_list:
                diff = float(some_dataframe.loc[i, 'PVALUE'])
                if diff > cutoff:
                    some_dataframe = some_dataframe.drop([i])
            return some_dataframe

    def sort_table(self, some_dataframe):

        sorted_data = some_dataframe.sort_values('PVALUE', ascending=True)
        return sorted_data

    def add_information(self, some_dataframe, dictionary):

        indeksy = list(some_dataframe.index)
        for i in indeksy:
            try:

                pfam = i[0:2] + i[4:]
                family = dictionary[pfam][0]
                summary = dictionary[pfam][1]

                some_dataframe.at[i, 'Family'] = family
                some_dataframe.at[i, 'Summary'] = summary
            except KeyError:
                continue
        return some_dataframe

    def pfam_for_pf(self, dataframe):
        indexy = dataframe.index
        for i in indexy:
            dataframe = dataframe.rename(index={i:i[:2].upper()+i[4:]})
        dataframe['PVALUE'] = dataframe['PVALUE'].map('{:.3e}'.format)
        return dataframe

    def go(self):
        """Zipping all functions and execute them"""

        # JUST LOCALLY
        # print("checkpoint #1")
        # mighty_domains= self.open_singleline(
        #     '/mnt/d/45.76.38.24/final_site-project/important_files/LISTA_DOMEN.txt')
        # genome_id_size_in_bp = self.open_multiple_line(
        #     '/mnt/d/45.76.38.24/final_site-project/important_files/GENOME_ID_SIZE_IN_BP.txt')
        # genome_id_size_in_gene = self.open_multiple_line(
        #     '/mnt/d/45.76.38.24/final_site-project/important_files/GENOME_ID_SIZE_IN_GENE.txt')
        # domain_information = self.collect_pfam_domain_description(
        #     '/mnt/d/45.76.38.24/final_site-project/important_files/domain_information')

        # # KLASTER
        #
        # print("checkpoint #1")
        # # KLASTER
        # domain_information = self.collect_pfam_domain_description(
        #     '/home/klaster/ProFaNA v1.0/important_files/domain_information')
        # genome_id_size_in_gene = self.open_multiple_line(
        #     '/home/klaster/ProFaNA v1.0/important_files/GENOME_ID_SIZE_IN_GENE.txt')
        
        ## VULTR
        print("checkpoint 1")
        domain_information = self.collect_pfam_domain_description(
            "/home/djangoadmin/final_site-project/important_files/domain_information")
        genome_id_size_in_gene = self.open_multiple_line(
            "/home/djangoadmin/final_site-project/important_files/GENOME_ID_SIZE_IN_GENE.txt")
        
        genome_id = [x[0] for x in genome_id_size_in_gene]
        size_in_gene = [x[1] for x in genome_id_size_in_gene]

        print("checkpoint #2")
        genome_dataframe = pd.DataFrame()
        neigh_dataframe = pd.DataFrame()
        genome_number_overall = 0
        genome_number_to_stat = 0

        just_dlok = pd.DataFrame()
        just_dlok_dglob = pd.DataFrame()


        list_dlok_matrix = []
        list_dglob_matrix = []
        list_matrix = []
        pfam_whole_domain_counter = Counter({})
        pfam_same_strand_domain_counter = Counter({})
        pfam_oposite_strand_domain_counter = Counter({})
        message_for_output = "You have looked for conserved neighbourhood for " + self.user_pfam + \
                             " domain, in range " + str(self.user_distance) + \
                             " bp, in " + self.user_organisms + " database."
        print(message_for_output)
        message_for_additional_data = "Pfam domain , PVALUE,  occurence in neighbourhoods, " \
                                      "average occurence in neighbourhood ,occurence genomes, " \
                                      "average occurence in genome, avg DLOK-DGLOB, In what percentage?, " \
                                      "Family, Summary"



        ######################### TAX SELECTION ######################################

        if self.user_organisms == "escherichia":
            tax = "Escherichia"
        elif self.user_organisms == "salmonella":
            tax = "Salmonella"
        elif self.user_organisms == "pseudomonas":
            tax = "Pseudomonas"
        elif self.user_organisms == "staphylococcus":
            tax = "Staphylococcus"
        elif self.user_organisms == "streptococcus":
            tax = "Streptococcus"
        elif self.user_organisms == "mycobacterium":
            tax = "Mycobacterium"
        elif self.user_organisms == "acinetobacter":
            tax = "Acinetobacter"
        elif self.user_organisms == "vibrio":
            tax = "Vibrio"
        elif self.user_organisms == "bacillus":
            tax = "Bacillus"
        elif self.user_organisms == "streptomyces":
            tax = "Streptomyces"
        elif self.user_organisms == "porphyromonas":
            tax = "Porphyromonas"
        elif self.user_organisms == "klebsiella":
            tax = "Klebsiella"
        elif self.user_organisms == "enterococcus":
            tax = "Enterococcus"
        elif self.user_organisms == "burkholderia":
            tax = "Burkholderia"
        elif self.user_organisms == "lactobacillus":
            tax = "Lactobacillus"
        elif self.user_organisms == "campylobacter":
            tax = "Campylobacter"
        elif self.user_organisms == "helicobacter":
            tax = "Helicobacter"
        elif self.user_organisms == "shigella":
            tax = "Shigella"
        elif self.user_organisms == "all_db":
            tax = "all_genomes"
        elif self.user_organisms == "enterobacteriaceae":
            tax = "Enterobacteriaceae"
        elif self.user_organisms == "yokenella":
            tax = "Yokenella"
        elif self.user_organisms == "trabulsiella":
            tax = "Trabulsiella"
        elif self.user_organisms == "superficieibacter":
            tax = "Superficieibacter"
        elif self.user_organisms == "siccibacter":
            tax = "Siccibacter"
        elif self.user_organisms == "shimwellia":
            tax = "Shimwellia"
        elif self.user_organisms == "rosenbergiella":
            tax = "Rosenbergiella"
        elif self.user_organisms == "raoultella":
            tax = "Raoultella"
        elif self.user_organisms == "pseudocitrobacter":
            tax = "Pseudocitrobacter"
        elif self.user_organisms == "pluralibacter":
            tax = "Pluralibacter"
        elif self.user_organisms == "metakosakonia":
            tax = "Metakosakonia"
        elif self.user_organisms == "mangrovibacter":
            tax = "Mangrovibacter"
        elif self.user_organisms == "limnobaculum":
            tax = "Limnobaculum"
        elif self.user_organisms == "lelliottia":
            tax = "Lelliottia"
        elif self.user_organisms == "leclercia":
            tax = "Leclercia"
        elif self.user_organisms == "kluyvera":
            tax = "Kluyvera"
        elif self.user_organisms == "izhakiella":
            tax = "Izhakiella"
        elif self.user_organisms == "gibbsiella":
            tax = "Gibbsiella"
        elif self.user_organisms == "franconibacter":
            tax = "Franconibacter"
        elif self.user_organisms == "enterobacter":
            tax = "Enterobacter"
        elif self.user_organisms == "enterobacillus":
            tax = "Enterobacillus"
        elif self.user_organisms == "cronobacter":
            tax = "Cronobacter"
        elif self.user_organisms == "citrobacter":
            tax = "Citrobacter"
        elif self.user_organisms == "cedecea":
            tax = "Cedecea"
        elif self.user_organisms == "buttiauxella":
            tax = "Buttiauxella"
        elif self.user_organisms == "biostraticola":
            tax = "Biostraticola"
        elif self.user_organisms == "atlantibacter":
            tax = "Atlantibacter"


        ################################################################################

        # # LOCAL
        # file_names = self.open_singleline('/mnt/d/45.76.38.24/final_site-project/important_files/' + tax+'.txt')
        # KLASTER
        # file_names = self.open_singleline('/home/klaster/ProFaNA v1.0/important_files/' + tax)
        # VULTR
        file_names = self.open_singleline('/home/djangoadmin/final_site-project/important_files/'+tax)
        just_neigh_data = []
        genomes_with_domain = []
        neigh_genome_size = []

        counter = 0
        counter_db = 0
        percentage_counter = Counter()
        print("DLOK TIME START",datetime.datetime.now())
        for file in file_names:
            counter_db +=1
            # pdb.set_trace()
            counter +=1
            try:
                genes, start_coord, end_coord, orientation, domains, contig = self.create_six_list(file)
            except FileNotFoundError:
                continue
            except ValueError:
                continue
            file_name_raw = file.split('/')
            tax_name = file_name_raw[-1]
            genome_number_overall += 1
            number_of_genes_in_genome = self.genome_size_in_gene(tax_name, genome_id, size_in_gene)
            coords = self.searching_for_domain_in_genome(self.user_pfam, start_coord, end_coord, orientation,
                                                         domains, contig,genes)
            if len(coords) > 0:
                genome_number_to_stat += 1

            for point in coords:

                if self.user_distance != 0:
                    last_coordinate, first_coordinate, pfam_beg, pfam_end, searched_pfam_orientation = self.get_range_coordinates(
                        point, self.user_distance)
                    pfam_index_to_neigh = self.get_domains_both_strands(start_coord, end_coord, last_coordinate,
                                                                        first_coordinate, pfam_beg, pfam_end, contig,
                                                                        point)
                else:
                    pfam_index_to_neigh = self.get_domain_both_zeros(genes,point[4])


                genes_in_neigh = self.list_of_genes_in_neigh(genes, pfam_index_to_neigh)
                number_of_genes_in_neigh = self.size_in_genes(genes_in_neigh)
                whole = self.get_list_of_domain_in_neigh(pfam_index_to_neigh,file,domains)

                percentage_counter += Counter(set(whole))

                # neighbourhood_domains_counter = Counter(whole)

                # d_lok = self.counting_dlok_or_dglob(neighbourhood_domains_counter, number_of_genes_in_neigh, mighty_domains)
                # self.count_for_dlok(neighbourhood_domains_counter,number_of_genes_in_neigh,tax_name,just_dlok)
                # pfam_whole_domain_counter += Counter(whole)
                just_neigh_data.append(whole)
                genomes_with_domain.append(file)
                neigh_genome_size.append((number_of_genes_in_neigh,number_of_genes_in_genome))
                # pdb.set_trace()
        print("DLOK TIME OVER", datetime.datetime.now())
        print("concatenate_domain")

        alls = []
        neigh_counter = Counter()

        for i in just_neigh_data:

            for j in i:
                if j not in alls:
                    alls.append(j)
        genome_counter = Counter()
        print(len(alls))
        # pdb.set_trace()
        print("MATRIX CREATING",datetime.datetime.now())


        counter = 0
        big_data = []
        already_scanned = []
        for domain_list, genome_in_domain, ng_size in zip(just_neigh_data, genomes_with_domain, neigh_genome_size):

            counter += 1
            part = []
            genes, start_coord, end_coord, orientation, domains, contig = self.create_six_list(genome_in_domain)

            genome_domains_counter = Counter(domains)
            neigh_domains_counter = Counter(domain_list)
            neigh_counter += neigh_domains_counter

            if genome_in_domain not in already_scanned:
                genome_counter += genome_domains_counter
            already_scanned.append(genome_in_domain)
            


        print("MATRIX OVER", datetime.datetime.now())
        # pdb.set_trace()
        print("Wilcoxon start", datetime.datetime.now())

        

        counter = 0
        scores = []
        # percentage = []
        for i in alls:

            counter +=1

            # data_to_calculate = self.open_singleline_num("temp_data/" + i)
            # for_percentage = [float(x) for x in data_to_calculate if x > 0]
            # percentage.append(len(for_percentage) / len(just_neigh_data))
            wynik = 0
            mean = 15
            scores.append((wynik, mean))







        print("Wilcoxon OVER", datetime.datetime.now())
        # pdb.set_trace()
        print("Collecting data START", datetime.datetime.now())
        najlepsze_dane = pd.DataFrame(columns=['PVALUE','occurence in neighborhoods',
                                               'average occurence in neighborhood','occurence genomes',
                                               'average occurence in genome','Density difference', 'In what percentage',
                                                'Family', 'Summary'])
        for domena, wynik, in zip(alls,scores):
            if self.user_distance ==0 :
                if wynik[1] > 0:
                    najlepsze_dane.at[domena,'PVALUE'] = wynik[0]
                    najlepsze_dane.at[domena,'Density difference'] = wynik[1]
                    najlepsze_dane.at[domena,'In what percentage'] = percentage_counter[domena]/len(just_neigh_data)
                else:
                    najlepsze_dane.at[domena, 'PVALUE'] = 1.0
                    najlepsze_dane.at[domena, 'Density difference'] = wynik[1]
                    najlepsze_dane.at[domena, 'In what percentage'] = percentage_counter[domena]/len(just_neigh_data)
            else:

                if wynik[1] > 0:
                    najlepsze_dane.at[domena,'PVALUE'] = wynik[0]
                    najlepsze_dane.at[domena,'Density difference'] = wynik[1]
                    najlepsze_dane.at[domena, 'In what percentage'] = percentage_counter[domena]/len(just_neigh_data)
        for domain in najlepsze_dane.index.to_list():
            najlepsze_dane.at[domain, 'occurence in neighborhoods'] = neigh_counter[domain]
            najlepsze_dane.at[domain, 'average occurence in neighborhood'] = neigh_counter[domain]/len(just_neigh_data)
            najlepsze_dane.at[domain, 'occurence genomes'] = genome_counter[domain]
            najlepsze_dane.at[domain, 'average occurence in genome'] = genome_counter[domain]/len(set(genomes_with_domain))
        print("Collecting data OVER", datetime.datetime.now())
        # pdb.set_trace()
        print("Customizing_data START", datetime.datetime.now())
        after_test = self.multiple_test_correction(najlepsze_dane, self.user_correction)
        after_cutoff = self.cutoff_value(after_test, self.user_cutoff)
        sorted_table = self.sort_table(after_cutoff)
        added_information = self.add_information(sorted_table,domain_information)
        final_data = self.pfam_for_pf(added_information)
        print("Customizing_data OVER", datetime.datetime.now())
        message_down = " In selected database there is {} genomes and in {} searched domain " \
                       "was found".format(str(counter_db),str(genome_number_to_stat) )
        # pdb.set_trace()
        self.save_data(self.user_output,message_for_output,message_for_additional_data,message_down,final_data)


#
if __name__ == "__main__":

    

    a = SuperSpeedAnalysisFromDomain('pfam01636', 5000, 'all_db', 'none' ,'none', 'both','/media/results/new_pfam01636.txt' )
    a.go()



#
#     # # # a.start()