"""
Created on Tue Aug 13 17:26:21 2019

@author: B@rtek
"""
import json
def retype_domain(user_input):

    domain_for_database = user_input.lower()
    domain_to_search = user_input[:2].lower() + 'am' + user_input[2:]


    return domain_for_database, domain_to_search

def check_if_domain_can_be_reachable(organism, domain):

    if organism != 'all_db':
        response = "OK"
        return True
    elif organism == 'all_db':

        with open("/home/djangoadmin/final_site-project/important_files/excluded_domains") as inputfile:
            excluded = [line.strip() for line in inputfile]
        with open("/home/djangoadmin/final_site-project/important_files/reachable_domains") as inputfile:
            reachable = [line.strip() for line in inputfile]
        if domain not in reachable:
            return False
        else:
            return True


    #
    # with open('/home/djangoadmin/final_site-project/important_files/correct_domain.json') as json_file:
    #     data = json.load(json_file)
    # if domain in data[organism]:
    #     return True
    # else:
    #     return False