# from analiza_otoczenia_class_V2_5_1_vultr import NeighbourhoodAnalyzer
# from _gene_neigh_anlyzer import SuperSpeedAnalysisFromDomain
from profana import SuperSpeedAnalysisFromDomain
import sys
import os
a = SuperSpeedAnalysisFromDomain(sys.argv[1], int(sys.argv[2]), sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7], sys.argv[8] )
a.go()
# VULTR
os.system("rm /home/djangoadmin/final_site-project/scripts/temp_data/*")
