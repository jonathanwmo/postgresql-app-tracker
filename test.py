import psycopg2
from prettytable import from_db_cursor

conn = psycopg2.connect(host='localhost', database='applications_2020_2021')
with conn:
    c = conn.cursor()
    c.execute('SELECT * FROM apps_2020_2021')
    table = from_db_cursor(c)
    table.align['company'] = 'l'
    # table.title = 'hi' # TODO: Change title to self.tablename

print(table)