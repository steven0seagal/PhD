"""
Created on Mon May 13 15:06:52 2019
Updated on June 10 2019
@author: Bartosz Baranowski
"""

"Import what is essential"
import requests as r
from Bio import SeqIO
from io import StringIO
import collections
from itertools import groupby

class HMMER():

    def __init__(self, main_seqs, skip_seqs):
        self.main_seqs = main_seqs
        self.skip_seqs = skip_seqs

    def result_name_maker(self):

        name_split = self.main_seqs.split('.')
        new_name = name_split[0] + '_fixed.fa'
        return new_name

    def OpenLine(self,file_name):
        file = []
        with open(file_name , 'r') as f:
            file = [line.strip() for line in f]
        return file


    def sort_and_take_care_of_dumps(self, sequences,skip_seqs):

        sorted_names = []
        #sort sequences
        sorted_fasta = [f for f in sorted(sequences, key=lambda x : x.id)]
        #take sequence names and count duplicates
        for s in sorted_fasta:
            name_split = s.name.split('/')
            name = name_split[0]
            sorted_names.append(name)
            name_dups = [item for item, count in collections.Counter(sorted_names).items() if count > 1]
        #SKIP WHAT IS TO SKIP
        if skip_seqs == None:
            return name_dups
        else:
            for name_to_skip in name_dups:
                if name_to_skip in skip_seqs:
                    name_dups.remove(name_to_skip)
            return name_dups

        #for name_to_skip in name_dups:
        #    if name_to_skip in skip_seqs:
        #        name_dups.remove(name_to_skip)
        #return name_dups

    def checking_duplicates(self,sequences, name_dups):

        #duplicates for check
        sequences_fasta_dup = []
        #sequence container to which we will add
        sequences_fasta = []
        #GET SEQUENCE NAMES
        for s in sequences:
            name_split = s.name.split('/')
            name = name_split[0]
            #SEPARATE DUPLICATES
            if name not in name_dups:
                sequence = str('>' + s.description + '\n' + s.seq + '\n')
                sequences_fasta.append(sequence)
            else:
                sequences_fasta_dup.append(s)


        #OUR ALL DUPLICATES IDS
        ids = []
        for s in sequences_fasta_dup:
            ids.append(s.name)

        return ids,sequences_fasta

    def grouping_duplicates(self,ids):

        groups = [ list(value) for key, value in groupby(ids, key=lambda element: element.split('/')[0])]
        return groups

    def someting_plus_downloading(self,groups,sequences_fasta):
        new_sequences = []
        for group in groups:

            min_ = []
            max_ = []
            for element in group:
                element_parts = element.split('/')
                element_number = element_parts[1].split('-')
                min_.append(int(element_number[0]))
                max_.append(int(element_number[1]))
            from_ = min(min_)
            to_ = max(max_)
            id_parts = element_parts[0].split('_')
            id_ = id_parts[0]

    ############################################################################
    ###############SEQUENCE DOWNLOAD############################################
    ############################################################################
            try:
                base_url = 'http://www.uniprot.org/uniprot/'
                current_url = base_url + id_ + '.fasta'
                response = r.post(current_url)
                cData = ''.join(response.text)

                Seq = StringIO(cData)
                pSeq = list(SeqIO.parse(Seq,'fasta'))
                new_sequence = str('>' + pSeq[0].name + '/' + str(from_) + '-' + str(to_) + '\n' + pSeq[0].seq[from_-1:to_] + '\n')
                new_sequences.append(new_sequence)
            except:
                print('sequence obsolete!: ', element_parts[0])
    #            obsolete = str('>' + id_ + '/' + str(from_) + '-' + str(to_) + '\n')
    #            new_sequences.append(obsolete)
                continue
        result_fasta = sequences_fasta + new_sequences
        return result_fasta

    def Saver(self,file_name, container):
        name_for_save = file_name.replace('(', '_').replace(')', '_')
        with open(name_for_save,'w') as w:
            for s in container:
                w.write(s)



    def Go(self):
        #skip_seks = self.OpenLine(self.skip_seqs)
        if self.skip_seqs == None:
            skip_seks = None
        else:
            skip_seks = self.OpenLine(self.skip_seqs)
        with open(self.main_seqs,'r') as rs:
            sequences = list(SeqIO.parse(rs, 'fasta'))
        name_output = self.result_name_maker()


        name_dups = self.sort_and_take_care_of_dumps(sequences,skip_seks)
        ids,sequences_fasta = self.checking_duplicates(sequences,name_dups)
        groups = self.grouping_duplicates(ids)
        result_fasta = self.someting_plus_downloading(groups,sequences_fasta)
        self.Saver(name_output, result_fasta)
        
#EXAMPLE
"""
first = HMMER('bf.fa','bf_seqs_to_skip')
first.Go()
first.result_name_maker()
"""