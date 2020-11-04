from Bio import AlignIO


class ThreeAlignmentColapser():

    """
    Initialize
    """
    def __init__(self, reference_multifasta, first_multifasta, second_multifasta, out_name):

        self.reference_multifasta = reference_multifasta
        self.first_multifasta = first_multifasta
        self.second_multifasta = second_multifasta
        self.out_name = out_name
        

    """
    Tells which file contains first [0] reference and wchich contains
    second [1] reference.
    'one_one' --> in first file there is first reference - LINEAR
    'one_two' --> in first file there is second reference - CROSSED
    """
    def SearchForReferenceSeq(self,ref_seqs,first_seqs):

        ref_seq = str(ref_seqs[0].seq).replace('-','')
        first_seq = str(first_seqs[0].seq).replace('-','')
    
        if ref_seq in first_seq:
            selector = 'one_one'
        else:
            selector = 'one_two'
        return selector
##OLD 
#        id_list = [x.id for x in first_seqs]
#        if ref_seqs[0].id in id_list:
#            selector = 'one_one'
#        else:
#            selector = 'one_two'
#        return selector


################################################################################
# MAYBE IN FUTURE I WILL USE THIS TO TARGET MASTER POSITION IN SLAVE LIST      #
#                                                                              #
#    def MasterSlaveAlignIndex(self, first_seqs,second_seqs,ref_seqs,selector):#
#                                                                              #
#        first_id_list = [x.id for x in first_seqs]                            #
#        second_id_list = [x.id for x in second_seqs]                          #
#                                                                              #
#        if selector == 'one_one':                                             #
#            index_first_master = first_id_list.index(ref_seqs[0].id)          #
#            index_second_master = second_id_list.index(ref_seqs[1].id)        #
#        elif selector =='two_two'                                             #
#            index_first_master = first_id_list.index(ref_seqs[1].id)          #
#            index_second_master = second_id_list.index(ref_seqs[0].id)        #
#                                                                              #
#        return index_first_master, index_second_master                        #
################################################################################

    """
    It takes reference sequences and strech them to fit in slave alignment and
    paralell saves positions of master nucl/prot in new seq and positions of
    slave nucl/prot in new seq. And returns new changed seq.
    """
    def CreateSlaveRemakeList(self, ref_seqs, slave_alignment,place_in_reference, place_in_slave):

        master_in_slave = str(slave_alignment[place_in_slave].seq)
        reference_seq = str(ref_seqs[place_in_reference].seq)
        range_for_it = 3 * len(str(master_in_slave))
        lista_slave = []
        lista_mastera = []
     #   listaa= []
        new_seq = ''
        counter_master = 0
        counter_slave = 0
        counter_overall = 0
        for i in range(range_for_it): #3x dlugosc max seq

            try:
                if reference_seq[counter_master] == master_in_slave[counter_slave]:
                    new_seq += reference_seq[counter_master]
    #                listaa.append(i)
                    counter_slave +=1
                    counter_master+=1
                    lista_mastera.append(counter_master)
                    lista_slave.append(counter_overall)

                elif reference_seq[counter_master] != master_in_slave[counter_slave] and reference_seq[counter_master] =='-' :
                    new_seq += reference_seq[counter_master]
    #                listaa.append(i)
                    counter_master+=1
                    lista_mastera.append(counter_master)

                elif reference_seq[counter_master] != master_in_slave[counter_slave] and master_in_slave[counter_slave] =='-' :
                    new_seq += master_in_slave[counter_slave]
                    counter_slave +=1
                    lista_slave.append(counter_overall)
                    lista_mastera.append('x')
            except IndexError:
                try:
                    new_seq += master_in_slave[counter_slave]
                    counter_slave +=1
                    lista_slave.append(counter_overall)
                    lista_mastera.append('x')
                except IndexError:
                    try:
                        new_seq += reference_seq[counter_master]
                        counter_master +=1
                        lista_mastera.append(counter_master)
    #                    listaa.append(i)
                    except IndexError:
                        continue

            counter_overall +=1
        return lista_mastera, lista_slave,new_seq

    """
    It takes slave alignment and change each sequence to fit to given template.
    And returns completely different sequences with ids.
    """
    def RemakeSlave(self, list_of_changes,list_of_seqs_to_change,new_seq):

        list_of_ids = []
        list_of_seqs = []
        for seq in list_of_seqs_to_change:
            list_of_ids.append(seq.id)
            seq = str(seq.seq)
            new_seq_output = ''
            for nucl in range(len(new_seq)):

                if nucl in list_of_changes:
                    new_seq_output += seq[list_of_changes.index(nucl)]
                else:
                    new_seq_output +='-'
            list_of_seqs.append(new_seq_output)
        return list_of_ids, list_of_seqs

    """
    It takes 2 list from CreateSlaveRemakeList with positions of master
    nucl/prot in new seq and strech them even more to match positions in main
    raw alignment (reference). And returns lists that will be template for final
    streching.
    """
    def DifferenceBetweenChangedMasters(self, master1, master2):

        counter1 = 0
        counter2 = 0
        lista1= []
        lista2 = []

        for i in range(100000):
            try:

                if master1[counter1] == master2[counter2]:
                    lista1.append(master1[counter1])
                    lista2.append(master2[counter2])
                    counter1 += 1
                    counter2 += 1

                elif master1[counter1] != master2[counter2] and master1[counter1] == 'x':
                    lista2.append('-')
                    lista1.append('x')
                    counter1 += 1
                elif master1[counter1] != master2[counter2] and master2[counter2] == 'x':
                    lista1.append('-')
                    lista2.append('x')
                    counter2 += 1
                elif counter1 > len(master1) and master2[counter2] =='x':
                    lista1.append('-')
                    lista2.append('x')
                    counter2 += 1
                elif counter2 > len(master2) and master1[counter1] == 'x':
                    lista2.append('-')
                    lista1.append('x')
                    counter1 += 1
            except IndexError:
    #        elif counter1 == len(master1) and counter2 == len(master2):
                continue
        return lista1, lista2

    """
    Final streching of sequences that both slave alignments will be fitted to
    each other and to master (reference) sequences. And returns complete
    alignment in two sets, slave1 and slave2.
    """
    def FinalChange(self, list_of_seq, list_of_changes, list_of_ids):

        counter_id = 0
        new_set = []
        for seq in list_of_seq:
            new_seq = ''
            counter = 0
            for replace in list_of_changes:
                if replace != '-':
                    new_seq += seq[counter]
                    counter += 1
                elif replace == '-':
                    new_seq += '-'
            id_complete = ">" + str(list_of_ids[counter_id])
            new_set.append(id_complete)
            new_set.append(new_seq)
            counter_id += 1
        return new_set

    """
    It takes two sets and return 1 complete alignment with two master sets on
    first places.
    """
    def MergeTwoSets(self, set1, set2):

        all_mighty = []
        all_mighty.append(set1[0])
        all_mighty.append(set1[1])
        all_mighty.append(set2[0])
        all_mighty.append(set2[1])
        for i in set1[2:]:
            all_mighty.append(i)
        for i in set2[2:]:
            all_mighty.append(i)

        return all_mighty

    """
    My classic single object save function ;)
    """
    def SaveOutput(self, container,file_name):
        #file_name = list(self.reference_multifasta.split('.'))
        name_for_save = file_name.replace('(', '_').replace(')', '_')
        with open('/home/djangoadmin/final_site-project' + name_for_save , 'w') as output:
            for line in container:
                output.write("".join([str(i) for i in line]))
                output.write("\n")

    def CreateDownloadableLink(self):
        file_name = list(self.reference_multifasta.split('.'))
        link = file_name[0] + "_streched.txt"
        return link

    def Go(self):
        file_directory = '/home/djangoadmin/final_site-project'
        ref_seqs = list(AlignIO.read(file_directory + self.reference_multifasta, "fasta"))
        first_seqs =  list(AlignIO.read(file_directory + self.first_multifasta, "fasta"))
        second_seqs =  list(AlignIO.read(file_directory + self.second_multifasta, "fasta"))
        selector = self.SearchForReferenceSeq(ref_seqs,first_seqs)
        if selector == "one_one":
            #index_first_master, index_second_master = self.MasterSlaveAlignIndex(first_seqs,second_seqs,ref_seqs,selector)
            lista_master_1 , lista_slave_1, new_seq_1 = self.CreateSlaveRemakeList(ref_seqs, first_seqs, 0, 0 )
            lista_master_2 , lista_slave_2, new_seq_2 = self.CreateSlaveRemakeList(ref_seqs,second_seqs , 1,0 )

            list_of_ids_1, list_of_seqs_1 = self.RemakeSlave(lista_slave_1 ,first_seqs, new_seq_1)
            list_of_ids_2, list_of_seqs_2 = self.RemakeSlave(lista_slave_2 ,second_seqs, new_seq_2)

            final_list1, final_list2 = self.DifferenceBetweenChangedMasters(lista_master_1, lista_master_2)

            new_set_1 = self.FinalChange(list_of_seqs_1, final_list1, list_of_ids_1)
            new_set_2 = self.FinalChange(list_of_seqs_2, final_list2, list_of_ids_2)

            all_mighty_set = self.MergeTwoSets(new_set_1, new_set_2)

            self.SaveOutput(all_mighty_set, self.out_name)



        elif selector == 'one_two':
            #index_first_master, index_second_master = self.MasterSlaveAlignIndex(first_seqs,second_seqs,ref_seqs,selector)
            lista_master_1 , lista_slave_1, new_seq_1 = self.CreateSlaveRemakeList(ref_seqs, first_seqs, 1, 0 )
            lista_master_2 , lista_slave_2, new_seq_2 = self.CreateSlaveRemakeList(ref_seqs, second_seqs, 0,0 )

            list_of_ids_1, list_of_seqs_1 = self.RemakeSlave(lista_slave_1 ,first_seqs, new_seq_1)
            list_of_ids_2, list_of_seqs_2 = self.RemakeSlave(lista_slave_2 ,second_seqs, new_seq_2)

            final_list1, final_list2 = self.DifferenceBetweenChangedMasters(lista_master_1, lista_master_2)

            new_set_1 = self.FinalChange(list_of_seqs_1, final_list1, list_of_ids_1)
            new_set_2 = self.FinalChange(list_of_seqs_2, final_list2, list_of_ids_2)

            all_mighty_set = self.MergeTwoSets(new_set_1, new_set_2)

            self.SaveOutput(all_mighty_set, self.out_name)
