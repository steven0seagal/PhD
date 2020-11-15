"""
Script created Wednesday October 9th 2019

@uthor: BP Baranowsky
"""

"""
Changes :
--> Inserted tool for finding genomes that are not downloaded in my database
"""

#################################################################################
""" Importing libraries that will be used. """
from collections import Counter
from scipy.stats import wilcoxon as test
import pandas as pd
from statsmodels.stats.multitest import multipletests as correction  #
import datetime
import json


#################################################################################

class SuperSpeedAnalysisFromDomain:

    def __init__(self, user_pfam, user_distance, user_organisms, user_cutoff, user_correction,
                 user_strand, user_output,skip_negative):
        """ Initializing input data
            Inputs:
                    user_pfam:  str (from pfam00000 to pfam99999)
                    user_distance: str non negative integer 1-20000
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
        self.skip_negative = skip_negative

    def open_singleline(self, path_to_file):
        """ Opens file that contain 1 column and strip it by space.
            Inputs:
                    path_to_file: str
        """

        with open(path_to_file, 'r') as f:
            file_names = [line.strip() for line in f]
        return file_names

    def open_singleline_num(self, path_to_file):
        """ Opens file that contain 1 column and strip it by space. """

        with open(path_to_file, 'r') as f:
            file_names = [float(line.strip()) for line in f]
        return file_names

    def open_multiple_line(self, path_to_file):
        """ Opens file that contains data about single genome """

        plik = []
        with open(path_to_file) as inputfile:
            for line in inputfile:
                plik.append(line.strip().split())
        return plik

    def save_data(self, file_name, message_for_output, message_for_additional_data, message_down, complete_data):
        """ Saves all stuff together as one file """

        # # LOCAL
        # with open('/mnt/d/45.76.38.24/final_site-project' + file_name + '.txt', 'w') as output_file:
        # VULTR
        with open('/home/djangoadmin/final_site-project' + file_name, 'w') as output_file:
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
        # KLASTER
        # data = self.open_multiple_line("/home/klaster/ProFaNA v1.0/nowa_baza_danych/"+file)

        # LOCAL
        # data = self.open_multiple_line("/mnt/d/45.76.38.24/final_site-project/important_files/database_file/"+file)

        # VULTR
        data = self.open_multiple_line("/home/djangoadmin/final_site-project/important_files/nowa_baza_danych/" + file)
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

    def open_database(self,tax):

        tax = tax.replace("_", " ")
        if tax == "all genomes":

            # LOCAL
            # with open("/mnt/d/45.76.38.24/final_site-project/important_files/all_genomes.txt","r") as handler:

            # VULTR
            with open("/home/djangoadmin/final_site-project/important_files/all_genomes","r") as handler:
                genomes = [x.strip() for x in handler]
            return genomes

        else:
            # LOCAL
            # with open('/mnt/d/45.76.38.24/final_site-project/important_files/database.json', "r") as handler:

            # VULTR
            with open("/home/djangoadmin/final_site-project/important_files/database.json", "r") as handler:
                data = json.load(handler)
            if tax in data.keys():
                genomes = []
                for genus, genome in data[tax].items():
                    genomes += genome
                return genomes
            else:
                for family,genera in data.items():
                    if tax in genera:
                        genomes = data[family][tax]
                return genomes

    def genome_size_in_gene(self, genome_id, list_of_genome, list_of_size):
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

    def presence_confirmation(self, coords, file, pfam):
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
        """Collect only domains that are in one gene"""

        index_list_gene = []
        counter = 0
        for gene in ref_gene:
            if gene == int(q_gene):
                index_list_gene.append(counter)
            counter += 1
        return index_list_gene

    def get_domains_both_strands(self, start_coord, end_coord, last_coordinate, first_coordinate, pfam_beg,
                                 pfam_end, contig, point):
        """Collect  domains that are in selected range"""

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

    def get_domains_plus_minus_strand(self, start_coord, end_coord, last_coordinate, first_coordinate,
                                      pfam_beg, pfam_end, contig, point, orientation):
        """Get domains from selected strand +/-"""

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

    def get_list_of_domain_in_neigh(self, pfam_index, file, domains):
        """ Complete list of domains"""

        to_counter = []
        party = []
        party.append(file)
        for part in pfam_index:
            party.append(domains[part])
            to_counter.append(domains[part])
        #        neighbourhood_complete.append(party)

        return to_counter

    def counting_dlok_or_dglob(self, some_counter, genome_neigh_size, mighty_domains):
        """Count DLOK DGLOB index"""

        dlok_glob = []
        for domain_mighty in mighty_domains:
            if domain_mighty in some_counter.keys():
                lok_glob = some_counter.get(domain_mighty) / int(genome_neigh_size)
                dlok_glob.append(lok_glob)
            else:
                dlok_glob.append(0)
        return dlok_glob

    def count_for_dlok(self, somecounter, neigh_size, tax_name, dlok_dataframe):

        for k, v in somecounter.items():
            dlok_dataframe.at[tax_name, k] = v / neigh_size

    def multiple_test_correction(self, some_dataframe, correction_met):
        "Multiple test correction"

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

    def multiple_test_correction_list(self,some_tuple_list,correction_met):
        "Multiple test correction from list"

        pvalues = [float(x[0]) for x in some_tuple_list]
        density = [x[1] for x in some_tuple_list]

        if correction_met == 'none':
            output = [(i, j) for i, j in zip(pvalues, density)]

        else:
            try:

                reject, pvals_corrected, alphaSidak, alphaBonf = correction(pvals=pvalues,
                                                                            method=correction_met,
                                                                            is_sorted=False, returnsorted=False)
                pvals_after_corr = pvals_corrected.tolist()
                output = [(i, j) for i, j in zip(pvals_after_corr, density)]
            except ZeroDivisionError:
                output = [(i, j) for i, j in zip(pvalues, density)]
        return output

    def cutoff_value(self, some_dataframe, cutoff):
        """Return dataframe with values below selected"""

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
        """Add extra information to dataframe"""

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
        """Final customization of dataframe
            --> PF02696 instead of pfam02696
            --> PVALUE in 10e-3 format
            --> In what percentage % format
            --> avg occurences and density  have now 3 digits after coma
            --> drop NOam
        """

        indexy = dataframe.index
        for i in indexy:
            dataframe = dataframe.rename(index={i: i[:2].upper() + i[4:]})
        dataframe['PVALUE'] = dataframe['PVALUE'].map('{:.3e}'.format)
        dataframe['In what percentage'] = dataframe['In what percentage'].map('{:.3%}'.format)
        dataframe['average occurence in neighborhood'] = dataframe['average occurence in neighborhood'].map('{:.3}'.format)
        dataframe['Density difference'] = dataframe['Density difference'].map('{:.3}'.format)
        dataframe['average occurence in genome'] = dataframe['average occurence in genome'].map('{:.3}'.format)

        # dataframe = dataframe.round({"average occurence in neighborhood": 3,"average occurence in genome": 3,
        #                              "Density difference": 3})
        if "NOam" in indexy:
            dataframe = dataframe.drop(index="NOam")
        # dataframe = dataframe.style.format({'In what percentage': '{:,.3%}'.format})
        return dataframe

    def go(self):
        print(self.user_organisms)
        """Zipping all functions and execute them"""
        ################################################################################################################
        # JUST LOCALLY
        # print("checkpoint #1")
        # genome_id_size_in_gene = self.open_multiple_line(
        #     '/mnt/d/45.76.38.24/final_site-project/important_files/GENOME_ID_SIZE_IN_GENE.txt')
        # domain_information = self.collect_pfam_domain_description(
        #     '/mnt/d/45.76.38.24/final_site-project/important_files/domain_information')
        ################################################################################################################

        ################################################################################################################
        # # KLASTER
        #
        # print("checkpoint #1")
        # # KLASTER
        # domain_information = self.collect_pfam_domain_description(
        #     '/home/klaster/ProFaNA v1.0/important_files/domain_information')
        # genome_id_size_in_gene = self.open_multiple_line(
        #     '/home/klaster/ProFaNA v1.0/important_files/GENOME_ID_SIZE_IN_GENE.txt')
        ################################################################################################################

        ################################################################################################################
        # # VULTR
        domain_information = self.collect_pfam_domain_description(
            "/home/djangoadmin/final_site-project/important_files/domain_information")
        genome_id_size_in_gene = self.open_multiple_line(
            "/home/djangoadmin/final_site-project/important_files/GENOME_ID_SIZE_IN_GENE.txt")
        ################################################################################################################
        print("checkpoint 1")

        genome_id = [x[0] for x in genome_id_size_in_gene]
        size_in_gene = [x[1] for x in genome_id_size_in_gene]

        genome_number_overall = 0
        genome_number_to_stat = 0

        message_for_output = "You have looked for conserved neighbourhood for " + self.user_pfam + \
                             " domain, in range " + str(self.user_distance) + \
                             " bp, in " + self.user_organisms + " database."
        message_for_additional_data = "Pfam domain , PVALUE,  occurence in neighbourhoods, " \
                                      "average occurence in neighbourhood ,occurence genomes, " \
                                      "average occurence in genome, avg DLOK-DGLOB, In what percentage?, " \
                                      "Family, Summary"
        print("checkpoint 2")

        ################################################################################################################
        # # LOCAL
        # file_names = self.open_database(self.user_organisms)
        ################################################################################################################
        ################################################################################################################
        # KLASTER
        # file_names = self.open_database('/home/klaster/ProFaNA v1.0/important_files/database', self.user_organism)
        ################################################################################################################
        ################################################################################################################
        # VULTR
        file_names = self.open_database(self.user_organisms)
        ################################################################################################################

        just_neigh_data = []
        genomes_with_domain = []
        neigh_genome_size = []
        counter = 0
        counter_db = 0
        percentage_counter = Counter()

        print("DLOK TIME START", datetime.datetime.now())
        for file in file_names:
            # print(file)
            counter_db += 1
            counter += 1
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
                                                         domains, contig, genes)
            if len(coords) > 0:
                genome_number_to_stat += 1

            for point in coords:

                if self.user_distance != 0:
                    last_coordinate, first_coordinate, pfam_beg, pfam_end, searched_pfam_orientation = \
                        self.get_range_coordinates(point, self.user_distance)
                    pfam_index_to_neigh = self.get_domains_both_strands(start_coord, end_coord, last_coordinate,
                                                                        first_coordinate, pfam_beg, pfam_end, contig,
                                                                        point)
                else:
                    pfam_index_to_neigh = self.get_domain_both_zeros(genes, point[4])

                genes_in_neigh = self.list_of_genes_in_neigh(genes, pfam_index_to_neigh)
                number_of_genes_in_neigh = self.size_in_genes(genes_in_neigh)
                whole = self.get_list_of_domain_in_neigh(pfam_index_to_neigh, file, domains)
                percentage_counter += Counter(set(whole))
                just_neigh_data.append(whole)
                genomes_with_domain.append(file)
                neigh_genome_size.append((number_of_genes_in_neigh, number_of_genes_in_genome))
        print("DLOK TIME OVER", datetime.datetime.now())
        print("concatenate_domain")



        alls = []
        neigh_counter = Counter()

        for i in just_neigh_data:
            for j in i:
                if j not in alls:
                    alls.append(j)
        genome_counter = Counter()
        print("MATRIX CREATING", datetime.datetime.now())

        counter = 0
        big_data = []
        for domain_list, genome_in_domain, ng_size in zip(just_neigh_data, genomes_with_domain, neigh_genome_size):
            counter += 1
            part = []
            genes, start_coord, end_coord, orientation, domains, contig = self.create_six_list(genome_in_domain)
            genome_domains_counter = Counter(domains)
            genome_counter += genome_domains_counter
            neigh_domains_counter = Counter(domain_list)
            neigh_counter += neigh_domains_counter
            if counter != 100:
                for fine_domain in alls:
                    dlok = neigh_domains_counter[fine_domain] / int(ng_size[0])
                    dglob = genome_domains_counter[fine_domain] / int(ng_size[1])
                    diff = dlok - dglob
                    part.append(str(diff))
                big_data.append(part)

            if counter != 100 and domain_list == just_neigh_data[-1]:
                for place, domain in enumerate(alls):
                    data_to_save = [x[place] for x in big_data]
                    # VULTR
                    with open('/home/djangoadmin/final_site-project/scripts/temp_data/' + domain, 'a+') as output:
                    # LOCAL
                    # with open('/mnt/d/45.76.38.24/final_site-project/scripts/temp_data/' + domain, 'a+') as output:
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

                for place, domain in enumerate(alls):
                    data_to_save = [x[place] for x in big_data]
                    # VULTR
                    with open('/home/djangoadmin/final_site-project/scripts/temp_data/' + domain, 'a+') as output:
                    # LOCAL
                    # with open('/mnt/d/45.76.38.24/final_site-project/scripts/temp_data/' + domain, 'a+') as output:
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
        for i in alls:
            counter += 1
            # VULTR
            data_to_calculate = self.open_singleline_num("/home/djangoadmin/final_site-project/scripts/temp_data/" + i)
            # LOCAL
            # data_to_calculate = self.open_singleline_num("/mnt/d/45.76.38.24/final_site-project/scripts/temp_data/" + i)
            wynik = test(data_to_calculate, zero_method="wilcox")
            mean = sum(data_to_calculate) / len(just_neigh_data)
            scores.append((wynik.pvalue, mean))

        scores_after_correction = self.multiple_test_correction_list(scores,self.user_correction)
        print("Wilcoxon OVER", datetime.datetime.now())
        print("Collecting data START", datetime.datetime.now())
        najlepsze_dane = pd.DataFrame(columns=['PVALUE', 'occurence in neighborhoods',
                                               'average occurence in neighborhood', 'occurence genomes',
                                               'average occurence in genome', 'Density difference',
                                               'In what percentage',
                                               'Family', 'Summary'])





        for domena, wynik, in zip(alls, scores_after_correction):
            if self.user_distance == 0 or self.skip_negative == "no":
                if wynik[1] > 0:
                    najlepsze_dane.at[domena, 'PVALUE'] = wynik[0]
                    najlepsze_dane.at[domena, 'Density difference'] = wynik[1]
                    najlepsze_dane.at[domena, 'In what percentage'] = percentage_counter[domena] / len(just_neigh_data)
                else:
                    najlepsze_dane.at[domena, 'PVALUE'] = 1.0
                    najlepsze_dane.at[domena, 'Density difference'] = wynik[1]
                    najlepsze_dane.at[domena, 'In what percentage'] = percentage_counter[domena] / len(just_neigh_data)
            else:

                if wynik[1] > 0:
                    najlepsze_dane.at[domena, 'PVALUE'] = wynik[0]
                    najlepsze_dane.at[domena, 'Density difference'] = wynik[1]
                    najlepsze_dane.at[domena, 'In what percentage'] = percentage_counter[domena] / len(just_neigh_data)
        for domain in najlepsze_dane.index.to_list():
            najlepsze_dane.at[domain, 'occurence in neighborhoods'] = neigh_counter[domain]
            najlepsze_dane.at[domain, 'average occurence in neighborhood'] = neigh_counter[domain] / len(
                just_neigh_data)
            najlepsze_dane.at[domain, 'occurence genomes'] = genome_counter[domain]
            najlepsze_dane.at[domain, 'average occurence in genome'] = genome_counter[domain] / len(
                set(genomes_with_domain))



        print("Collecting data OVER", datetime.datetime.now())
        print("Customizing_data START", datetime.datetime.now())
        after_cutoff = self.cutoff_value(najlepsze_dane, self.user_cutoff)
        sorted_table = self.sort_table(after_cutoff)
        added_information = self.add_information(sorted_table, domain_information)
        final_data = self.pfam_for_pf(added_information)

        print("Customizing_data OVER", datetime.datetime.now())
        message_down = " In selected database there is {} genomes and in {} searched domain " \
                       "was found".format(str(counter_db), str(genome_number_to_stat))
        self.save_data(self.user_output, message_for_output, message_for_additional_data, message_down, final_data)


# EXAMPLE USEAGE
# if __name__ == "__main__":
#
#     a = SuperSpeedAnalysisFromDomain('pfam04655', 5000, 'alldb', 'none' ,'none', 'both','/media/results/timing.txt' )
#     a.go()
#
#     # # # a.start()