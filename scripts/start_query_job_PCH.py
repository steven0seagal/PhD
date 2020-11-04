import psycopg2
import os


connection = psycopg2.connect(user = "djangoadmin", password = "psqlsteve99",host = "localhost",port = "5432",
                              database = "final_sitedb")
cursor = connection.cursor()
cursor.execute("SELECT * FROM public.accounts_queforpch ORDER BY id ASC;")
records = cursor.fetchall()
# Description
# record[0] = pk
# record[1] = user_id
# record[2] = tool
# record[3] = status
# record[4] = analysis_name
# record[5] = script
# record[6] = file

sql_update_query = """UPDATE public.accounts_queforpch SET status = %s WHERE id = %s"""

for record in records:
    if record[3] == 'Done':
        continue
    elif record[3] == 'Running':
        break
    elif record[3] == 'Queue':
        # Change status to RUNNING
        cursor.execute(sql_update_query, ('Running', record[0]))
        connection.commit()
        run = os.system(record[5])
        if run == 0:
            cursor.execute(sql_update_query, ('Done', record[0]))
            connection.commit()
            # INPUT TO OTHER DATABASE !!!

        elif run != 0:
            cursor.execute(sql_update_query, ('Error', record[0]))
            connection.commit()
        break
        # Change status to DONE
    elif record[3] == 'Error':
        continue

cursor.close()
connection.close()
