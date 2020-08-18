#!/usr/local/bin/python

from application import Application
import time
from datetime import date
import psycopg2
from prettytable import PrettyTable

class Table:
    def __init__(self, database, tablename):
        self.database = database
        self.tablename = tablename
        self.conn = psycopg2.connect(host="localhost", database=database)
        self.c = self.conn.cursor()

    def insert_app(self, app):
        with self.conn:
            self.c.execute("SELECT * FROM {} WHERE company='{}'".format(self.tablename, app.company))
            if (self.c.fetchone() is None):
                if app.apply_date is None:
                    app.apply_date = date.today()
                if app.progress is None:
                    app.progress = 'Applied'

                mystr = "Inserting new company: {}, with new fields: {}".format(app.company, ', '.join(str(x)+'='+ "'"+str(vars(app)[x])+"'" for x in vars(app).keys() if vars(app)[x] is not None))
                if len(mystr) > 175:
                    index = 175
                    while mystr[index] != " ":
                        index -= 1
                    mystr = mystr[:index] + '\n\t' + mystr[index+1:]
                print('\n\t' + mystr)

                self.c.execute("""
                                INSERT INTO {} ({})
                                VALUES ({})
                                """.format(self.tablename,
                                           ', '.join(str(x) for x in vars(app).keys() if vars(app)[x] is not None),
                                           ', '.join("'" + str(x) + "'" for x in vars(app).values() if x is not None),
                                           )
                                )
            else:
                mystr = "Updating company: {}, with new fields: {}".format(app.company, ', '.join(str(x)+'='+ "'"+str(vars(app)[x])+"'" for x in vars(app).keys() if vars(app)[x] is not None))
                if len(mystr) > 175:
                    index = 175
                    while mystr[index] != " ":
                        index -= 1
                    mystr = mystr[:index] + '\n\t' + mystr[index+1:]
                print('\n\t' + mystr)

                self.c.execute("""
                                UPDATE {} 
                                SET {}
                                WHERE company='{}'""".format(self.tablename,
                                                 ', '.join(str(x)+'='+ "'"+str(vars(app)[x])+"'" for x in vars(app).keys() if vars(app)[x] is not None),
                                                 app.company
                                                )
                                )

    def remove_app(self, company):
        print("\n\tDeleting {} from '{}' table".format(company.title(), self.tablename))
        with self.conn:
            self.c.execute('''
            DELETE FROM {} WHERE company='{}';
            '''.format(self.tablename, company))

    def print_table(self, app):
        with self.conn:
            self.c.execute("SELECT * from apps_2020_2021 ORDER BY apply_date ASC")
            rows = self.c.fetchall()
            table = PrettyTable([x.title().replace("_", " ") for x in vars(app).keys()])
            for row in rows:
                row = list(row)
                for i in range(len(row)):
                    if row[i] is None:
                        row[i] = ""
                    if len(row[i]) > 30:
                        index = len(row[i])//2
                        if "https:" not in row[i]:
                            while row[i][index] != " ":
                                index += 1
                        elif "https:" in row[i]:
                            while row[i][index] != "/":
                                index += 1
                        row[i] = row[i][:index] + '\n' + row[i][index:]
                table.add_row(list(row))
            table.align['Company'] = 'l'
            table.align['Progress'] = 'l'
            print(table)

def main():
    company = input("Company: ") or "EMPTY"
    progress = input("Progress: ") or None
    listing_link = input("URL Link: ") or None
    apply_date = input("Apply Date: ") or None
    response_date = input("Response Date: ") or None
    interview_status = input("Interview Status: ") or None
    contacts = input("Contacts: ") or None
    notes = input("Notes: ") or None

    start = time.time()

    mytable = Table(database="applications_2020_2021",
                    tablename="apps_2020_2021")
    app = Application(company=company,
                     progress=progress,
                     interview_status=interview_status,
                     apply_date=apply_date,
                     response_date=response_date,
                     listing_link=listing_link,
                     contacts=contacts,
                     notes=notes)

    mytable.insert_app(app)
    # mytable.remove_app('EMPTY')
    # mytable.remove_app('Zillow')
    # mytable.remove_app('NASA')
    mytable.print_table(app)

    end = time.time()
    print("\nFinished in {} seconds".format(end-start))

if __name__ == "__main__":
    main()