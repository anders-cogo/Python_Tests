#Anders Simpson-Wolf
#09/16/2015
#Create a script in Python that executes a Query written in PostgreSQL on one of the Cogo Labs databases and then performs some calculation with the result-set

#code is based off the psycopg2 tutorial wiki

#Attempt to connect to the database
import psycopg2

try:
    conn = psycopg2.connect("dbname='Alex' user='anders' host=alexpg' password=''")
except:
    print "I am unable to connect to the database"

#Define a cursor to work with
cur = conn.cursor()

#Use the cursor to try to execute a query
try: 
    cur.execute("""SELECT * 
        FROM scratch.hp_testing
        LIMIT 5""")
except: 
    print "I cannot execute the query."
#In the future, see if I can import a query from another file

#Create a list to put the results in
rows = cur.fetchall()

#Print the results
print "\nRows:\n"
for row in rows:
    print "    ", row[1]

