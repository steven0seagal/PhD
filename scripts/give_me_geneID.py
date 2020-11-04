def OpenDirectory(path_to_file):
    """ Opens file that contain 1 column and strip it by space. """

    with open(path_to_file , 'r') as f:
        file_names = [line.strip() for line in f]
    return file_names
def OpenMatrix(path_to_file):
    """ Opens file that contain 1 column and strip it by space. """

    with open(path_to_file , 'r') as f:
        file_names = [line.strip().split() for line in f]
    return file_names
def OpenDatabaseFile(file_name):
    """ Opens file that contains data about single genome """

    plik=[]
    with open(file_name+".txt") as inputfile:
        for line in inputfile:
            plik.append(line.strip().split())
    return plik
def Create6Lists(file):
    """ Open single genome file chew it and return 6 lists -> GENE, START_COORD, END_COORDS ,ORIENTATION, DOMAINS """

    data = OpenDatabaseFile(file)
    start_coord = []
    end_coord = []
    orientation = []
    domains = []
    genes = []
    contig = []
    for bit in data :
        genes.append(int(bit[0]))
        start_coord.append(int(bit[1]))
        end_coord.append(int(bit[2]))
        orientation.append(bit[3])
        domains.append(bit[4])
        contig.append(bit[5])
    return genes, start_coord,end_coord, orientation, domains, contig

def Return_Domain_Counter(lista):
    list = []
    counter = 0
    for domain in lista:
        if domain =="pfam02661":
            list.append(counter)
        counter +=1
    return list
tax ="all_genomes.txt"
database =OpenDirectory('/mnt/d/45.76.38.24/final_site-project/important_files/'+tax)
genome_id = OpenDirectory(path_to_file="pf07756.img.jgi")
matrix = OpenMatrix(path_to_file="pf07756.pfams.img.jgi")

interesting_genomes = []
licznik = 0
for neigh in matrix:
    if 'pfam02661' in neigh:
        interesting_genomes.append(genome_id[licznik])
    licznik += 1

for file in database:
    genome_pre = file.split("/")
    genome = genome_pre[-1]
    if genome in interesting_genomes:
        genes, start_coord, end_coord, orientation, domains, contig = Create6Lists(file)
        lista_domen = Return_Domain_Counter(domains)
        for i in lista_domen:
            print(genes[i])

