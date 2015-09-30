#Anders Simpson-Wolf
#09/30/2015
#Write a script that executes a SQL query on the EDS database

import psycopg2
import sys, os
from cryptography.fernet import Fernet
os.chdir("/Users/anders/Documents/Learning/Python/Python_Tests")

def sql_call():
    print("Connecting to Database and Running Query")
    host = "emaildata.cqlai0yteoyb.us-east-1.redshift.amazonaws.com"
    port = 5439
    database = "eds"
    user = "anders"

    f = open('eds_key.txt', r)
    key = f.read()
    f.close()
    f = open('eds_password.txt', r)
    cipher_text = f.read()
    f.close()
    cipher_suite = Fernet(key)
    password = cipher_suite.decrypt(cipher_text)

    conn = psychopg2.connect(database=database, user=user, host=host, port=port, password=password, sslmode='allow')
    cur = con.cursor(name = "conquer")

    query = "SELECT * FROM email WHERE from_domain = 'googlemail.com' AND message_time >= CURRENT_DATE -10 LIMIT 3"

    print(query)
    cur.execute(query)

    resultsTable = cur.fetchmany(10)
    for row in resultsTable:
        print(row)

    conn.close()

def main():
    print("In main, about to run a query.")
    sql_call()

