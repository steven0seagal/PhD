""" This script is created only for testing my algorithm and how it manages caluclations"""

from analiza_otoczenia_class_v2_2_linux import NeighbourhoodAnalyzer
import sys


a = NeighbourhoodAnalyzer(sys.argv[1], int(sys.argv[2]), sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7] )
a.GO()