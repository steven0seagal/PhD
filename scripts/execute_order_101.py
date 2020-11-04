from FFAS import FFAS
import sys
import os

a = FFAS(sys.argv[1], sys.argv[2], sys.argv[3])
a.calculate()

# check where tee file is saving