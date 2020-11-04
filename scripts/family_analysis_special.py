import pandas as pd
from scipy.stats import wilcoxon as test
import statistics
import ast
import pdb
class NeighFamilyAnalysis:

    def __init__(self,cutoff_value, save_name,organism_list):

        self.organism_list = organism_list
        self.cutoff_value = cutoff_value
        self.save_name = save_name


    def compress_all_data(self, lista_plikow):

        columns = ['Query', 'Domain', 'Pvalue', 'occurence in neighbourhoods', 'average occurence in neighbourhood',
                   'occurence genomes', 'average occurence in genome', 'avg DLOK-DGLOB', 'In what percentage?',
                   'Family', 'Summary','Dloc','Dglob']
        zbiorcze_dane = pd.DataFrame(columns=columns)
        row_counter = 0
        

        # print(' '.join(lista_plikow).split(','))

        for fil in lista_plikow:
            print(fil)
            # LOCAL
            # file_path = '/mnt/d/45.76.38.24/final_site-project/media/results/temp/' + file + ".txt"
            # VULTR
            file_path = '/home/djangoadmin/final_site-project/media/results/temp/' + fil 
            try:
                data = pd.read_csv(file_path, sep='\t',
                               error_bad_lines=False, skiprows=3, header=None,engine='python')
            except pd.errors.EmptyDataError:
                continue
            except FileNotFoundError:
                continue
            for line in data.iterrows():
                # print(counter)
                lista_wynikow = line[1].to_list()
                # dane_do_tabeli = []
                # print(lista_wynikow)
                try:
                    zbiorcze_dane.loc[row_counter] = [fil, lista_wynikow[0], lista_wynikow[1],
                                                  lista_wynikow[2], lista_wynikow[3],
                                                  lista_wynikow[4], lista_wynikow[5],
                                                  lista_wynikow[6], lista_wynikow[7],
                                                  lista_wynikow[8], lista_wynikow[9],
                                                  lista_wynikow[10],lista_wynikow[11]]
                except IndexError:
                    continue
                # zbiorcze_dane.loc[row_counter] = [0,1,2,3,4,5,6,7,8,9,10]
                row_counter += 1

        return zbiorcze_dane

    def create_dictionary(self,dataframe):

        domeny = list(set(dataframe['Domain']))
        dict_domain = {}
        for domain in domeny:
            dict_domain[domain] = {}
            for line in dataframe.iterrows():
                one_line = line[1].to_list()
                if one_line[1] == domain:
                    if 'occurence in neighbourhoods' in dict_domain[domain]:
                        dict_domain[domain]['occurence in neighbourhoods'].append(float(one_line[3]))
                    else:
                        dict_domain[domain]['occurence in neighbourhoods'] = [float(one_line[3])]

                    if 'average occurence in neighbourhood' in dict_domain[domain]:
                        dict_domain[domain]['average occurence in neighbourhood'].append(float(one_line[4]))
                    else:
                        dict_domain[domain]['average occurence in neighbourhood'] = [float(one_line[4])]

                    if 'occurence genomes' in dict_domain[domain]:
                        dict_domain[domain]['occurence genomes'].append(float(one_line[5]))
                    else:
                        dict_domain[domain]['occurence genomes'] = [float(one_line[5])]

                    if 'average occurence in genome' in dict_domain[domain]:
                        dict_domain[domain]['average occurence in genome'].append(float(one_line[6]))
                    else:
                        dict_domain[domain]['average occurence in genome'] = [float(one_line[6])]

                    if 'avg DLOK-DGLOB' in dict_domain[domain]:
                        dict_domain[domain]['avg DLOK-DGLOB'].append(float(one_line[7]))
                    else:
                        dict_domain[domain]['avg DLOK-DGLOB'] = [float(one_line[7])]

                    if 'In what percentage?' in dict_domain[domain]:
                        dict_domain[domain]['In what percentage?'].append(float(one_line[8][:-1]))
                    else:
                        dict_domain[domain]['In what percentage?'] = [float(one_line[8][:-1])]

                    if 'Family' not in dict_domain[domain]:
                        dict_domain[domain]['Family'] = (one_line[9])

                    if 'Summary' not in dict_domain[domain]:
                        dict_domain[domain]['Summary'] = (one_line[10])

                    if 'Families %' in dict_domain[domain]:
                        dict_domain[domain]['Families %'].append(1)
                    else:
                        dict_domain[domain]['Families %'] = [1]

                    if 'Dloc' in dict_domain[domain]:
                        dict_domain[domain]['Dloc'].append(one_line[11])
                    else:
                        dict_domain[domain]["Dloc"] = [float(one_line[11])]

                    if 'Dglob' in dict_domain[domain]:
                        dict_domain[domain]['Dglob'].append(one_line[12])
                    else:
                        dict_domain[domain]["Dglob"] = [float(one_line[12])]

        return dict_domain

    def calulate_data(self, dataframe, lista_plikow):

        new_columns = ['Pvalue', 'Family%', 'occurence in neighbourhoods', 'average occurence in neighbourhood',
                       'occurence genomes', 'average occurence in genome', 'avg_DLOK_DGLOB', 'In what percentage?',
                       'Family', 'Summary', 'Dloc', 'Dglob']
        domeny = list(dataframe.keys())
        caluclated_data = pd.DataFrame(columns=new_columns, index=domeny, )

        for dom in domeny:
            avg_DLDG = dataframe[dom]['avg DLOK-DGLOB']
            wynik = test(avg_DLDG, zero_method="wilcox")
            caluclated_data['Pvalue'][dom] = wynik.pvalue
            caluclated_data['avg_DLOK_DGLOB'][dom] = statistics.mean(avg_DLDG)
            caluclated_data['Family%'][dom] = sum(dataframe[dom]['Families %'])/len(' '.join(lista_plikow).split(','))

            caluclated_data['occurence in neighbourhoods'][dom] = sum(dataframe[dom]['occurence in neighbourhoods'])
            caluclated_data['average occurence in neighbourhood'][dom] = statistics.mean(
                dataframe[dom]['average occurence in neighbourhood'])
            caluclated_data['occurence genomes'][dom] = sum(dataframe[dom]['occurence genomes'])
            caluclated_data['average occurence in genome'][dom] = statistics.mean(dataframe[dom]['average occurence in genome'])
            caluclated_data['In what percentage?'][dom] = str(statistics.mean(dataframe[dom]['In what percentage?']))+"%"
            caluclated_data['Family'][dom] = dataframe[dom]['Family']
            caluclated_data['Summary'][dom] = dataframe[dom]['Summary']
            caluclated_data['Dloc'][dom] = statistics.mean(dataframe[dom]['Dloc'])
            caluclated_data['Dglob'][dom] = statistics.mean(dataframe[dom]['Dglob'])

        return caluclated_data

    def prepare(self, cutoff, dataframe):


        dataframe = dataframe[dataframe['avg_DLOK_DGLOB'] > 0]


        # dataframe['In what percentage?'] = dataframe['In what percentage?'].map('{:.3%}'.format)
        dataframe['Family%'] = dataframe['Family%'].map('{:.3%}'.format)
        dataframe['average occurence in neighbourhood'] = dataframe['average occurence in neighbourhood'].map(
            '{:.3}'.format)
        dataframe['avg_DLOK_DGLOB'] = dataframe['avg_DLOK_DGLOB'].map('{:.3}'.format)
        dataframe['average occurence in genome'] = dataframe['average occurence in genome'].map('{:.3}'.format)


        if cutoff == 'none':
            dataframe['Pvalue'] = dataframe['Pvalue'].map('{:.3e}'.format)
            return dataframe
        else:

            dataframe = dataframe[dataframe['Pvalue'] < float(cutoff)]
            dataframe['Pvalue'] = dataframe['Pvalue'].map('{:.3e}'.format)
            return dataframe

    def save_data(self,file_name, complete_data):
        """ Saves all stuff together as one file """
        columns_names = ['Domain','Pvalue', 'Group%', 'occurence in neighbourhoods', 'average occurence in neighbourhood',
                       'occurence genomes', 'average occurence in genome', 'Density difference', 'In what percentage?',
                       'Family', 'Summary']
        # # LOCAL
        # with open('/mnt/d/45.76.38.24/final_site-project/' + file_name, 'w') as output_file:
        # VULTR
        with open('/home/djangoadmin/final_site-project/'+file_name, 'w') as output_file:
            # output_file.write(complete_data)
            for names in columns_names:
                output_file.write(names)
                output_file.write("\t")
            output_file.write('\n')
            for row in complete_data.iterrows():
                # print(row)
                output_file.write
                index, data = row
                pre = data.tolist()
                output_file.write(index)
                output_file.write("\t")
                output_file.write("\t".join([str(i) for i in pre]))
                output_file.write("\n")

    def start(self):
        
        compressed_data = self.compress_all_data(lista_plikow=self.organism_list)
        create_dictionary = self.create_dictionary(dataframe=compressed_data)
        calculated = self.calulate_data(dataframe=create_dictionary, lista_plikow=self.organism_list)
        ready_dataframe = self.prepare(cutoff=self.cutoff_value, dataframe=calculated)
        self.save_data(file_name=self.save_name, complete_data=ready_dataframe)



# ########################################################################################################################
# # Wrzut wszystkiego do jednego wora
#
# columns = ['Query', 'Domain', 'Pvalue','occurence in neighbourhoods', 'average occurence in neighbourhood' ,
#            'occurence genomes', 'average occurence in genome', 'avg_DLOK_DGLOB', 'In what percentage?', 'Family', 'Summary']
# zbiorcze_dane = pd.DataFrame(columns=columns)
# lista_plikow = ['atlantibacter','biostraticola','buttiauxella','cedecea','citrobactert','cronobacter','escherichia',
#                 'enterobacillus', 'enterobacter','franconibacter','gibbsiella', 'izhakiella', 'klebsiella','kluyvera',
#                 'kosakonia', 'leclercia','lelliottia', 'limnobaculum', 'mangrovibacter', 'metakosakonia', 'pluralibacter',
#                 'pseudescherichia', 'pseudocitrobacter', 'raoultella', 'rosenbergiella', 'salmonella', 'shigella',
#                 'shimwellia', 'siccibacter', 'superficieibacter', 'trabulsiella', 'yokenella','enterobacteriaceae']
#
#
# row_counter = 0
# for file in lista_plikow:
#     data = pd.read_csv('D:\\45.76.38.24\\final_site-project\\test_files\\PF02696-' + file + '.txt',sep='\t',error_bad_lines=False, skiprows= 3, header=None)
#     for line in data.iterrows():
#
#         # print(counter)
#         lista_wynikow = line[1].to_list()
#         # dane_do_tabeli = []
#         # print(lista_wynikow)
#         zbiorcze_dane.loc[row_counter] = [file, lista_wynikow[0], lista_wynikow[1], lista_wynikow[2],lista_wynikow[3],
#                                           lista_wynikow[4],lista_wynikow[5],lista_wynikow[6],lista_wynikow[7],
#                                           lista_wynikow[8],lista_wynikow[9],]
#         # print(lista_wynikow[6])
#         # zbiorcze_dane.loc[row_counter] = [0,1,2,3,4,5,6,7,8,9,10]
#         row_counter += 1
#
# ########################################################################################################################
# # zbierz liste domen i zrob słownik do którego będziemy zbierać dane
#
# domeny = list(set(zbiorcze_dane['Domain']))
# dict_domain = {}
# for domain in domeny:
#     dict_domain[domain] = {}
#     for line in zbiorcze_dane.iterrows():
#         one_line = line[1].to_list()
#         if one_line[1] == domain:
#
#             if 'occurence in neighbourhoods' in dict_domain[domain]:
#                 dict_domain[domain]['occurence in neighbourhoods'].append(float(one_line[3]))
#             else:
#                 dict_domain[domain]['occurence in neighbourhoods'] = [float(one_line[3])]
#
#             if 'average occurence in neighbourhood' in dict_domain[domain]:
#                 dict_domain[domain]['average occurence in neighbourhood'].append(float(one_line[4]))
#             else:
#                 dict_domain[domain]['average occurence in neighbourhood'] = [float(one_line[4])]
#
#             if 'occurence genomes' in dict_domain[domain]:
#                 dict_domain[domain]['occurence genomes'].append(float(one_line[5]))
#             else:
#                 dict_domain[domain]['occurence genomes'] = [float(one_line[5])]
#
#             if 'average occurence in genome' in dict_domain[domain]:
#                 dict_domain[domain]['average occurence in genome'].append(float(one_line[6]))
#             else:
#                 dict_domain[domain]['average occurence in genome'] = [float(one_line[6])]
#
#             if 'avg_DLOK_DGLOB' in dict_domain[domain]:
#                 dict_domain[domain]['avg_DLOK_DGLOB'].append(float(one_line[7]))
#             else:
#                 dict_domain[domain]['avg_DLOK_DGLOB'] = [float(one_line[7])]
#
#             if 'In what percentage?' in dict_domain[domain]:
#                 dict_domain[domain]['In what percentage?'].append(float(one_line[8]))
#             else:
#                 dict_domain[domain]['In what percentage?'] = [float(one_line[8])]
#
#             if 'Family' not in dict_domain[domain]:
#                 dict_domain[domain]['Family'] = (one_line[9])
#
#             if 'Summary' not in dict_domain[domain]:
#                 dict_domain[domain]['Summary'] = (one_line[10])
#
#             if 'Families %' in dict_domain[domain]:
#                 dict_domain[domain]['Families %'].append(1)
#             else:
#                 dict_domain[domain]['Families %'] = [1]
#
#
# #######################################################################################################################
# # tworzymy zbiorcza tabele i liczymy wszystko
#
# new_columns = ['Pvalue','Family%','occurence in neighbourhoods', 'average occurence in neighbourhood' ,
#            'occurence genomes', 'average occurence in genome', 'avg_DLOK_DGLOB', 'In what percentage?', 'Family', 'Summary']
#
# caluclated_data = pd.DataFrame(columns=new_columns, index=domeny,)
#
#
# for dom in domeny:
#
#     avg_DLDG = dict_domain[dom]['avg_DLOK_DGLOB']
#     wynik = test(avg_DLDG, zero_method="wilcox")
#     caluclated_data['Pvalue'][dom] = wynik.pvalue
#     caluclated_data['avg_DLOK_DGLOB'][dom] = statistics.mean(avg_DLDG)
#     caluclated_data['Family%'][dom] = sum(dict_domain[dom]['Families %']) / len(lista_plikow)
#     caluclated_data['occurence in neighbourhoods'][dom] = sum(dict_domain[dom]['occurence in neighbourhoods'])
#     caluclated_data['average occurence in neighbourhood'][dom] = statistics.mean(dict_domain[dom]['occurence in neighbourhoods'])
#     caluclated_data['occurence genomes'][dom] = sum(dict_domain[dom]['occurence genomes'])
#     caluclated_data['average occurence in genome'][dom] = statistics.mean(dict_domain[dom]['occurence genomes'])
#     caluclated_data['In what percentage?'][dom] = statistics.mean(dict_domain[dom]['In what percentage?'])
#     caluclated_data['Family'][dom] = dict_domain[dom]['Family']
#     caluclated_data['Summary'][dom] = dict_domain[dom]['Summary']
#
# print(caluclated_data)
#
# #######################################################################################################################
# # wywal negatywy, sortuj, zapis, powrzucać wszystko w funkcje i klasyprint(caluclated_data[caluclated_data["avg_DLOK_DGLOB"] > 0])
#
# caluclated_data[caluclated_data["Pvalue"] < 0.05]
