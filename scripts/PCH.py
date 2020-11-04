
import scipy.stats as stats
from statsmodels.stats.multitest import multipletests
import math
import pdb

def fisher_test(both, first, second, none):
    oddsratio, pvalue = stats.fisher_exact([[both, first], [second, none]])
    return pvalue

def multiple_test_correction(data):
    scores = multipletests(data, method="bonferroni", is_sorted=False, returnsorted=False)
    return scores

def calculate_sim_dif(data_list_first, data_list_second):
    data_list_first = set(data_list_first)
    data_list_second = set(data_list_second)

    both = len(data_list_first.intersection(data_list_second))
    first = len(data_list_first - data_list_second)
    second = len(data_list_second - data_list_first)
    none = 103293 - both - first - second
    return both, first, second, none

def scalar_value(both,first,second):
    top = both
    bottom_first = both + first
    bottom_second = both + second
    bottom_pre = bottom_first*bottom_second
    bottom = math.sqrt(bottom_pre)
    result = top / bottom
    return result

def calculate_PXX_part(up):
    value = up / 103293
    return value

def calculate_P11ST(both,first):
    top = both + first
    value = top / 103293
    return value

def calculate_P12ND(both,second):
    top = both + second
    value = top / 103293
    return value

def calculate_C00(both,first,second,none):

    # P00
    if none != 0: 
        first_part = calculate_PXX_part(none)

        # P00 / P01st * P02nd
        ## P00
        second_part_top = first_part
        ## P01st
        second_part_bottom_1 = 1 - calculate_P11ST(both,first)
        ## P02nd
        second_part_bottom_2 = 1 - calculate_P12ND(both,second)
        ##  P01st * P02nd
        second_part_bottom = second_part_bottom_1 * second_part_bottom_2
        ## P00 / P01st * P02nd
        second_part = second_part_top / second_part_bottom

        # log(P00 / P01st * P02nd)
        third = math.log2(second_part)

        value = first_part * third
    else:
        value = 0 
    return value

def calculate_C01(both,first,second,none):

    if second != 0 :
        # P01
        first_part = calculate_PXX_part(second)

        # P01 / P01st * P12nd
        ## P01
        second_part_top = first_part
        ## P01st
        second_part_bottom_1 = 1 - calculate_P11ST(both,first)
        ## P12nd
        second_part_bottom_2 = calculate_P12ND(both,second)
        ##  P01st * P12nd
        second_part_bottom = second_part_bottom_1 * second_part_bottom_2
        ## P01 / P01st * P12nd
        second_part = second_part_top / second_part_bottom

        # log(P01 / P01st * P12nd)
        third = math.log2(second_part)

        value = first_part * third
    else:
        value = 0
    return value

def calculate_C10(both,first,second,none):

    if first != 0: 
        # P10
        first_part = calculate_PXX_part(first)

        # P10 / P11st * P02nd
        ## P10
        second_part_top = first_part
        ## P11st
        second_part_bottom_1 = calculate_P11ST(both,first)
        ## P02nd
        second_part_bottom_2 = 1 - calculate_P12ND(both,second)
        ##  P11st * P02nd
        second_part_bottom = second_part_bottom_1 * second_part_bottom_2
        ## P10 / P11st * P02nd
        second_part = second_part_top / second_part_bottom

        # log(P00 / P01st * P02nd)
        third = math.log2(second_part)

        value = first_part * third
    else:
        value = 0 
    return value

def calculate_C11(both,first,second,none):

    if both != 0: 
        # P11
        first_part = calculate_PXX_part(both)

        # P11 / P11st * P12nd
        ## P11
        second_part_top = first_part
        ## P11st
        second_part_bottom_1 = calculate_P11ST(both,first)
        ## P12nd
        second_part_bottom_2 = calculate_P12ND(both,second)
        ##  P11st * P12nd
        second_part_bottom = second_part_bottom_1 * second_part_bottom_2
        ## P11 / P11st * P12nd
        second_part = second_part_top / second_part_bottom

        # log(P11 / P11st * P12nd)
        third = math.log2(second_part)

        value = first_part * third
    else:
        value = 0
    return value

def mutual_information(C00,C01,C10,C11):

    value = C00 + C01 + C10 + C11
    return value

def save_all(save_file,genes,pvalues,corr_pvalues,scalars, mutuals):

    with open("/home/djangoadmin/final_site-project/"+save_file, "+a") as handler:
        for gene,pvalue,corr_pvalue, scalar, mutual in zip(genes,pvalues,corr_pvalues,scalars, mutuals ):
            handler.write(gene)
            handler.write("\t")
            handler.write(str(pvalue))
            handler.write("\t")
            handler.write(str(corr_pvalue))
            handler.write("\t")
            handler.write(str(scalar))
            handler.write("\t")
            handler.write(str(mutual))
            handler.write("\t")

def save_all(save_file,zbiorcze,correction):
    

    with open("/home/djangoadmin/final_site-project/" + save_file, "+a") as handler:
        for line, corr in zip(zbiorcze, correction[1]):
            for i in line:
                handler.write(str(i))
                handler.write("\t")
            handler.write(str(corr))
            handler.write("\n")

def save_small(save_file, zbiorcze):

    with open("/home/djangoadmin/final_site-project" + save_file, "+a") as handler:
        for line in zbiorcze:
            for i in line:
                handler.write(str(i))
                handler.write("\t")
            handler.write("\n")


def open_file_important(filename):
    with open("/home/djangoadmin/final_site-project/important_files/"+filename,"r") as handler:
        data = [x.strip() for x in handler]
    return data

def get_list_of_fragments(protein):

    with open("/home/djangoadmin/final_site-project/important_files/wszystkie_bialka",'r') as handler:
        data = [x.strip() for x in handler]
    result = [x for x in data if protein in x]

    return result

def save_header(save_file, header):

    with open("/home/djangoadmin/final_site-project" + save_file, "+a") as handler:
        handler.write(header)



class HS_calculation:

    def __init__(self, protein, fisher,scalar,mutual,link):

        self.protein = protein
        self.fisher = fisher
        self.scalar = scalar
        self.mutual = mutual
        self.link = link

    def calculate_HS(self):

        self.header = "Gene1"+"\t"+"Gene2"+"\t"+ "Both" + "\t" + "First" + "\t" + "Second" + "\t" +"None" + "\t"
        if self.scalar == 'True':
            self.header += "Scalars"+ "\t"
        if self.mutual == 'True':
            self.header += "Mutual Information" + "\t"
        if self.fisher == 'True':
            self.header += "Fisher pvalue" + "\t" + "Fisher pvalue(corrected) "
        self.header += "\n"
        save_header(self.link, self.header)

            

        proteins = get_list_of_fragments(self.protein)
        seq_id = open_file_important('wszystkie_bialka')
        for protein in proteins:
            print(protein)
            zbiorcze = []
            genes = []
            pvalues = []
            scalars = []
            mutual_inf = []
            gene_data_first = open_file_important('hs_cooc/' + protein)

            for id_second in seq_id:
                
                single_result = []
                single_result.append(protein)
                single_result.append(id_second)

                genes.append((protein,id_second))
                gene_data_second = open_file_important('hs_cooc/'+id_second)

                both, first, second, none = calculate_sim_dif(gene_data_first, gene_data_second)
                single_result.extend([both, first,second,none])


                if self.scalar == 'True':
                    scalar = scalar_value(both, first, second)
                    scalars.append(scalar)
                    single_result.append(scalar)
                if self.mutual == 'True':
                    
                    C00 = calculate_C00(both, first, second, none)
                    C01 = calculate_C01(both, first, second, none)
                    C10 = calculate_C10(both, first, second, none)
                    C11 = calculate_C11(both, first, second, none)
                    mutual = mutual_information(C00, C01, C10, C11)
                    mutual_inf.append(mutual)
                    single_result.append(mutual)
                if self.fisher == 'True':

                    pvalue = fisher_test(both, first, second, none)
                    pvalues.append(pvalue)
                    single_result.append(pvalue)
                zbiorcze.append(single_result)

            if self.fisher == 'True':
                pvalues_after_correction = multiple_test_correction(pvalues)
            if self.fisher == 'True':
                save_all(self.link, zbiorcze,pvalues_after_correction)
            else:
                save_small(self.link, zbiorcze )



