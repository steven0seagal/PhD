import subprocess
import sys
import time

class FFAS:

    def __init__(self,database,input_file, output_file):

        self.database = database
        self.input_file = input_file
        self.output_file = output_file

    def calculate(self):

        # nazwa pliku wejsciowego
        server_path_input = '/home/djangoadmin/final_site-project'
        full_input_file_name = server_path_input + self.input_file

        # nazwa profilu wyjściowego
        output_file_name = server_path_input + self.output_file

        if self.database == "profile":

            # nazwa alignmentu wyjsciowego
            full_name_split = full_input_file_name.rsplit('.')
            file_name = full_name_split[0]
            alignments_name = file_name + ".fa"

            # Tworzenie profilu
            print('Running... ', 'blast.pl < %s | tee %s | profil > %s' % (full_input_file_name, alignments_name, output_file_name))
            subprocess.run(('blast.pl < %s | tee %s | profil > %s' % (full_input_file_name, alignments_name, output_file_name)), shell=True)
            # subprocess.run(('blast.pl < %s | tee %s | profil > %s' % (arg , alignments_name, profile_name)),shell=True)

        elif self.database == "PDB":

            # Przeszukiwanie PDB
            print('pdb')
            subprocess.run(('ffas -b %s /home/djangoadmin/ffas/db/PDB1018.db/fb > %s' % (full_input_file_name, output_file_name)), shell=True)

        elif self.database == "SCOP":

            # Przeszukiwanie SCOP
            print('scop')
            subprocess.run(('ffas -b %s /home/djangoadmin/ffas/db/SCOP207.db/fb > %s' % (full_input_file_name, output_file_name)), shell=True)

        elif self.database == "PFAM":

            # Przeszukiwanie PFAM
            print('pfam')
            subprocess.run(('ffas -b %s /home/djangoadmin/ffas/db/PfamA32U.db/fb > %s' % (full_input_file_name, output_file_name)), shell=True)

        elif self.database == "Hsapiens":

            # Przeszukiwanie H.Sapiens
            print('hsapiens')
            subprocess.run(('ffas -b %s /home/djangoadmin/ffas/db/H.sapiens.db/fb > %s' % (full_input_file_name, output_file_name)), shell=True)

        elif self.database == "COG":

            # Przeszukiwanie COG
            print('cog')
            subprocess.run(('ffas -b %s /home/djangoadmin/ffas/db/COG1018.db/fb > %s' % (full_input_file_name, output_file_name)), shell=True)

        elif self.database == "VFdbcustom":

            # Przeszukiwanie VFdbcustom
            print('VFdbcustom')
            subprocess.run(('ffas -b %s /home/djangoadmin/ffas/db/VFDBcustom.db/fb > %s' % (full_input_file_name, output_file_name)), shell=True)

        elif self.database == "VFDB":

            # Przeszukiwanie VFDB 
            print('VFDB')
            subprocess.run(('ffas -b %s /home/djangoadmin/ffas/db/VFDB.db/fb > %s' % (full_input_file_name, output_file_name)), shell=True)




