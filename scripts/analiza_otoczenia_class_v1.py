"""
Script created Wend Jan 9 2019

@uthor: BP Baranowsky
"""

"""
###
The main reason why this script was created is to easyly import all of functions to website and use them so it has no data validations or so.
Data valitation will be achived by other script.
###
Important files:
-> List of domains (all of existed) -> LISTA_DOMEN.txt
-> Lists of genomes that we want to analyze, now it will be only Escherichia sp. later: Salmonella sp., Pseudomonas sp. Staphylococcus sp.  -> E_COLA.text
-> List of genomes with data about genome's size in basepairs -> GENOME_ID_SIZE_IN_BP.txt (currently not used)
-> List of genomes with data about genome's size in gene -> GENOME_ID_SIZE_IN_GENE.txt (currently used in script)
-> Genome data files in one folder


In this version of software we are analysing neighbourhood based on their membership to contigs, so we are changing:

-> Create5Lists() to Create6Lists() V
-> Opening pfam domain's file through function  V
-> def SearchingForDomainAndCoordinatesPlusAndMinus() additionally returns also contigs
-> def ReturnIndexesDomainsStrandSameOposite()  additionally takes data about contigs and returns unique index odatkowo bierze pod uwage numer kontigu oraz unikalnie wrzuca indexy V
-> def ReturnIndexesDomainsWhole() additionally takes data about contigs and returns unique index odatkowo bierze pod uwage numer kontigu oraz unikalnie wrzuca indexy V
-> Opening genome's list through function and we used that data to gather information about genome size


Ideas to do :
-> merge files (GENOME_ID_SIZE_IN_BP + GENOME_ID_SIZE_IN_GENE) and save some time and space
-> create option to analyze different strands
-> choosig  which direction we want to analyze neighbourhood after or before main domain


Important stuff to do :
-> message in save
-> check folders in data open and save functions
-> think carefully about function NeighbourhoodSizeInGenes propably it is not needed

"""

################################################################################
""" Importing libraries that will be used. """

from collections import Counter
#from matplotlib import pyplot as plt
import time
import sys
from scipy.stats import wilcoxon as test


#import pdb
################################################################################

""" Creating class that will hold all functions. """

class NeighbourhoodAnalyzer():

    path_to_project = 'F:/backup_dyskowy/DJANGO/DJANGO2/projects_site-project/'
    """ Initializing input data """
    def __init__(self,user_PfamDomain,user_DistanceValue, user_OrganismValue, user_ChartValue, user_OutputValue):

        self.user_PfamDomain = user_PfamDomain
        self.user_DistanceValue = user_DistanceValue
        self.user_OrganismValue = user_OrganismValue
        self.user_ChartValue = user_ChartValue
        self.user_OutputValue = user_OutputValue

    """ Opens file that contain 1 column and strip it by space. """
    def OpenDirectory(self, file_name):
        file_names=[]
        with open(NeighbourhoodAnalyzer.path_to_project + "files_for_tools/neigh_analy/core_files/"+file_name +'.txt', 'r') as f:
            file_names = [line.strip() for line in f]
        return file_names

    """ Saves final output file with message above values. """
    def SaveOutput(self,file,all_together,message_for_output):
        with open(NeighbourhoodAnalyzer.path_to_project + "files_for_tools/neigh_analy/results_file/"+file+'.txt' , 'w') as output_file:
            output_file.write(message_for_output)
            output_file.write("\n")
            for line in all_together:
                output_file.write(" ".join([str(i) for i in line]))
                output_file.write("\n")

    """ SAVE FOR /media/ """
    def SaveOutputMedia(self,file,all_together,message_for_output):
        with open('F:/backup_dyskowy/DJANGO/DJANGO2/projects_site-project/media/'+file+'.txt' , 'w') as output_file:
            output_file.write(message_for_output)
            output_file.write("\n")
            for line in all_together:
                output_file.write(" ".join([str(i) for i in line]))
                output_file.write("\n")

    """ Opens file that contains data about single genome """
    def OpenDatabaseFile(self,file_name):
        plik=[]
        with open(NeighbourhoodAnalyzer.path_to_project + "files_for_tools/neigh_analy/database_file/"+file_name+".txt") as inputfile:
            for line in inputfile:
                plik.append(line.strip().split())
        return plik

    """ Opens file that contain 2 columns and strip it by space. """
    def OpenFile(self,file_name):
        plik=[]
        with open(NeighbourhoodAnalyzer.path_to_project + "files_for_tools/neigh_analy/core_files/" + file_name+".txt") as inputfile:
            for line in inputfile:
                plik.append(line.strip().split())
        return plik

    """ Open single genome file chew it and return 6 lists -> GENE, START_COORD, END_COORDS ,ORIENTATION, DOMAINS """
    def Create6Lists(self,file):
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

    """ Takes genome's id, list of genome and lists with data about how much genes in genome"""
    def GenomeSizeInGene(self,genome_id, list_of_genome, list_of_size):
        indeks_genomu = list_of_genome.index(genome_id)
        genome_size_in_gene = list_of_size[indeks_genomu]
        return genome_size_in_gene

    """ Takes list of genes and returns size of neighbourhood """
    def NeighbourhoodSizeInGenes(self, genome_or_genes):
        list_of_genes = []
        for gene in genome_or_genes:
            if gene not in list_of_genes:
                list_of_genes.append(gene)
            else:
                continue
        number_of_genes_in_genome_neigh = len(list_of_genes)
        return number_of_genes_in_genome_neigh

    """ Takes overall gene's list in genome and creates complete list of genes in neighbourhood """
    def ListOfGenesInNeigh(self, list_of_genes,index_list):
        list_of_genes_in_neigh = []
        for pfam_domain in index_list:
            list_of_genes_in_neigh.append(list_of_genes[pfam_domain])
        return list_of_genes_in_neigh

    """
    Takes user's pfam domain searches through lists contains coordinates,
    orientation, domains, contigs and returns complete data about all
    users' domains in genome
    """
    def SearchingForDomainAndCoordinatesPlusAndMinus(self,pfamValue, start_coord,end_coord, orientation, domains, contig):
        coords = []
        coords_counter = 0
        for domain in domains:
            one_coords_part = []
            if domain == pfamValue:
                #print(pfamValue)
                #print(domain)
    #           searched_pfam_domain = domains[coords_counter]
                orientation_pfam_domain = orientation[coords_counter]
                one_coords_part.append(start_coord[coords_counter])
                one_coords_part.append(end_coord[coords_counter])
                one_coords_part.append(orientation_pfam_domain)
                one_coords_part.append(contig[coords_counter])
                coords.append(one_coords_part)
                coords_counter +=1
            else:
                coords_counter +=1
                continue
        return coords

    """
    Just prints out information how many pfam domains is in each genome
    during analysis propably i will have to remove it before putting it to website ...
    """
    def PresenceConfirmation(self,coords,file,pfamValue):
        if len(coords) == 0:
            print("In genome  " + file + " pfam domain you have been searching do not exist")
        elif len(coords) == 1:
            print("In genome  " + file + " there is " + str(len(coords)) +" "+ pfamValue + " domain")
        else:
            print("In genome  " + file + " there are " + str(len(coords)) +" "+ pfamValue + " domains")

    """
    Based on how large neighbourhood user wants to analyze creates
    points FROM and TO, additionaly shows where main user's pfam begins and ENDS
    with orientation on strands
    """
    def GetRangeCoordinates(self,point,distanceValue):
        last_coordinate = point[1] + int(distanceValue)
        first_coordinate = point[0] - int(distanceValue)
        pfam_beg =point[0]
        pfam_end = point[1]
        searched_pfam_orientation = point[2]
        return last_coordinate, first_coordinate,pfam_beg, pfam_end , searched_pfam_orientation

    def ReturnIndexesDomainsWhole(self,start_coord,end_coord,last_coordinate,first_coordinate,pfam_beg, pfam_end,contig,point):
        pfam_index_to_neigh = []
        s_coord_counter=0
        for s_coord in start_coord:
            if s_coord <= last_coordinate and s_coord >= pfam_beg and contig[s_coord_counter] == point[3] and s_coord_counter not in pfam_index_to_neigh :
                pfam_index_to_neigh.append(s_coord_counter)
                s_coord_counter +=1
            else:
                s_coord_counter +=1
                continue
        e_coord_counter = 0
        for e_coord in end_coord:
            if e_coord >= first_coordinate and e_coord <= pfam_end and contig[e_coord_counter] == point[3]and e_coord_counter not in pfam_index_to_neigh :
                pfam_index_to_neigh.append(e_coord_counter)
                e_coord_counter +=1
            else:
                e_coord_counter +=1
                continue
        return pfam_index_to_neigh

    def ReturnIndexesDomainsStrandSameOposite(self,start_coord,end_coord,last_coordinate,first_coordinate,pfam_beg, pfam_end,contig,point,orientation):
        pfam_index_to_neigh_same_strand = []
        pfam_index_to_neigh_oposite_strand= []
        s_coord_counter=0
        for s_coord in start_coord:
            if s_coord <= last_coordinate and s_coord >= pfam_beg and orientation[s_coord_counter] == point[2] and contig[s_coord_counter] == point[3] and s_coord_counter not in pfam_index_to_neigh_same_strand:
                pfam_index_to_neigh_same_strand.append(s_coord_counter)
                s_coord_counter +=1
            elif s_coord <= last_coordinate and s_coord >= pfam_beg and orientation[s_coord_counter] != point[2] and contig[s_coord_counter] == point[3] and s_coord_counter not in pfam_index_to_neigh_oposite_strand:
                pfam_index_to_neigh_oposite_strand.append(s_coord_counter)
                s_coord_counter +=1
            else:
                s_coord_counter +=1
                continue
        e_coord_counter = 0
        for e_coord in end_coord:
            if e_coord >= first_coordinate and e_coord <= pfam_end and orientation[e_coord_counter] == point[2] and contig[e_coord_counter] == point[3] and e_coord_counter not in pfam_index_to_neigh_same_strand:
                pfam_index_to_neigh_same_strand.append(e_coord_counter)
                e_coord_counter +=1
            elif e_coord >= first_coordinate and e_coord <= pfam_end and orientation[e_coord_counter] != point[2] and contig[e_coord_counter] == point[3] and e_coord_counter not in pfam_index_to_neigh_oposite_strand:
                pfam_index_to_neigh_oposite_strand.append(e_coord_counter)
                e_coord_counter +=1
            else:
                e_coord_counter +=1
                continue
        return pfam_index_to_neigh_same_strand, pfam_index_to_neigh_oposite_strand

    def GiveMeListOfDomainsInNeigh(self, pfam_index,file,domains):
            to_counter = []
            party = []
            party.append(file)
            for part in pfam_index:
                party.append(domains[part])
                to_counter.append(domains[part])
    #        neighbourhood_complete.append(party)
            return to_counter

    def SortExtractForPlot(self, counter_neigh):
        counter_sorted =counter_neigh.most_common()
        values_counter = []
        pfam_neigh_domains_counter = []
        for i in counter_sorted:
            values_counter.append(i[1])
            pfam_neigh_domains_counter.append(i[0])
        return values_counter, pfam_neigh_domains_counter

    def DLOK_DGLOBTime(self, some_counter,genome_neigh_size,mighty_domains):
        dlok_glob = []
        for domain_mighty in mighty_domains:
            if domain_mighty in some_counter.keys():
                lok_glob = some_counter.get(domain_mighty)/int(genome_neigh_size)
                dlok_glob.append(lok_glob)
            else:
                dlok_glob.append(0)
        return dlok_glob

    def DataForWilcoxonTest(self, first_list, second_list,matrix):

        for_wilcoxon = [num_list_first - num_list_second for num_list_first, num_list_second in zip(first_list,second_list)]
        matrix.append(for_wilcoxon)


    def Ploting(self, values,pfam,rotation,chartValue):
        #plt.xticks(range(len(pfam[:int(chartValue)])),pfam[:int(chartValue)], rotation = rotation)
    #    plt.title("Occurence of 20 most common domains in "+ pfam_domain+" neighbourhood" )
        #plt.bar(range(len(pfam[:int(chartValue)])), list(map(float, values[:int(chartValue)])))
    #    plt.show()
        pass
    def WilcoxonCalculation(self,matrix):
        wyniki = []
        testowo = list(range(0, 17929))
        #print("Calculate data")
        for i in testowo:
            do_testu = []
            for j in matrix:
                if j[i] > 0:
                    do_testu.append(j[i])

            t= test(do_testu, zero_method='wilcox')
            wyniki.append(t.pvalue)
        return wyniki

    def ZippingScoresAndDiscardingNAN(self, mighty_domains, wyniki):
        all_together = []
        for i in zip(mighty_domains,wyniki):
            all_together.append(i)
        filter_scores = []
        for i in all_together:
            if str(i[1]) != 'nan':
                filter_scores.append(i)
        return filter_scores


################################################################################


    def GO(self):

        mighty_domains= self.OpenDirectory('LISTA_DOMEN')
        #print("Opening domain list")
        GENOME_ID_SIZE_IN_BP = self.OpenFile('GENOME_ID_SIZE_IN_BP')
        #print("Opening genome size in bp list")
        GENOME_ID_SIZE_IN_GENE = self.OpenFile('GENOME_ID_SIZE_IN_GENE')
        #print("Opening genome size in gene list")
        GENOME_ID = [x[0] for x in GENOME_ID_SIZE_IN_BP]
        SIZE_IN_BP = [x[1] for x in GENOME_ID_SIZE_IN_BP]
        SIZE_IN_GENE = [x[1] for x in GENOME_ID_SIZE_IN_GENE]
        matrix = []
        pfam_whole_domain_counter = Counter({})
        pfam_same_strand_domain_counter = Counter({})
        pfam_oposite_strand_domain_counter = Counter({})
        message_for_output = "You have looked for conserved neighbourhood for "+self.user_PfamDomain+" domain, in range "+str(self.user_DistanceValue)+" bp, in "+self.user_OrganismValue+ " organisms. Bellow are your scores :"
        #print(message_for_output)

    ################################################################################



        if self.user_OrganismValue in  ["escherichia", "escherichia sp."]:
            file_names = self.OpenDirectory("E_COLA")
        elif self.user_OrganismValue in  ["salmonella", "salmonella sp."]:
            file_names = self.OpenDirectory("E_COLA")
        elif self.user_OrganismValue in  ["pseudomonas", "pseudomonas sp."]:
            file_names = self.OpenDirectory("E_COLA")
        elif self.user_OrganismValue in  ["all", "everything"]:
            file_names = self.OpenDirectory("E_COLA")
        else :
            file_names = self.OpenDirectory("E_COLA")
            #print("Opening organisms list")

        ################################################################################


        for file in file_names:
            try:
                genes, start_coord,end_coord, orientation, domains, contig = self.Create6Lists(file)
            except FileNotFoundError:
                continue
            number_of_genes_in_genome = self.GenomeSizeInGene(file, GENOME_ID, SIZE_IN_GENE)
            genome_domains_counter = Counter(domains)
            coords = self.SearchingForDomainAndCoordinatesPlusAndMinus(self.user_PfamDomain, start_coord,end_coord, orientation, domains, contig)
            #self.PresenceConfirmation(coords,file,self.user_PfamDomain)
            D_GLOB = self.DLOK_DGLOBTime(genome_domains_counter,number_of_genes_in_genome,mighty_domains)
            for point in coords:
                last_coordinate, first_coordinate,pfam_beg,pfam_end,searched_pfam_orientation = self.GetRangeCoordinates(point,self.user_DistanceValue)
                pfam_index_to_neigh = self.ReturnIndexesDomainsWhole(start_coord,end_coord,last_coordinate,first_coordinate,pfam_beg, pfam_end,contig,point)
                pfam_index_to_neigh_same_strand, pfam_index_to_neigh_oposite_strand = self.ReturnIndexesDomainsStrandSameOposite(start_coord,end_coord,last_coordinate,first_coordinate,pfam_beg, pfam_end,contig,point,orientation)
                genes_in_neigh = self.ListOfGenesInNeigh(genes,pfam_index_to_neigh)
                number_of_genes_in_neigh = self.NeighbourhoodSizeInGenes(genes_in_neigh)
                whole = self.GiveMeListOfDomainsInNeigh(pfam_index_to_neigh,file,domains)
                neighbourhood_domains_counter = Counter(whole)
                D_LOK = self.DLOK_DGLOBTime(neighbourhood_domains_counter,number_of_genes_in_neigh,mighty_domains)
                same_strand = self.GiveMeListOfDomainsInNeigh(pfam_index_to_neigh_same_strand,file,domains)
                oposite_strand = self.GiveMeListOfDomainsInNeigh(pfam_index_to_neigh_oposite_strand,file,domains)
                pfam_same_strand_domain_counter += Counter(same_strand)
                pfam_oposite_strand_domain_counter += Counter(oposite_strand)
                pfam_whole_domain_counter += Counter(whole)
                self.DataForWilcoxonTest(D_LOK,D_GLOB,matrix)


        values_counter_whole_neigh, pfam_whole_neigh_domain_counter = self.SortExtractForPlot(pfam_whole_domain_counter)
        values_counter_same_strand_neigh, pfam_same_strand_neigh_domain_counter = self.SortExtractForPlot(pfam_same_strand_domain_counter)
        values_counter_oposite_strand_neigh, pfam_oposite_strand_neigh_domain_counter = self.SortExtractForPlot(pfam_oposite_strand_domain_counter)
#        pdb.set_trace()
        #plt.subplot(3,1,1)
        #self.Ploting(values_counter_whole_neigh,pfam_whole_neigh_domain_counter,10, self.user_ChartValue)
        #plt.subplot(3,1,2)
        #self.Ploting(values_counter_same_strand_neigh,pfam_same_strand_neigh_domain_counter,10, self.user_ChartValue)
        #plt.subplot(3,1,3)
        #self.Ploting(values_counter_oposite_strand_neigh,pfam_oposite_strand_neigh_domain_counter,10,self.user_ChartValue)
        #plt.show()

        wyniki = self.WilcoxonCalculation(matrix)
        filter_scores = self.ZippingScoresAndDiscardingNAN(mighty_domains, wyniki)

        ################################################################################

        #print("File " + self.user_OutputValue + " saving")
        self.SaveOutput(self.user_OutputValue,filter_scores,message_for_output)
        self.SaveOutputMedia(self.user_OutputValue,filter_scores,message_for_output)
        return filter_scores
        #print("Task complete !")


################################################################################

""" Example of usage """

#a = NeighbourhoodAnalyzer('pfam02696', 5000, 'all', 10 ,'class_test' )
#a.GO()
