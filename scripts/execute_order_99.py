# from _gene_neigh_anlyzer import NeighborhoodAnalyzerFromGene
from profana import NeighborhoodAnalyzerFromGene
import sys
import os
a = NeighborhoodAnalyzerFromGene(sys.argv[1], int(sys.argv[2]), sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7])
a.go()
# VULTR
os.system("rm /home/djangoadmin/final_site-project/scripts/temp_data/*")