"""
Script created Wednesday September 4th 2019

@uthor: BP Baranowsky
"""

"""
This script is created to make some improvement:
--> Speed up whole process by saving partials and complete output on list of list or dict 
--> Try to save outputs from single neighborhood into file and later on reload to script 
--> Add full description to all functions
--> Delete all unimportant stuff such as printing and create this in next script  
"""

#################################################################################
""" Importing libraries that will be used. """                                  #
                                                                                #
from collections import Counter                                                 #
from scipy.stats import wilcoxon as test                                        #
import numpy as np                                                              #
import pandas as pd                                                             #
from statsmodels.stats.multitest import multipletests as correction             #
import statistics                                                               #
#################################################################################

class NeighbourhoodAnalyzer():
    """ Creating class that will hold all functions. """

    def __init__(self,user_PfamDomain, user_DistanceValue, user_OrganismValue, user_CutOff, user_Correction,
                 user_StrandValue, user_OutputValue):
        """ Initializing input data
            Inputs:
                    user_PfamDomain:  str (from pfam00000 to pfam99999)
                    user_DistanceValue: non negative integer 1-20000
                    user_OrganismValue: str

        """

        self.user_PfamDomain = user_PfamDomain
        self.user_DistanceValue = user_DistanceValue
        self.user_OrganismValue = user_OrganismValue
        self.user_CutOff = user_CutOff
        self.user_Correction = user_Correction
        self.user_StrandValue = user_StrandValue
        self.user_OutputValue = user_OutputValue

    def OpenDirectory(self, path_to_file):
        """ Opens file that contain 1 column and strip it by space. """

        with open(path_to_file + '.txt', 'r') as f:
            file_names = [line.strip() for line in f]
        return file_names

    def SaveComplete(self,file, message_for_output, message_for_additional_data, message_down, complete_data):
        """ Saves all stuff together as one file """
        ## Windows
        #with open(r'E:\project_site\final_site-project\results\test.txt', 'w') as output_file:

        # Linux
        with open('/home/djangoadmin/final_site-project'+file, 'w') as output_file:
            output_file.write(message_for_output)
            output_file.write("\n")
            output_file.write(message_down)
            output_file.write("\n")
            output_file.write(message_for_additional_data)
            output_file.write("\n")
            #output_file.write(complete_data)
            for row in complete_data.iterrows():
                index, data = row
                pre = data.tolist()
                output_file.write(index)
                output_file.write("\t")
                output_file.write("\t".join([str(i) for i in pre]))
                output_file.write("\n")

    def OpenDatabaseFile(self,file_name):
        """ Opens file that contains data about single genome """

        plik=[]
        with open(file_name+".txt") as inputfile:
            for line in inputfile:
                plik.append(line.strip().split())
        return plik

    def OpenFile(self,file_name):
        """ Opens file that contain 2 columns and strip it by space. """

        plik=[]
        with open(file_name+".txt") as inputfile:
            for line in inputfile:
                plik.append(line.strip().split())
        return plik

    def Create6Lists(self,file):
        """ Open single genome file chew it and return 6 lists -> GENE, START_COORD, END_COORDS ,ORIENTATION, DOMAINS """

        data = self.OpenDatabaseFile(file)
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

    def GenomeSizeInGene(self, genome_id, list_of_genome, list_of_size):
        """ Takes genome's id, list of genome and lists with data about how much genes in genome"""

        indeks_genomu = list_of_genome.index(genome_id)
        genome_size_in_gene = list_of_size[indeks_genomu]
        return genome_size_in_gene

    def NeighbourhoodSizeInGenes(self, genome_or_genes):
        """ Takes list of genes and returns size of neighbourhood """

        list_of_genes = []
        for gene in genome_or_genes:
            if gene not in list_of_genes:
                list_of_genes.append(gene)
            else:
                continue
        number_of_genes_in_genome_neigh = len(list_of_genes)
        return number_of_genes_in_genome_neigh

    def ListOfGenesInNeigh(self, list_of_genes, index_list):
        """ Takes overall gene's list in genome and creates complete list of genes in neighbourhood """

        list_of_genes_in_neigh = []
        for pfam_domain in index_list:
            list_of_genes_in_neigh.append(list_of_genes[pfam_domain])
        return list_of_genes_in_neigh

    def SearchingForDomainAndCoordinatesPlusAndMinus(self, pfamValue, start_coord, end_coord, orientation, domains,
                                                     contig):
        """
        Takes user's pfam domain searches through lists contains coordinates,
        orientation, domains, contigs and returns complete data about all
        users' domains in genome
        """

        coords = []
        coords_counter = 0
        for domain in domains:
            one_coords_part = []
            if domain == pfamValue:
                #                print(pfamValue)
                #                print(domain)
                #           searched_pfam_domain = domains[coords_counter]
                orientation_pfam_domain = orientation[coords_counter]
                one_coords_part.append(start_coord[coords_counter])
                one_coords_part.append(end_coord[coords_counter])
                one_coords_part.append(orientation_pfam_domain)
                one_coords_part.append(contig[coords_counter])
                coords.append(one_coords_part)
                coords_counter += 1
            else:
                coords_counter += 1
                continue
        return coords

    def PresenceConfirmation(self, coords, file, pfamValue):
        """
        Just prints out information how many pfam domains is in each genome
        during analysis propably i will have to remove it before putting it to website ...
        """

        if len(coords) == 0:
            print("In genome  " + file + " pfam domain you have been searching do not exist")
        elif len(coords) == 1:
            print("In genome  " + file + " there is " + str(len(coords)) + " " + pfamValue + " domain")
        else:
            print("In genome  " + file + " there are " + str(len(coords)) + " " + pfamValue + " domains")

    def GetRangeCoordinates(self, point, distanceValue):
        """
        Based on how large neighbourhood user wants to analyze creates
        points FROM and TO, additionaly shows where main user's pfam begins and ENDS
        with orientation on strands
        """

        last_coordinate = point[1] + int(distanceValue)
        first_coordinate = point[0] - int(distanceValue)
        pfam_beg = point[0]
        pfam_end = point[1]
        searched_pfam_orientation = point[2]
        return last_coordinate, first_coordinate, pfam_beg, pfam_end, searched_pfam_orientation

    def ReturnIndexesDomainsWhole(self, start_coord, end_coord, last_coordinate, first_coordinate, pfam_beg,
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

    def OpenInformationBoutDomains(self, file):
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

    def ReturnIndexesDomainsStrandSameOposite(self, start_coord, end_coord, last_coordinate, first_coordinate,
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

    def GiveMeListOfDomainsInNeigh(self, pfam_index, file, domains):

        to_counter = []
        party = []
        party.append(file)
        for part in pfam_index:
            party.append(domains[part])
            to_counter.append(domains[part])
        #        neighbourhood_complete.append(party)
        return to_counter

    def SortExtractForPlot(self, counter_neigh):

        counter_sorted = counter_neigh.most_common()
        values_counter = []
        pfam_neigh_domains_counter = []
        for i in counter_sorted:
            values_counter.append(i[1])
            pfam_neigh_domains_counter.append(i[0])
        return values_counter, pfam_neigh_domains_counter

    def DLOK_DGLOBTime(self, some_counter, genome_neigh_size, mighty_domains):

        dlok_glob = []
        for domain_mighty in mighty_domains:
            if domain_mighty in some_counter.keys():
                lok_glob = some_counter.get(domain_mighty) / int(genome_neigh_size)
                dlok_glob.append(lok_glob)
            else:
                dlok_glob.append(0)
        return dlok_glob

########################################################################################################################
    def DataForWilcoxonTest(self, first_list, second_list, matrix, genome, dlok_matrix, dglob_matrix):

        for_wilcoxon = [num_list_first - num_list_second for num_list_first, num_list_second in
                        zip(first_list, second_list)]
        matrix[genome] = for_wilcoxon
        dlok_matrix[genome] = first_list
        dglob_matrix[genome] = second_list

    def AlternativeDataForWilcoxonTest(self, first_list, second_list, alternative_matrix, genome, alternative_dlok_matrix, alternative_dglob_matrix):
        for_wilcoxon = [num_list_first - num_list_second for num_list_first, num_list_second in
                        zip(first_list, second_list)]
        alternative_matrix[genome] = for_wilcoxon
        alternative_dglob_matrix[genome] = second_list
        alternative_dlok_matrix[genome] = first_list

    def List_DataForWicoxonTest(self, first_list, second_list, list_matrix, genome, list_dlok_matrix, list_dglob_matrix):
        for_wilcoxon = [num_list_first - num_list_second for num_list_first, num_list_second in
                        zip(first_list, second_list)]
        list_matrix.append(for_wilcoxon)
        list_dglob_matrix.append(second_list)
        list_dlok_matrix.append(first_list)
########################################################################################################################

########################################################################################################################
    def WilcoxonCalculation(self, matrix):

        scores = []
        print("Calculate data")
        for row in matrix.iterrows():
            index, data = row
            pre = data.tolist()

            post = [x for x in pre]
            try:
                wynik = test(post, zero_method="wilcox")
                scores.append(wynik.pvalue)
            except ValueError:
                scores.append(1.0)

        return scores

    def Alternative_WilcoxonCalculation(self, matrix):
        scores = []
        print("Calculate data")
        for i in range(0, 17929):
            test_values = []
            for k,v in matrix.items():
                test_values.append(v[i])
            try:
                wynik  =test(test_values, zero_method="wilcox")
                scores.append(wynik.pvalue)
            except ValueError:
                scores.append((1.0))
        return scores

    def List_WilcoxonCalculation(self,matrix):
        scores = []
        print("Calculate")
        for i in range(0, 17929):
            test_valuse = [x[i] for x in matrix]
            try:
                wynik = test(test_valuse, zero_method="wilcox")
                scores.append(wynik.pvalue)
            except ValueError:
                scores.append((1.0))
        return scores
########################################################################################################################

########################################################################################################################
    def AvgCalculation(self, some_matrix):

        scores = []
        print("Calculate data")
        for row in some_matrix.iterrows():
            index, data = row
            pre = data.tolist()
            post = [x for x in pre]
            if sum(post) != 0:
                wynik = statistics.mean(post)
                scores.append(wynik)
            else:
                scores.append(0)
        return scores

    def Alternative_AvgCalculation(self,some_matrix):
        scores = []
        print("Calculate data")
        for i in range(0, 17929):
            test_values = []
            for k, v in some_matrix.items():
                test_values.append(v[i])
            if sum(test_values) != 0:
                wynik = statistics.mean(test_values)
                scores.append(wynik)
            else:
                scores.append(0)
        return scores

    def List_AvgCalculation(self,some_matrix):
        scores = []
        print("Calculate data")
        for i in range(0, 17929):
            test_valuse = [x[i] for x in some_matrix]
            if sum(test_valuse) != 0:
                wynik = statistics.mean(test_valuse)
                scores.append(wynik)
            else:
                scores.append(0)
        return scores

    def ZippingScoresAndDiscardingNAN(self, mighty_domains, wyniki):

        all_together = []
        pfam_occurence = []
        for i in zip(mighty_domains, wyniki):
            all_together.append(i)
        for i in all_together:
            if str(i[1]) != 'nan':
                pfam_occurence.append(i[0])
        return all_together, pfam_occurence

########################################################################################################################
    def ZippingAdditionalData(self, mighty_domains, wyniki, pfam_occurence):

        all_together = []
        for i in zip(mighty_domains, wyniki):
            all_together.append(i)
        filter_scores = []
        for i in all_together:
            if str(i[0]) in pfam_occurence:
                filter_scores.append(i)
        return filter_scores

    def CollectAllData(self, filter_scores, genome_dataframe, neigh_dataframe,
                       genome_number_overall, genome_number_to_stat,
                       filter_add_scores_avg_DLOK_DGLOB):

        alternative_complete = pd.DataFrame(columns=['PVALUE',
                                                     'occurence in neighbourhoods',
                                                     'min occurence in neighbourhood',
                                                     'max occurence in neighbourhood',
                                                     'occurence genomes',
                                                     'min occurence in genome',
                                                     'max occurence in genome',
                                                     'Local density',
                                                     'Global density',
                                                     'Density difference',
                                                     'Family', 'Summary'])

        avaible_domains = list(genome_dataframe.columns)
        for pfam in filter_scores:

            domena = pfam[0]
            pfam_value = pfam[1]

            if domena in avaible_domains:
                pfam_pvalue = format(pfam_value, ".3e")
                alternative_complete.at[domena, 'PVALUE'] = pfam_pvalue
                try:
                    list_of_domains_neigh = [x for x in list(neigh_dataframe[domena]) if str(x) != 'nan']
                except KeyError:
                    list_of_domains_neigh = [0, 0, 0, 0, 0]
                sum_neigh = np.sum(list_of_domains_neigh)
                sum_genome = np.sum([x for x in list(genome_dataframe[domena]) if str(x) != 'nan'])
                alternative_complete.at[domena, 'occurence in neighbourhoods'] = sum_neigh
                alternative_complete.at[
                    domena, 'average occurence in neighbourhood'] = sum_neigh / genome_number_overall
                alternative_complete.at[domena, 'min occurence in neighbourhood'] = np.min(list_of_domains_neigh)
                alternative_complete.at[domena, 'max occurence in neighbourhood'] = np.max(list_of_domains_neigh)
                alternative_complete.at[domena, 'occurence genomes'] = sum_genome
                alternative_complete.at[domena, 'average occurence in genome'] = sum_genome / genome_number_overall
                alternative_complete.at[domena, 'min occurence in genome'] = np.min(
                    [x for x in list(genome_dataframe[domena]) if str(x) != 'nan'])
                alternative_complete.at[domena, 'max occurence in genome'] = np.max(
                    [x for x in list(genome_dataframe[domena]) if str(x) != 'nan'])

        for add_data in filter_add_scores_avg_DLOK_DGLOB:
            difference_pfam = add_data[0]
            difference_pvalue = format(add_data[1], ".3e")
            if difference_pfam in avaible_domains:
                alternative_complete.at[difference_pfam, 'Density difference'] = difference_pvalue

        return alternative_complete

    def MultipleTestCorrection(self, some_dataframe, correction_met):

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

    def RemoveNegativeValues(self, some_dataframe):

        domain_list = list(some_dataframe.index)
        for i in domain_list:
            diff = float(some_dataframe.loc[i, 'Density difference'])
            if diff < 0:
                some_dataframe = some_dataframe.drop([i])
        return some_dataframe

    def CutOffValue(self, some_dataframe, cutoff):

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

    def SortData(self, some_dataframe):

        sorted_data = some_dataframe.sort_values('PVALUE', ascending=True)
        return sorted_data

    def AddInfformation(self, some_dataframe, dictionary):

        indeksy = list(some_dataframe.index)
        for i in indeksy:
            pfam = i[0:2] + i[4:]
            family = dictionary[pfam][0]
            summary = dictionary[pfam][1]

            some_dataframe.at[i, 'Family'] = family
            some_dataframe.at[i, 'Summary'] = summary
        return some_dataframe

    def GO(self):
        "Zipping all functions and execute them"

        print('Allright')
        # LINUX

        mighty_domains = self.OpenDirectory('/home/djangoadmin/final_site-project/important_files/LISTA_DOMEN')
        print("Opening domain list")
        GENOME_ID_SIZE_IN_BP = self.OpenFile(
            '/home/djangoadmin/final_site-project/important_files/GENOME_ID_SIZE_IN_BP')
        print("Opening genome size in bp list")
        GENOME_ID_SIZE_IN_GENE = self.OpenFile(
           '/home/djangoadmin/final_site-project/important_files/GENOME_ID_SIZE_IN_GENE')
        print("Opening genome size in gene list")

        # WINDOWS

        #mighty_domains= self.OpenDirectory('E:\\project_site\\final_site-project\\important_files\\LISTA_DOMEN')
        #GENOME_ID_SIZE_IN_BP = self.OpenFile('E:\\project_site\\final_site-project\\important_files\\GENOME_ID_SIZE_IN_BP')
        #GENOME_ID_SIZE_IN_GENE = self.OpenFile('E:\\project_site\\final_site-project\\important_files\\GENOME_ID_SIZE_IN_GENE')


        GENOME_ID = [x[0] for x in GENOME_ID_SIZE_IN_BP]
        SIZE_IN_BP = [x[1] for x in GENOME_ID_SIZE_IN_BP]
        SIZE_IN_GENE = [x[1] for x in GENOME_ID_SIZE_IN_GENE]

        ################################################################################################################
        #dlok_matrix = pd.DataFrame()
        #dglob_matrix = pd.DataFrame()
        #matrix = pd.DataFrame()
        genome_dataframe = pd.DataFrame()
        neigh_dataframe = pd.DataFrame()

        alternative_dlok_matrix = dict()
        alternative_dglob_matrix = dict()
        alternative_matrix = dict()
        alternative_genome_dataframe = dict()
        alternative_neigh_dataframe = dict()

        list_dlok_matrix = []
        list_dglob_matrix = []
        list_matrix = []

        ################################################################################################################


        genome_number_overall = 0
        genome_number_to_stat = 0
        pfam_whole_domain_counter = Counter({})
        pfam_same_strand_domain_counter = Counter({})
        pfam_oposite_strand_domain_counter = Counter({})
        message_for_output = "You have looked for conserved neighbourhood for " + self.user_PfamDomain + " domain, in range " + str(
            self.user_DistanceValue) + " bp, in " + self.user_OrganismValue + " organisms."
        print(message_for_output)
        message_for_additional_data = "Pfam domain , PVALUE,  occurence in neighbourhoods, average occurence in neighbourhood ,min occurence in neighbourhood , max occurence in neighbourhood ,occurence genomes, average occurence in genome, min occurence in genome,  max occurence in genome, avg DLOK-DGLOB, Family, Summary"

        ##############################################################################
        ######################### TAX SELECTION ######################################

        if self.user_OrganismValue == "escherichia":
            tax = "Escherichia"

        elif self.user_OrganismValue == "salmonella":
            tax = "Salmonella"
        elif self.user_OrganismValue == "pseudomonas":
            tax = "Pseudomonas"
        elif self.user_OrganismValue == "staphylococcus":
            tax = "Staphylococcus"
        elif self.user_OrganismValue == "streptococcus":
            tax = "Streptococcus"
        elif self.user_OrganismValue == "mycobacterium":
            tax = "Mycobacterium"
        elif self.user_OrganismValue == "acinetobacter":
            tax = "Acinetobacter"
        elif self.user_OrganismValue == "vibrio":
            tax = "Vibrio"
        elif self.user_OrganismValue == "bacillus":
            tax = "Bacillus"
        elif self.user_OrganismValue == "streptomyces":
            tax = "Streptomyces"
        elif self.user_OrganismValue == "porphyromonas":
            tax = "Porphyromonas"
        elif self.user_OrganismValue == "klebsiella":
            tax = "Klebsiella"
        elif self.user_OrganismValue == "enterococcus":
            tax = "Enterococcus"
        elif self.user_OrganismValue == "burkholderia":
            tax = "Burkholderia"
        elif self.user_OrganismValue == "lactobacillus":
            tax = "Lactobacillus"
        elif self.user_OrganismValue == "campylobacter":
            tax = "Campylobacter"
        elif self.user_OrganismValue == "helicobacter":
            tax = "Helicobacter"
        elif self.user_OrganismValue == "shigella":
            tax = "Shigella"
        elif self.user_OrganismValue == "alldb":
            tax = "Alldb"

        ################################################################################
        # LINUX
        file_names = self.OpenDirectory('/home/djangoadmin/final_site-project/important_files/' + tax)

        #WINDOWS
        #file_names = self.OpenDirectory('E:\\project_site\\final_site-project\\important_files\\'+tax)
        counter = 0
        for file in file_names:

            try:
                genes, start_coord, end_coord, orientation, domains, contig = self.Create6Lists(file)

            except FileNotFoundError:
                continue

            # LINUX
            file_name_raw = file.split('/')
            tax_name = file_name_raw[-1]

            #WINDOWS
            #file_name_raw = file.split('\\')
            #tax_name = file_name_raw[-1]


            genome_number_overall += 1
            number_of_genes_in_genome = self.GenomeSizeInGene(tax_name, GENOME_ID, SIZE_IN_GENE)
            genome_domains_counter = Counter(domains)
            coords = self.SearchingForDomainAndCoordinatesPlusAndMinus(self.user_PfamDomain, start_coord, end_coord,
                                                                       orientation, domains, contig)
            self.PresenceConfirmation(coords, file, self.user_PfamDomain)
            D_GLOB = self.DLOK_DGLOBTime(genome_domains_counter, number_of_genes_in_genome, mighty_domains)

            if len(coords) > 0:
                genome_number_to_stat += 1
                genome_dataframe = genome_dataframe.append(genome_domains_counter, ignore_index=True)

            for point in coords:
                counter +=1
                last_coordinate, first_coordinate, pfam_beg, pfam_end, searched_pfam_orientation = self.GetRangeCoordinates(
                    point, self.user_DistanceValue)
                pfam_index_to_neigh = self.ReturnIndexesDomainsWhole(start_coord, end_coord, last_coordinate,
                                                                     first_coordinate, pfam_beg, pfam_end, contig,
                                                                     point)
                pfam_index_to_neigh_same_strand, pfam_index_to_neigh_oposite_strand = self.ReturnIndexesDomainsStrandSameOposite(
                    start_coord, end_coord, last_coordinate, first_coordinate, pfam_beg, pfam_end, contig, point,
                    orientation)
                genes_in_neigh = self.ListOfGenesInNeigh(genes, pfam_index_to_neigh)
                number_of_genes_in_neigh = self.NeighbourhoodSizeInGenes(genes_in_neigh)

                whole = self.GiveMeListOfDomainsInNeigh(pfam_index_to_neigh, file, domains)
                neighbourhood_domains_counter = Counter(whole)
                neigh_dataframe = neigh_dataframe.append(neighbourhood_domains_counter, ignore_index=True)

                D_LOK = self.DLOK_DGLOBTime(neighbourhood_domains_counter, number_of_genes_in_neigh, mighty_domains)
                same_strand = self.GiveMeListOfDomainsInNeigh(pfam_index_to_neigh_same_strand, file, domains)
                oposite_strand = self.GiveMeListOfDomainsInNeigh(pfam_index_to_neigh_oposite_strand, file, domains)
                pfam_same_strand_domain_counter += Counter(same_strand)
                pfam_oposite_strand_domain_counter += Counter(oposite_strand)
                pfam_whole_domain_counter += Counter(whole)
                #self.DataForWilcoxonTest(D_LOK, D_GLOB, matrix, str(counter), dlok_matrix, dglob_matrix)
                #self.AlternativeDataForWilcoxonTest(D_LOK, D_GLOB, alternative_matrix, file, alternative_dlok_matrix, alternative_dglob_matrix)
                self.List_DataForWicoxonTest(D_LOK, D_GLOB,list_matrix,str(counter), list_dlok_matrix, list_dglob_matrix)
        values_counter_whole_neigh, pfam_whole_neigh_domain_counter = self.SortExtractForPlot(pfam_whole_domain_counter)
        values_counter_same_strand_neigh, pfam_same_strand_neigh_domain_counter = self.SortExtractForPlot(
            pfam_same_strand_domain_counter)
        values_counter_oposite_strand_neigh, pfam_oposite_strand_neigh_domain_counter = self.SortExtractForPlot(
            pfam_oposite_strand_domain_counter)


        ################################################################################################################
        #wyniki = self.WilcoxonCalculation(matrix)
        #avg_DLOK_DGLOB = self.AvgCalculation(matrix)
        #avg_DLOK = self.AvgCalculation(dlok_matrix)
        #avg_DGLOB = self.AvgCalculation(dglob_matrix)

        alternative_wyniki = self.Alternative_WilcoxonCalculation(alternative_matrix)
        alternative_avg_DLOK_DGLOB = self.Alternative_AvgCalculation(alternative_matrix)
        #alternative_avg_DLOK = self.Alternative_AvgCalculation(alternative_dlok_matrix)
        #alternative_avg_DGLOB = self.Alternative_AvgCalculation(alternative_dglob_matrix)

        #list_wyniki = self.List_WilcoxonCalculation(list_matrix)
        #list_avg_DLOK_DGLOB = self.List_AvgCalculation(list_matrix)
        #list_avg_DLOK = self.List_AvgCalculation(list_dlok_matrix)
        #list_avg_DGLOB = self.List_AvgCalculation(list_dglob_matrix)
        ###############################################################################################################
        ###############################################################################################################

        #filter_scores, pfam_occurence = self.ZippingScoresAndDiscardingNAN(mighty_domains, wyniki)
        #filter_add_scores_avg_DLOK_DGLOB = self.ZippingAdditionalData(mighty_domains, avg_DLOK_DGLOB, pfam_occurence)
        #filter_add_scores_avg_DGLOB = self.ZippingAdditionalData(mighty_domains, avg_DGLOB, pfam_occurence)
        #filter_add_scores_avg_DLOK = self.ZippingAdditionalData(mighty_domains, avg_DLOK, pfam_occurence)

        filter_scores, pfam_occurence = self.ZippingScoresAndDiscardingNAN(mighty_domains, alternative_wyniki)
        filter_add_scores_avg_DLOK_DGLOB = self.ZippingAdditionalData(mighty_domains, alternative_avg_DLOK_DGLOB, pfam_occurence)
        #filter_add_scores_avg_DGLOB = self.ZippingAdditionalData(mighty_domains, alternative_avg_DGLOB, pfam_occurence)
        #filter_add_scores_avg_DLOK = self.ZippingAdditionalData(mighty_domains, alternative_avg_DLOK, pfam_occurence)

        #filter_scores, pfam_occurence = self.ZippingScoresAndDiscardingNAN(mighty_domains, list_wyniki)
        #filter_add_scores_avg_DLOK_DGLOB = self.ZippingAdditionalData(mighty_domains, list_avg_DLOK_DGLOB, pfam_occurence)
        #filter_add_scores_avg_DGLOB = self.ZippingAdditionalData(mighty_domains, list_avg_DGLOB, pfam_occurence)
        #filter_add_scores_avg_DLOK = self.ZippingAdditionalData(mighty_domains, list_avg_DLOK, pfam_occurence)

        ###############################################################################################################

        message_down = "In my database there was " + str(
            genome_number_overall) + " " + self.user_OrganismValue + " genomes and in " + str(
            genome_number_to_stat) + " searched domain was found"

        alternative_complete = self.CollectAllData(filter_scores, genome_dataframe,
                                                   neigh_dataframe,
                                                   genome_number_overall,
                                                   genome_number_to_stat,
                                                   filter_add_scores_avg_DLOK_DGLOB)

        after_testcorrection = self.MultipleTestCorrection(alternative_complete, self.user_Correction)
        without_minuses = self.RemoveNegativeValues(after_testcorrection)
        aftercutoff = self.CutOffValue(without_minuses, self.user_CutOff)
        complete_output = self.SortData(aftercutoff)
        domain_information = self.OpenInformationBoutDomains(
            '/home/djangoadmin/final_site-project/important_files/domain_information')
        with_information = self.AddInfformation(complete_output, domain_information)
        self.SaveComplete(self.user_OutputValue, message_for_output, message_for_additional_data,
                          message_down, aftercutoff)

"""
if __name__ == "__main__":
    a = NeighbourhoodAnalyzer('pfam02696', 5000, 'escherichia', 'none' ,'none', 'both','timing' )
    a.GO()
"""