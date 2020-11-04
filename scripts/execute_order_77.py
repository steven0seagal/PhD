# from analiza_otoczenia_class_V2_5_1_vultr import NeighbourhoodAnalyzer
# from _gene_neigh_anlyzer import SuperSpeedAnalysisFromDomain
from PCH import HS_calculation
import sys
import os
a = HS_calculation(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
a.calculate_HS()
# VULTR
