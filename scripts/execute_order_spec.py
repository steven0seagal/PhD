# from profana_special_task import SuperSpeedAnalysisFromDomainAll
# import sys
# import os
# import json
# import pdb
# # ALL DATABASE -- family
# # open file with genomes
# with open("/home/djangoadmin/final_site-project/important_files/family_level.json", "r") as handler:
#     taxonomy = json.load(handler)

# print("Succesfully loaded file with genomes")

# for group in taxonomy:
#     output = '/media/results/temp/'+ group
#     query = SuperSpeedAnalysisFromDomainAll('pfam02696', '5000', group, 'none', 'bonferroni','both',output, 'family', 'no')
#     query.go()
#     os.system("rm /home/djangoadmin/final_site-project/scripts/temp_data/*")

 
# from family_analysis_special import NeighFamilyAnalysis
# import sys, os
# tax_list = list(taxonomy.keys())
# data = NeighFamilyAnalysis('none','/media/results/family_resultst_pfam02696',tax_list)
# data.start()
# os.system("rm /home/djangoadmin/final_site-project/media/results/temp/*")

# ##################################################################################################################################

# # ALL DATABASE -- phylum
# # open file with genomes
# with open("/home/djangoadmin/final_site-project/important_files/phylum_level.json", "r") as handler:
#     taxonomy = json.load(handler)

# print("Succesfully loaded file with genomes")

# for group in taxonomy:
#     output = '/media/results/temp/'+ group
#     query = SuperSpeedAnalysisFromDomainAll('pfam02696', '5000', group, 'none', 'bonferroni','both',output, 'phylum', 'no')
#     query.go()
#     os.system("rm /home/djangoadmin/final_site-project/scripts/temp_data/*")

 
# from family_analysis_special import NeighFamilyAnalysis
# import sys, os
# tax_list = list(taxonomy.keys())
# data = NeighFamilyAnalysis('none','/media/results/phylum_resultst_pfam02696',tax_list)
# data.start()
# os.system("rm /home/djangoadmin/final_site-project/media/results/temp/*")

# #################################################################################################

# # ALL DATABASE -- genus
# # open file with genomes
# with open("/home/djangoadmin/final_site-project/important_files/genus_level.json", "r") as handler:
#     taxonomy = json.load(handler)

# print("Succesfully loaded file with genomes")

# for group in taxonomy:
#     output = '/media/results/temp/'+ group
#     query = SuperSpeedAnalysisFromDomainAll('pfam02696', '5000', group, 'none', 'bonferroni','both',output, 'genus', 'no')
#     query.go()
#     os.system("rm /home/djangoadmin/final_site-project/scripts/temp_data/*")

 
# from family_analysis_special import NeighFamilyAnalysis
# import sys, os
# tax_list = list(taxonomy.keys())
# data = NeighFamilyAnalysis('none','/media/results/genus_resultst_pfam02696',tax_list)
# data.start()
# os.system("rm /home/djangoadmin/final_site-project/media/results/temp/*")

########################################################################################################

from profana_special_task import SuperSpeedAnalysisFromDomain

# import sys
# import os

# query = SuperSpeedAnalysisFromDomain('pfam02696', '5000', 'Escherichia', 'none', 'bonferroni','both','/media/results/Escherichia02696.txt', 'yes')
# query.go()
# os.system("rm /home/djangoadmin/final_site-project/scripts/temp_data/*")

# query = SuperSpeedAnalysisFromDomain('pfam02696', '5000', 'Salmonella', 'none', 'bonferroni','both','/media/results/Salmonella02696.txt', 'yes')
# query.go()
# os.system("rm /home/djangoadmin/final_site-project/scripts/temp_data/*")

# query = SuperSpeedAnalysisFromDomain('pfam02696', '5000', 'Klebsiella', 'none', 'bonferroni','both','/media/results/Klebsiella02696.txt', 'yes')
# query.go()
# os.system("rm /home/djangoadmin/final_site-project/scripts/temp_data/*")

# query = SuperSpeedAnalysisFromDomain('pfam02696', '5000', 'Shigella', 'none', 'bonferroni','both','/media/results/Shigella02696.txt', 'yes')
# query.go()
# os.system("rm /home/djangoadmin/final_site-project/scripts/temp_data/*")

# query = SuperSpeedAnalysisFromDomain('pfam11119', '5000', 'Escherichia', 'none', 'bonferroni','both','/media/results/Escherichia11119.txt', 'yes')
# query.go()
# os.system("rm /home/djangoadmin/final_site-project/scripts/temp_data/*")

# query = SuperSpeedAnalysisFromDomain('pfam13493', '5000', 'Escherichia', 'none', 'bonferroni','both','/media/results/Escherichia13493.txt', 'yes')
# query.go()
# os.system("rm /home/djangoadmin/final_site-project/scripts/temp_data/*")

# query = SuperSpeedAnalysisFromDomain('pfam07208', '5000', 'Escherichia', 'none', 'bonferroni','both','/media/results/Escherichia07208.txt', 'yes')
# query.go()
# os.system("rm /home/djangoadmin/final_site-project/scripts/temp_data/*")


# query = SuperSpeedAnalysisFromDomain('pfam02696', '5000', 'all genomes', 'none', 'bonferroni','both','/media/results/all_db_02696.txt', 'yes')
# query.go()
# os.system("rm /home/djangoadmin/final_site-project/scripts/temp_data/*")

taxonomy_list = ['Enterobacter', 'Escherichia', 'Salmonella', 'Klebsiella', 'Shigella', 'Cronobacter','Atlantibacter', 'Citrobacter', 'Buttiauxella', 'Enterobacillus', 
'Superficieibacter', 'Kosakonia', 'Raoultella', 'Lelliottia', 'Leclercia', 'Franconibacter', 'Trabulsiella', 'Candidatus_Moranella', 'Candidatus_Westeberhardia', 
'Candidatus_Regiella', 'Candidatus_Riesia', 'Kluyvera', 'Gibbsiella', 'Candidatus_Hamiltonella', 'Pluralibacter', 'Cedecea', 'Shimwellia', 'Izhakiella', 'Pseudescherichia', 
'Candidatus_Tachikawaea', 'Limnobaculum', 'Pseudocitrobacter', 'Mangrovibacter', 'Yokenella', 'Candidatus_Blochmannia', 'Rosenbergiella', 'Candidatus_Gullanella', 'Siccibacter', 
'Candidatus_Mikella', 'Candidatus_Hoaglandella', 'Metakosakonia', 'Biostraticola', 'Candidatus_Doolittlea'] 

# for tax in taxonomy_list:

#     output = '/media/results/temp/'+ tax
#     query = SuperSpeedAnalysisFromDomain('pfam02696', '5000', tax,'none', 'bonferroni','both', output, 'no')
#     query.go()
#     os.system("rm /home/djangoadmin/final_site-project/scripts/temp_data/*")

from family_analysis_special import NeighFamilyAnalysis
import sys, os

data = NeighFamilyAnalysis('none','/media/results/enterobacteriaceae_family_resultst_pfam02696',taxonomy_list)
data.start()