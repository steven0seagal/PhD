
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio.Alphabet import IUPAC
import datetime


class ColapsingSeq():

    def __init__(self,multifasta_sequences):

        self.multifasta_sequences = multifasta_sequences

    def IndexesFromMaster(self, sequences):

        parser = 0
        master_sequence = sequences[0]

        id_master = master_sequence.id
        sequence_master = str(master_sequence.seq)
        lista_index_dash = []
        lista_index_letter = []
        for letter in sequence_master:
            if letter != "-":
                lista_index_letter.append(parser)
                parser += 1
            elif letter == "-":
                lista_index_dash.append(parser)
                parser += 1
        return lista_index_dash, lista_index_letter

    def CreateConsensusSeqDash(self, lista_index_dash, sequence):

        new_seq = ''
        id_slave = sequence.id
        seq_slave = sequence.seq
        seq_slave = str(seq_slave)
        parser = 0
        for letter in seq_slave:
            if parser not in lista_index_dash:
                new_seq +=letter
                parser +=1
            else:
                parser +=1

        return new_seq, id_slave


    def CreateConsensusSeqLetter(self, lista_index_letter,sequence):

        new_seq = ''
        parser = 0
        id_slave = sequence.id
        seq_slave = sequence.seq
        seq_slave = str(seq_slave)
        for indexy in lista_index_letter:
            new_seq += seq_slave[indexy]
            parser +=1
        return new_seq, id_slave

    def SaveOutput(self,all_together):
        links_divided = list(self.multifasta_sequences.split('/'))
        name_for_save = links_divided[-1].replace('(','_').replace(')', '_')

        with open('/home/djangoadmin/final_site-project/media/'+ name_for_save +'_colapsed.txt' , 'w') as output_file:
            for line in all_together:
                output_file.write("".join([str(i) for i in line]))
    
    def CreateLink(self):
        links_divided = list(self.multifasta_sequences.split('/'))
        out_file = links_divided[-1] +'_colapsed.txt'
        return out_file

    def Go(self):
        all_together = []
        sequences = list(SeqIO.parse(self.multifasta_sequences, "fasta"))
        lista_index_dash, lista_index_letter = self.IndexesFromMaster(sequences)
        for sequence in sequences:
            if len(lista_index_dash) == len(lista_index_letter):
                sequence, id_seq = self.CreateConsensusSeqLetter(lista_index_letter,sequence)
            elif len(lista_index_letter) > len(lista_index_dash):
                sequence, id_seq = self.CreateConsensusSeqDash(lista_index_dash,sequence)
            elif len(lista_index_letter) < len(lista_index_dash):
                sequence, id_seq = self.CreateConsensusSeqLetter(lista_index_letter,sequence)
            all_together.append(">"+id_seq)
            all_together.append("\n")
            all_together.append(sequence)
            all_together.append("\n")
        #pdb.set_trace()
        self.SaveOutput(all_together)
        return all_together
