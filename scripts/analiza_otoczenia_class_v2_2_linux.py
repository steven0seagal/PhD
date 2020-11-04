"""
Script created Wend Jan 9 2019

@uthor: BP Baranowsky
"""

"""

###
Difference between this and old one is that this script generates complete raport in one files. And works only on one database
###

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
import pdb
import numpy as np
import pandas as pd
from statsmodels.stats.multitest import multipletests as correction
################################################################################

""" Creating class that will hold all functions. """

class NeighbourhoodAnalyzer():

    """ Initializing input data """
    def __init__(self,user_PfamDomain,user_DistanceValue, user_OrganismValue, user_CutOff, user_Correction,user_StrandValue, user_OutputValue):

        self.user_PfamDomain = user_PfamDomain
        self.user_DistanceValue = user_DistanceValue
        self.user_OrganismValue = user_OrganismValue
        self.user_CutOff = user_CutOff
        self.user_Correction = user_Correction
        self.user_StrandValue = user_StrandValue
        self.user_OutputValue = user_OutputValue

    """ Opens file that contain 1 column and strip it by space. """
    def OpenDirectory(self, file_name):
        file_names=[]
        with open(file_name +'.txt', 'r') as f:
            file_names = [line.strip() for line in f]
        return file_names
#####################################################################################################
#   FOR DIAGNOSTICS PURPOSE ONLY
#   """ Saves final output file with message above values. """                                     #
#    def SaveOutput(self,file,all_together,message_for_output):                                     #
#        with open("results//"+file+'.txt' , 'w') as output_file:                                   #
#            output_file.write(message_for_output)
#            output_file.write("\n")
#            for line in all_together:
#                output_file.write(" ".join([str(i) for i in line]))
#                output_file.write("\n")
#
#    "FOR SAVING ADDITIONAL DATA "
#    def SaveOutputAddData(self,file,additional_data,message_for_additional_data, message_down):
#        with open("results//"+file+'_additional.txt' , 'w') as output_file:
#            output_file.write(message_down)
#            output_file.write("\n")
#            output_file.write(message_for_additional_data)
#            output_file.write("\n")
#            for line in additional_data:
#                output_file.write("\t".join([str(i) for i in line]))
#                output_file.write("\n")

    def MiddleSave(self, part):
        with open("/home/klaster/neighborhood_analyzer/results/crossroad.txt" , 'a') as output_file:
            output_file.write(" ".join([str(i) for i in part]))
            output_file.write("\n")
        

#####################################################################################################
    def SaveComplete(self,file, message_for_output,message_for_additional_data, message_down,complete_data):
        with open('/home/djangoadmin/'+file+'_complete_output.txt' , 'w') as output_file:
            output_file.write(message_for_output)
            output_file.write("\n")
            output_file.write(message_down)
            output_file.write("\n")
            output_file.write(message_for_additional_data)
            output_file.write("\n")
            #output_file.write(complete_data)
            for row in complete_data.iterrows():
                index,data = row
                pre=  data.tolist()
                output_file.write("\t".join([str(i) for i in pre]))
                output_file.write("\n")  
            
            #for line in complete_data:
            #    output_file.write("\t".join([str(i) for i in line]))
            #    output_file.write("\n")

    """ Opens file that contains data about single genome """
    def OpenDatabaseFile(self,file_name):
        plik=[]
        with open(file_name+".txt") as inputfile:
            for line in inputfile:
                plik.append(line.strip().split())
        return plik

    """ Opens file that contain 2 columns and strip it by space. """
    def OpenFile(self,file_name):
        plik=[]
        with open(file_name+".txt") as inputfile:
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
#                print(pfamValue)
#                print(domain)
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

    def DataForWilcoxonTest(self, first_list, second_list):
        matrix = [] 
        for_wilcoxon = [num_list_first - num_list_second for num_list_first, num_list_second in zip(first_list,second_list)]
        matrix.append(for_wilcoxon)
        return matrix

    #def Ploting(self, values,pfam,rotation,chartValue):
       # plt.xticks(range(len(pfam[:int(chartValue)])),pfam[:int(chartValue)], rotation = rotation)
    #    plt.title("Occurence of 20 most common domains in "+ pfam_domain+" neighbourhood" )
        #plt.bar(range(len(pfam[:int(chartValue)])), list(map(float, values[:int(chartValue)])))
    #    plt.show()
####################################################################################################################
#    def CollectAddData(self,final_list,genome_counter, neigh_counter,genome_number_overall,genome_number_to_stat):
#        additional = []
#
#        for pfam in final_list:
#            domena = pfam[0]
#            part = []
#            part.append(domena)
#            #pdb.set_trace()
#            sum_neigh = np.sum([x for x in list(neigh_counter[domena]) if str(x) != 'nan'])
#            sum_genome = np.sum([x for x in list(genome_counter[domena]) if str(x) != 'nan'])
#            part.append(sum_neigh)
#            part.append(sum_neigh/genome_number_overall)
#            part.append(np.min([x for x in list(neigh_counter[domena]) if str(x) != 'nan']))
#            part.append(np.max([x for x in list(neigh_counter[domena]) if str(x) != 'nan']))
#            part.append(sum_genome)
#            part.append(sum_genome/genome_number_overall)
#            part.append(np.min([x for x in list(genome_counter[domena]) if str(x) != 'nan']))
#            part.append(np.max([x for x in list(genome_counter[domena]) if str(x) != 'nan']))
#            additional.append(part)
#
#        return(additional)
##################################################################################################
    def CollectAllData(self, final_list, genome_counter, neigh_counter, genome_number_overall,genome_number_to_stat):
        complete = []
        counter = 0
        for pfam in final_list:


            domena = pfam[0]
            part = []
            part.append(domena)
            pfam_pvalue = format(float(final_list[counter][1]), ".3e") 
            part.append(pfam_pvalue)
            counter+=1
            
            #pdb.set_trace()
            try:
                list_of_domains_neigh = [x for x in list(neigh_counter[domena])if str(x) != 'nan']
            except KeyError:
                list_of_domains_neigh = [0,0,0,0,0]


            sum_neigh = np.sum(list_of_domains_neigh)
            sum_genome = np.sum([x for x in list(genome_counter[domena]) if str(x) != 'nan'])
            part.append(sum_neigh)
            part.append(sum_neigh/genome_number_overall)
            part.append(np.min(list_of_domains_neigh))
            part.append(np.max(list_of_domains_neigh))
            part.append(sum_genome)
            part.append(sum_genome/genome_number_overall)
            part.append(np.min([x for x in list(genome_counter[domena]) if str(x) != 'nan']))
            part.append(np.max([x for x in list(genome_counter[domena]) if str(x) != 'nan']))
            complete.append(part)


        return(complete)
    def CreateDataFrame(self, complete_data):

        "CREATING DATAFRAME"
        dataframe= pd.DataFrame(data = complete_data, columns = ['Pfam domain' , 'PVALUE',  'sum in neighbourhood', 'average in neighbourhood' ,'min in neighbourhood' , 'max in neighbourhood' ,'sum in genome', 'average in genome', 'min in genome',  'max in genome'])

        "SORTING BY PVALUE"
        dataframe['PVALUE'] = dataframe['PVALUE'].astype(float)
        dataframe_sortred = dataframe.sort_values('PVALUE', ascending = True)

        "MAKING STUFF SIMPLE"
        dataframe_sortred[['sum in neighbourhood','min in neighbourhood','max in neighbourhood','min in genome',  'max in genome','sum in genome']] = dataframe_sortred[['sum in neighbourhood','min in neighbourhood','max in neighbourhood','min in genome',  'max in genome','sum in genome']].astype(int)

        return(dataframe_sortred)

    def CutOffValue(self, some_dataframe, cutoff):
        if cutoff == 'none':
            return some_dataframe
        elif cutoff == '0':
            for row in some_dataframe.iterrows():
                index,data = row 
                if float(data[1]) >= float(cutoff):
                    some_dataframe = some_dataframe.drop(index = index)
            return some_dataframe
        else:
            for row in some_dataframe.iterrows():
                index,data = row 
                if float(data[1]) > float(cutoff):
                    some_dataframe = some_dataframe.drop(index = index)
            return some_dataframe
    def MultipleTestCorrection(self, some_dataframe, correction_met ):
        if correction_met == 'none': 
            return some_dataframe
        else:
            value_to_correct = some_dataframe.PVALUE.tolist()
            reject, pvals_corrected, alphaSidak, alphaBonf = correction(pvals =value_to_correct, method=correction_met, is_sorted=False, returnsorted=False)
            pvals = pvals_corrected.tolist()
            some_dataframe.PVALUE = pvals
            return some_dataframe
        


    def WilcoxonCalculation(self,matrix):
#        scores = []
#        print("Calculate data")
#        for row in matrix.iterrows():
#            index,data = row
#            pre=  data.tolist()
#            post = [x for x in pre if x >0]
#            wynik = test(post, zero_method="wilcox")
#            scores.append(wynik.pvalue)
#        return scores
        wyniki = []         
        testowo = list(range(0, 17929))
        
        for i in testowo:
            do_testu = []

            for j in matrix:

                if int(j[i]) > 0 :
                    do_testu.append(int(j[i]))

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
        #print('Allright')
        #LINUX

        mighty_domains= self.OpenDirectory('/home/djangoadmin/final_site-project/important_files/LISTA_DOMEN')
        print("Opening domain list")
        GENOME_ID_SIZE_IN_BP = self.OpenFile('/home/djangoadmin/final_site-project/important_files/GENOME_ID_SIZE_IN_BP')
        print("Opening genome size in bp list")
        GENOME_ID_SIZE_IN_GENE = self.OpenFile('/home/djangoadmin/final_site-project/important_files/GENOME_ID_SIZE_IN_GENE')
        print("Opening genome size in gene list")
        
        """WINDOWS
        mighty_domains= self.OpenDirectory('LISTA_DOMEN')
        GENOME_ID_SIZE_IN_BP = self.OpenFile('GENOME_ID_SIZE_IN_BP')
        GENOME_ID_SIZE_IN_GENE = self.OpenFile('GENOME_ID_SIZE_IN_GENE')
        """

        GENOME_ID = [x[0] for x in GENOME_ID_SIZE_IN_BP]
        SIZE_IN_BP = [x[1] for x in GENOME_ID_SIZE_IN_BP]
        SIZE_IN_GENE = [x[1] for x in GENOME_ID_SIZE_IN_GENE]
        matrix = pd.DataFrame()
        matrix2=[]
        wyniki = []
        genome_dataframe = pd.DataFrame()
        neigh_dataframe =pd.DataFrame()
        genome_number_overall = 0
        genome_number_to_stat = 0
        pfam_whole_domain_counter = Counter({})
        pfam_same_strand_domain_counter = Counter({})
        pfam_oposite_strand_domain_counter = Counter({})
        message_for_output = "You have looked for conserved neighbourhood for "+self.user_PfamDomain+" domain, in range "+str(self.user_DistanceValue)+" bp, in "+self.user_OrganismValue+ " organisms."
        #print(message_for_output)
        message_for_additional_data = "Pfam domain , PVALUE,  occurence in neighbourhoods, average occurence in neighbourhood ,min occurence in neighbourhood , max occurence in neighbourhood ,occurence genomes, average occurence in genome, min occurence in genome,  max occurence in genome"



    ################################################################################


        if self.user_OrganismValue   == "escherichia":
            tax = "Escherichia"
            
        elif self.user_OrganismValue == "salmonella":
            tax ="Salmonella"
        elif self.user_OrganismValue ==  "pseudomonas":
            tax = "Pseudomonas"
        elif self.user_OrganismValue ==  "staphylococcus":
            tax = "Staphylococcus"
        elif self.user_OrganismValue ==  "streptococcus":
            tax = "Streptococcus"
        elif self.user_OrganismValue ==  "mycobacterium":
            tax = "Mycobacterium"
        elif self.user_OrganismValue ==  "acinetobacter":
            tax = "Acinetobacter"
        elif self.user_OrganismValue ==  "vibrio":
            tax = "Vibrio"
        elif self.user_OrganismValue ==  "bacillus":
            tax = "Bacillus"
        elif self.user_OrganismValue ==  "streptomyces":
            tax = "Streptomyces"
        elif self.user_OrganismValue == "porphyromonas":
            tax = "Porphyromonas"
        elif self.user_OrganismValue ==  "klebsiella":
            tax = "Klebsiella"
        elif self.user_OrganismValue ==  "enterococcus":
            tax = "Enterococcus"
        elif self.user_OrganismValue ==  "burkholderia":
            tax = "Burkholderia"        
        elif self.user_OrganismValue ==  "lactobacillus":
            tax = "Lactobacillus"
        elif self.user_OrganismValue ==  "campylobacter":
            tax = "Campylobacter"
        elif self.user_OrganismValue ==  "helicobacter":
            tax = "Helicobacter"
        elif self.user_OrganismValue ==  "shigella":
            tax = "Shigella"
        elif self.user_OrganismValue ==  "alldb":
            tax = "Alldb"
         


        ################################################################################
        #LINUX
        file_names = self.OpenDirectory('/home/djangoadmin/final_site-project/important_files/'+tax)

        
        """#WINDOWS
        file_names = self.OpenDirectory(tax)
        """
        for file in file_names:
            
            try:
                genes, start_coord,end_coord, orientation, domains, contig = self.Create6Lists(file)
                
            except FileNotFoundError:
                continue
            #LINUX
            file_name_raw = file.split('/')
            tax_name = file_name_raw[-1]
            
            """#WINDOWS
            file_name_raw = file.split('//')
            
            tax_name = file_name_raw[1]
            """

            genome_number_overall +=1
            number_of_genes_in_genome = self.GenomeSizeInGene(tax_name, GENOME_ID, SIZE_IN_GENE)
            genome_domains_counter = Counter(domains)
            coords = self.SearchingForDomainAndCoordinatesPlusAndMinus(self.user_PfamDomain, start_coord,end_coord, orientation, domains, contig)
            #self.PresenceConfirmation(coords,file,self.user_PfamDomain)
            D_GLOB = self.DLOK_DGLOBTime(genome_domains_counter,number_of_genes_in_genome,mighty_domains)

            if len(coords) > 0 :
                genome_number_to_stat +=1
                genome_dataframe = genome_dataframe.append(genome_domains_counter, ignore_index=True)

            for point in coords:
                last_coordinate, first_coordinate,pfam_beg,pfam_end,searched_pfam_orientation = self.GetRangeCoordinates(point,self.user_DistanceValue)
                pfam_index_to_neigh = self.ReturnIndexesDomainsWhole(start_coord,end_coord,last_coordinate,first_coordinate,pfam_beg, pfam_end,contig,point)
                pfam_index_to_neigh_same_strand, pfam_index_to_neigh_oposite_strand = self.ReturnIndexesDomainsStrandSameOposite(start_coord,end_coord,last_coordinate,first_coordinate,pfam_beg, pfam_end,contig,point,orientation)
                genes_in_neigh = self.ListOfGenesInNeigh(genes,pfam_index_to_neigh)
                number_of_genes_in_neigh = self.NeighbourhoodSizeInGenes(genes_in_neigh)

                whole = self.GiveMeListOfDomainsInNeigh(pfam_index_to_neigh,file,domains)
                neighbourhood_domains_counter = Counter(whole)
                neigh_dataframe = neigh_dataframe.append(neighbourhood_domains_counter,ignore_index=True)

                D_LOK = self.DLOK_DGLOBTime(neighbourhood_domains_counter,number_of_genes_in_neigh,mighty_domains)
                same_strand = self.GiveMeListOfDomainsInNeigh(pfam_index_to_neigh_same_strand,file,domains)
                oposite_strand = self.GiveMeListOfDomainsInNeigh(pfam_index_to_neigh_oposite_strand,file,domains)
                pfam_same_strand_domain_counter += Counter(same_strand)
                pfam_oposite_strand_domain_counter += Counter(oposite_strand)
                pfam_whole_domain_counter += Counter(whole)
                matrix2 = self.DataForWilcoxonTest(D_LOK,D_GLOB)
                print(matrix2)

#                #self.MiddleSave(matrix2)
#        #print("Loading data from server")
#        new_matrix = self.OpenFile("/home/klaster/neighborhood_analyzer/results/crossroad")
#        values_counter_whole_neigh, pfam_whole_neigh_domain_counter = self.SortExtractForPlot(pfam_whole_domain_counter)
#        values_counter_same_strand_neigh, pfam_same_strand_neigh_domain_counter = self.SortExtractForPlot(pfam_same_strand_domain_counter)
#        values_counter_oposite_strand_neigh, pfam_oposite_strand_neigh_domain_counter = self.SortExtractForPlot(pfam_oposite_strand_domain_counter)
        
        #plt.subplot(3,1,1)
        #self.Ploting(values_counter_whole_neigh,pfam_whole_neigh_domain_counter,10, self.user_ChartValue)
        #plt.subplot(3,1,2)
        #self.Ploting(values_counter_same_strand_neigh,pfam_same_strand_neigh_domain_counter,10, self.user_ChartValue)
        #plt.subplot(3,1,3)
        #self.Ploting(values_counter_oposite_strand_neigh,pfam_oposite_strand_neigh_domain_counter,10,self.user_ChartValue)
        #plt.show()

#        wyniki = self.WilcoxonCalculation(new_matrix)
#        filter_scores = self.ZippingScoresAndDiscardingNAN(mighty_domains, wyniki)

        ################################################################################
#        additional_data = self.CollectAddData(filter_scores,genome_dataframe, neigh_dataframe,genome_number_overall,genome_number_to_stat )
#        complete_data = self.CollectAllData(filter_scores, genome_dataframe, neigh_dataframe, genome_number_overall,genome_number_to_stat)
#        data_in_frames = self.CreateDataFrame(complete_data)
        
#        data_corrected = self.MultipleTestCorrection(data_in_frames, self.user_Correction)
#        after_cut = self.CutOffValue(data_corrected, self.user_CutOff)
        #print("File >>" + self.user_OutputValue + "<< saving")
#        message_down = "In my database there was " + str(genome_number_overall)+" "+ self.user_OrganismValue +  " genomes and in " + str(genome_number_to_stat) + " searched domain was found"

        #print("File " + self.user_OutputValue + " saving")
#        self.SaveOutput(self.user_OutputValue,filter_scores,message_for_output)
#        self.SaveOutputAddData(self.user_OutputValue,additional_data,message_for_additional_data,message_down)
#        self.SaveComplete(self.user_OutputValue, message_for_output,message_for_additional_data, message_down,after_cut )
        #print("File >>" + self.user_OutputValue + "<< saved")
        #return complete_data, message_down,message_for_output,message_for_additional_data

################################################################################
#
#""" Example of usage """
#
#a = NeighbourhoodAnalyzer('pfam02696', 5000, 'all', 10 ,'class_test' )
#a.GO()
################################################################################
