# -*- coding: utf-8 -*-
"""
Created on Mon Apr  8 13:17:48 2019

@author: bartek
"""

from crontab import CronTab
from datetime import datetime
from datetime import timedelta

class CreateCronTaskNeighborhood():
    
    def __init__(self, user_PfamDomain, user_DistanceValue, user_OrganismValue,user_CutOff, user_Correction,user_StrandValue, user_OutputValue):
        
        self.user_PfamDomain = user_PfamDomain
        self.user_DistanceValue = user_DistanceValue
        self.user_OrganismValue = user_OrganismValue
        self.user_CutOff = user_CutOff
        self.user_Correction = user_Correction
        self.user_StrandValue = user_StrandValue
        self.user_OutputValue = user_OutputValue
        
        
    def OpenLog(self):
        list_of_tasks = [] 
        with open('/home/djangoadmin/final_site-project/log/log.txt', 'r') as f:
            list_of_tasks = [line.strip() for line in f]
        return list_of_tasks 

    def SaveComplete(self,complete_data):
        with open('/home/djangoadmin/final_site-project/log/log.txt' , 'w') as output_file:
            for line in complete_data:
                output_file.write(line)
                output_file.write("\n")

    def Task(self):
        log_file  = self.OpenLog()
        last_entry = datetime.strptime(log_file[-1], '%Y-%m-%d %H:%M:%S.%f')
       
        current_time = datetime.now()
        if last_entry + timedelta(minutes=8) > current_time:
            to_log = last_entry + timedelta(minutes=8)
            log_file.append(str(to_log))
	    
            out_time = to_log + timedelta(minutes=8)
            end_end = str(out_time).replace(' ','_')

            cron = CronTab(user=True)
            job = cron.new(command='/home/djangoadmin/final_site_venv/bin/python3 /home/djangoadmin/final_site-project/scripts/execute_order_66.py '+ self.user_PfamDomain +' '+ str(self.user_DistanceValue)+' '+self.user_OrganismValue + ' '+ self.user_CutOff+' '+self.user_Correction+' '+self.user_StrandValue+' ' + end_end)
            job.setall(str(to_log.minute) +' '+ str(to_log.hour) +' '+ str(to_log.day) +' '+str(to_log.month) +' *')    
            cron.write()
            # +8 do cronA 
        
        elif last_entry + timedelta(minutes=8) < current_time or last_entry + timedelta(minutes=8) == current_time:
            to_log  = current_time + timedelta(minutes = 1)
            log_file.append(str(to_log))
            out_time = to_log + timedelta(minutes=8)
            end_end = str(out_time).replace(' ','_')
            cron = CronTab(user = True)
            job = cron.new(command='/home/djangoadmin/final_site_venv/bin/python3 /home/djangoadmin/final_site-project/scripts/execute_order_66.py '+ self.user_PfamDomain +' '+ str(self.user_DistanceValue)+' '+self.user_OrganismValue + ' ' + self.user_CutOff + ' ' + self.user_Correction + ' ' + self.user_StrandValue +' ' + end_end)

#            job = cron.new(command='python3 /home/djangoadmin/final_site-project/scripts/execute_order_66.py '+ self.user_PfamDomain +' '+ str(self.user_DistanceValue)+' '+self.user_OrganismValue+' ' + end_end)
            job.setall(str(to_log.minute) +' '+ str(to_log.hour) +' '+ str(to_log.day) +' '+str(to_log.month) +' *')    
            cron.write(user=True)
            #current + 1 do crona
        self.SaveComplete(log_file)
        return str(out_time)
#bartek = CreateCronTaskNeighborhood('pfam02696', 3000, 'escherichia', 'test_#1')
#a = bartek.Task()
#print(a)

class CreateCronTaskStreching():

    def __init__(self, pairwise_align, large_align_one, large_align_two,out_name):

        self.pairwise_align = pairwise_align
        self.large_align_one = large_align_one
        self.large_align_two = large_align_two
        self.out_name = out_name

    def OpenLog(self):
        list_of_tasks = [] 
        with open('/home/djangoadmin/final_site-project/log/log.txt', 'r') as f:
            list_of_tasks = [line.strip() for line in f]
        return list_of_tasks


    def SaveComplete(self,complete_data):
        with open('/home/djangoadmin/final_site-project/log/log.txt' , 'w') as output_file:
            for line in complete_data:
                output_file.write(line)
                output_file.write("\n")

    def Task(self):
        log_file  = self.OpenLog()
        last_entry = datetime.strptime(log_file[-1], '%Y-%m-%d %H:%M:%S.%f')
       
        current_time = datetime.now()
        if last_entry + timedelta(minutes=8) > current_time:
            to_log = last_entry + timedelta(minutes=8)
            log_file.append(str(to_log))
	    
            out_time = to_log + timedelta(minutes=8)
            end_end = str(out_time).replace(' ','_')
            ###################################################################################################
            cron = CronTab(user=True)
            job = cron.new(command='/home/djangoadmin/final_site_venv/bin/python3 /home/djangoadmin/final_site-project/scripts/execute_order_69.py '+ self.pairwise_align + ' ' + self.large_align_one +' '+ self.large_align_two + ' ' + end_end)
            job.setall(str(to_log.minute) +' '+ str(to_log.hour) +' '+ str(to_log.day) +' '+str(to_log.month) +' *')    
            cron.write()
            # +8 do cronA 
            ###################################################################################################
        elif last_entry + timedelta(minutes=8) < current_time or last_entry + timedelta(minutes=8) == current_time:
            to_log  = current_time + timedelta(minutes = 1)
            log_file.append(str(to_log))
            out_time = to_log + timedelta(minutes=8)
            end_end = str(out_time).replace(' ','_')
            
            #####################################################################################################
            cron = CronTab(user = True)
            job = cron.new(command='/home/djangoadmin/final_site_venv/bin/python3 /home/djangoadmin/final_site-project/scripts/execute_order_69.py '+ self.pairwise_align + ' ' + self.large_align_one +' '+ self.large_align_two + ' ' + end_end)

            job.setall(str(to_log.minute) +' '+ str(to_log.hour) +' '+ str(to_log.day) +' '+str(to_log.month) +' *')    
            cron.write(user=True)
            ##########################################################################################################
            #current + 1 do crona
        self.SaveComplete(log_file)
        return str(out_time)
#create_task = CreateCronTaskStreching('alignment_pkaslave_lani1194master_YVrvkYX.txt','lani1194_kin_fixed_al_GcyGXm1.fa','pka_2000_al.txt', 'dupa')
#pre = create_task.Task()