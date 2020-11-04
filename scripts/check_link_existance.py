import os
def link_ready(query_object, link_field= 'link'):
    output = []

    for query in query_object.values():

        if os.path.exists(os.getcwd()+query[link_field]) == False:
            query[link_field] = None
        output.append(query)
    return output


def new_file_checker(query_object, link_field= 'link'):
    output = []
    for query in query_object:
        if os.path.exists(os.getcwd()+ query[link_field]) == False:
            query[link_field] = None
        output.append(query)
    return output