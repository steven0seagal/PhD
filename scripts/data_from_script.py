
def feedMe(object,sel_tool):
    output = []

    for part in object:


        loads_info  = part.script
        data = loads_info.split()

        if part.tool == sel_tool and sel_tool == 'NA':
            domain = data[2][:2].upper() + data[2][4:]

            tax = data[4].capitalize() + ' (genus)'

            strand  = data[7].capitalize()

            if data[6]  == 'bonferroni':
                correction = 'Bonferroni'
            elif data[6] == 'fdr_bh':
                correction = 'Benjamini-Hochberg Procedure'
            else:
                correction = 'None'
            one_job = {'id':part.id ,'domain':domain, 'range':data[3], 'cutoff':data[5], 'tax': tax,
                       'strand':strand, 'correction': correction, 'link': data[8],'status': part.status,'out_name': part.analysis_name}
            output.append(one_job)
        elif part.tool == sel_tool and sel_tool == 'NAG':
            domain = "Gene list"
            tax = 'Whole database'
            strand  = data[7].capitalize()

            if data[6]  == 'bonferroni':
                correction = 'Bonferroni'
            elif data[6] == 'fdr_bh':
                correction = 'Benjamini-Hochberg Procedure'
            else:
                correction = 'None'
            one_job = {'id':part.id ,'domain':domain, 'range':data[3], 'cutoff':data[5], 'tax': tax,
                       'strand':strand, 'correction': correction, 'link': data[8],'status': part.status,'out_name': part.analysis_name}
            output.append(one_job)

        elif part.tool == sel_tool and sel_tool == 'M3A':
            one_job = {'id':part.id, 'master_master':data[2], 'master_slave_1':data[3], 'master_slave_2':data[4],'status':part.status, 'link': data[5],'anal_name':part.analysis_name}
            output.append(one_job)

        elif part.tool == sel_tool and sel_tool == 'NAF':
            domain = data[2][:2].upper() + data[2][4:]
            tax = data[-2] + ' (family)'
            strand = data[7].capitalize()
            if data[6]  == 'bonferroni':
                correction = 'Bonferroni'
            elif data[6] == 'fdr_bh':
                correction = 'Benjamini-Hochberg Procedure'
            else:
                correction = 'None'
            one_job = {'id': part.id, 'domain': domain, 'range': data[3], 'cutoff': data[5], 'tax': tax,
                       'strand': strand, 'correction': correction, 'link': part.file, 'status': part.status,
                       'out_name': part.analysis_name}
            output.append(one_job)

        elif part.tool == sel_tool and sel_tool == "NAD":
            domain = data[2][:2].upper() + data[2][4:]

            if len(data) == 10:
                tax = "All database"
                # print(data)
            else:
                # print(data)
                tax = "All database - {} ".format(data[9].capitalize())
            strand = data[7].capitalize()
            if data[6] == 'bonferroni':
                correction = 'Bonferroni'
            elif data[6] == 'fdr_bh':
                correction = 'Benjamini-Hochberg Procedure'
            else:
                correction = 'None'
            one_job = {'id': part.id, 'domain': domain, 'range': data[3], 'cutoff': data[5], 'tax': tax,
                       'strand': strand, 'correction': correction, 'link': part.file, 'status': part.status,
                       'out_name': part.analysis_name}
            output.append(one_job)

        elif part.tool == sel_tool and sel_tool == "FFAS":
            data = loads_info.split("&&")
            PDB_file = "-"
            SCOP_file = "-"
            PFAM_file = "-"
            Hsapiens_file = "-"
            COG_file = "-"
            VFDB_file = "-"
            VFDB_custom_file= "-"
            if len(data) == 1:

                small_data = data[0].split(" ")
                data = data[0].split(" ")
                one_job = {'id': part.id, 'out_name': part.analysis_name,'insert_file':small_data[3], 'profile_id':small_data[4],
                           'PDB':PDB_file, 'SCOP':SCOP_file, 'PFAM':PFAM_file, 'Hsapiens':Hsapiens_file, 'COG':COG_file,'VFDB':VFDB_file, 'VFDB_custom':VFDB_custom_file,'status':part.status}

                output.append(one_job)
            else:
                init_data = data[0].split(" ")
                for calculation in data:

                    small_data = (calculation.split())
                    if 'SCOP' in calculation:
                        SCOP_file = small_data[4]
                    if 'PFAM' in  calculation:
                        PFAM_file = small_data[4]
                    if 'PDB' in calculation:
                        PDB_file = small_data[4]
                    if 'Hsapiens' in calculation:
                        Hsapiens_file = small_data[4]
                    if 'COG' in calculation:
                        COG_file = small_data[4]
                    if 'VFDB' in calculation:
                        VFDB_file = small_data[4]
                    if 'VFdbcustom' in calculation:
                        VFDB_custom_file = small_data[4]
          
                one_job = {'id': part.id, 'out_name': part.analysis_name,'insert_file':init_data[3],'profile_id':init_data[4],
                           'PDB':PDB_file, 'SCOP':SCOP_file, 'PFAM':PFAM_file, 'Hsapiens':Hsapiens_file, 'COG':COG_file,'VFDB':VFDB_file, 'VFDB_custom':VFDB_custom_file,
                           'status':part.status}
                output.append(one_job)
        elif part.tool == sel_tool and sel_tool =="PCH":
            fisher, scalar,mutual = ["NO",'NO','NO']
            if data[3] == "True":
                fisher = "YES"
            if data[4] == "True":
                scalar = "YES"
            if data[5] == "True":
                mutual = "YES"
            one_job = {'id': part.id, 'out_name': part.analysis_name,'protein_id': data[2],'status': part.status,
                       'link':data[6],'fisher':fisher ,'scalar':scalar, 'mutual':mutual}
            output.append(one_job)




    return output
