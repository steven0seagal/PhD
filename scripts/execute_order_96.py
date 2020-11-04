from family_analysis import NeighFamilyAnalysis
import sys, os

data = NeighFamilyAnalysis(str(sys.argv[1]),sys.argv[2],sys.argv[4:])
print(sys.argv)
data.start()
# VULTR
os.system("rm /home/djangoadmin/final_site-project/media/results/temp/*")
# LOCAL
# os.system("rm /mnt/d/45.76.38.24/final_site-project/media/results/temp/*")