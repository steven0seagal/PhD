from profana import SuperSpeedAnalysisFromDomainAll
import sys
import os
a = SuperSpeedAnalysisFromDomainAll(sys.argv[1], int(sys.argv[2]), sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7],sys.argv[8],sys.argv[9] )
a.go()
# VULTR
os.system("rm /home/djangoadmin/final_site-project/scripts/temp_data/*")
# LOCAL
os.system("rm /mnt/d/45.76.38.24/final_site-project/scripts/temp_data/*")
