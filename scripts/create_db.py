import psycopg2 as pg2
def OpenMultipleList(file_name):
    list_ofs = [] 
    with open(file_name , 'r' ) as f:
        for line in f:
            list_ofs.append(line.strip().split())
    return list_ofs

def OpenSingleList(file_name):
    list_of = [] 
    with open(file_name , 'r' ) as f:
        list_of =[line.strip() for line in f]
    return list_of

lista_danych = OpenSingleList('lista.txt')

for plik in lista_danych:
    print(plik)
    data = OpenMultipleList(plik)
    if data != [] : 
        for line in data:
            conn = pg2.connect(database = 'final_sitedb', user = 'postgres',password ='Seagalinho_0X')
            cur = conn.cursor()
            cur.execute('INSERT INTO searchdb_coocurence_coocurence (gene_1,gene_2,together,first_only,second_only,neither,pvalue) VALUES(%s, %s,%s,%s,%s,%s,%s)',(line[0], line[1],line[2],line[3],line[4],line[5],line[6]))
            conn.commit()
            cur.close()
    #cur.fetchone()
