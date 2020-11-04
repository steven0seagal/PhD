# -*- coding: utf-8 -*-
"""
Created on Sun Jun 30 20:46:21 2019

@author: bartek
"""
class PfamValidator():
    
    def __init__(self, input_value):
        self.input_value = input_value
        
    def Validate(self):
        
        if len(self.input_value) != 7 :
            return False
        else:
            just_pfam = self.input_value[:2]
            if just_pfam.lower() != "pf":
                return False
            else:
                string_numba = self.input_value[2:]
                return(string_numba.isnumeric())


            

