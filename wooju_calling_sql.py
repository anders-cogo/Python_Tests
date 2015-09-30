#Anders Simpson-Wolf
#09/17/2015
#A script written in python that makes a sql query
#This code was originally written by Wooju Lee, I am adding comments for my own sake
#Personal information, like username and password, have also been modified with the 
    #intention of executing this code myself

#NOTE: other functions defined in the file are- from_csv and main
#NOTE: global variables are- domain, isp, update, subject_split, N_day, csv_dump, roll_date, and group_day

#the pandas library is a Python data analysis library
import pandas as pd
#the NumPy library is a fundamental package for scientific computing with Python
import numpy as np
#datetime supplies classes for maipulating dates and times
import datetime
#provides data endocing and decoding as specified in RFC 3548
import base64
#the psycopg2 library provides methods for linking Python and PostgreSQL
import psycopg2
#operating systems library
import sys, os
#a library of functions Wooju made to generate/calculate user statistics
import user_stats as us
#
pd.options.mode.chained_assignment = None

#defines theese variables in terms of arguments given on the command line
domain = sys.argv[1] #domain you are specifying in the query
isp = sys.argv[2] #isp you are specifying in the query
update = sys.argv[3] #do you want to update a .csv file
subject_split= sys.argv[4] #do you want to split the subjects in the results table into multiple sections

#Working/Saving Directory
#os.chdir - use the operating system to change the directory
os.chdir("/Users/anders/Documents/Learning/Python/Python_Tests")

#N Day cutoff to determine when a user should be considered dropped for the dropped user variable
#We can also make this a strict definition
N_day = 14
csv_dump = 1
roll_date = 3
group_day = 14

#The funciton that calls the sql query
def sql_call(domain, isp="gmail"):
    #the sql call requires a domain and an isp... for what use? And why set to gmaiil? UPDATE LATER.
    print("Connecting to Database and Running Query")

    #this is the database on which the query will run
    #This particular host is the EDS database
    host = "emaildata.cqlai0yteoyb.us-east-1.redshift.amazonaws.com"

    #the following is connection information
    port = 5439
    user = "anders"
    database = "eds" 

    #one method for providing your password in a more secure manner
    #UPDATE WITH YOUR OPEN PASSWORD FILE
    password = base64.b64decode(open("/Users/wlee/eds_sql.txt").read())

    #create a connection
    conn = psychopg2.connect(database=database, user=user, host=host, port=port, password=password, sslmode='allow')
    #create a cursor, the object used to interact with a database
    cur = con.cursor(name="QTQueryDesuNe")

    #the query is broken down into multiple parts:
    #"the query we send should depend on whether or not we want it for a specific ISP."
    #this SELECT part of the query looks like it chooses every columns from the EDS table
    #With the notable change that read, trash, delete, and complaint metrics are binary (instead of giving a time)
    query_select = "SELECT message_id, user_id, message_time, from_domain, delivery_location, (CASE WHEN read_ts IS NOT NULL THEN 1 ELSE 0 END) email_read, (CASE WHEN trash_ts IS NOT NULL THEN 1 ELSE 0 END) email_trash, (CASE WHEN delete_ts IS NOT NULL THEN 1 ELSE 0 END) email_del, (CASE WHEN complaint_ts IS NOT NULL THEN 1 ELSE 0 END) email_comp, subject"

    #the FROM part of the query
    table = " FROM eds.public.email_engagement_" + isp

    #the WHERE part of the query
    #Can be either all variants on a domain (ie: LIKE %yahoo%) or a list of domains (ie: google, cogo, etc)
    if "%" in domain:
        query_where = " WHERE from_domain LIKE \'" + domain + "\'"
        domain = domain.replace("%","")
    else: #CONFUSION HERE
        if type(domain) == type(" "):
            domainw = [domain]
        domains = '(\'' + "\',\'".join(domainw) + "\')" 
        query_where = " WHERE from_domain IN " + domains

   #the query statement is the conjoined SELECT, FROM, and WHERE statements
   query = query_select + table + query_where

   #print and execute the query
   print(query)
   cur.execute(query)

   #fetch the first 500000 rows from the results table
   b1 = pd.DataFrame(cur.fetchmany(500000))
   #continue to fetch results, 500000 at a time, until all are recorded in b1
   while(True):
       a = cur.fetchmany(500000)
       print(len(a))
       if a:
           b1 = b1.append(pd.DataFrame(a))
       else:
           break

   #close the connection
   conn.close()

   #label the columns of b1
   b1.columns = ["message_id", "user_id", "message_time", "from_domain", "delivery_location", "email_read", "email_trash", "email_del", "email_comp", "subject"]

   #csv_dump is determined explicitly here in the script.  Used to decide how the table of data is handled
   #if csv_dump = 1, then the table b1 is turned into a .csv file
   if csv_dump == 1:
       b1.to_csv("raw_" + domain[0] + "_" + str(datetime.date.today()) + ".csv", sep="\16") #What is \16?

   #finds the "date" column in b1, then formats the strings there as dates
   b1['date'] = b1.message_time.values.astype('M8[D]')
   return(b1)

def from_csv(domain, isp="gmail"):
    #get the latest file

    #get rid of any "%" symbols in the domain/list of domains
    temp_domain = domain.replace("%","")
    #Get list of files in the current directory 
    flist = os.listdir(os.getcwd())

    #For each item in the current working directoy, see if the csv file is there
    flist = [a for a in flist if "raw_" + temp_domain in a]
    if flist:
        flist.sort()
        print("Loading CSV: " + str(flist[-1]))

        #update b1 to have the most recent csv file
        b1 = pd.read_csv(flist[-1], sep="\16", parse_dates=[3])
        #generate the following: First Date and Last Date per user
        #look at the 'date' column and format the strings there as dates
        b1['date'] = b1.message_time.values.astype('M8[D]')
        print("Successfully loaded CSV!")
        return(b1)
    else:
        #if csv file is not found, print out a message saying so
        print("File not found: Running SQL Query")
        #Then execute the SQL query to generate the desired .csv file
        return(sql_call(domain,isp))

def main(domain, isp):
    #if the isp is not in a list of target isps, default to gamil
    if isp not in ["gmail", "yahoo", "aol"]:
        isp = "gmail"

    #sql query
    if update == "1": #update is a value specified in the command line as this script is executed
        df = sql_call(domain, isp) #run the SQL query
    #from csv
    else:
        #if not updating a .csv file, then... what is this step?
        df = from_csv(domain, isp)

    #delete all "%" symbols from the domain/list of domains
    domain = domain.replace("%","")

    first_date = us.first_engage(df)
    
    #calculate user statistics, as characterized explicitly by the script early on
    print("Calculating User Stats")
    #the us library is full of functions Wooju wrote.  They perform certain bits of analysis he found useful, but which were specific to his work at the time.
    u_df = us.user_stats(df, N_dat, roll_date, group_day)
    u_df = us.clear_engagement(u_df, first_date)

    #output the user stats to a .csv file
    u_df.to_csv("user_" + domain + str(datetime.date.today()) + ".csv")

    #plot the user stats vs domain/domains
    print("Generating plots")
    us.gen_plot(u_df, domain)

    #Calculate cadence stats and cumulative total stats
    print("Generating Cadence Stats")
    us.cadence_stats(df, N_day, roll_date, group_day).to_csv("cadence_" + domain + str(datetime.date.today()) + ".csv")
    print("Generating Cumulative Plots")
    us.running_cumulative_todal(df,domain)

    #now we filter by subject
    if subject_split == "1":
        #subject_split is the final argument gotten from the command line when this script is executed

        #count the total number of subjects in the file
        total = df['subject'].count()

        sub_count = pd.DataFrame(df['subject'].value_counts())
        sub_count.columns = ['emailcount']
        sub_count['cumulative'] = sub_count.emailcount.cumsum()

        #Two filters, used to break up the results into thrids (filter1 = first third, filter2 = second third)
        filter1 = total/3
        filter2 = filter1*2

        #create sublists 1, 2, and 3 to divide up the subjects
        sublist1 = sub_count[sub_count.cumulative <= filter1].index #.index?

        #these variables "a" and "b" are just getting the index values where section 2 begins and ends
        a = sub_count.cumulative > filter1
        b = sub_count.cumulative <= filter2
        sublist2 = sub_count[a & b].index
        sublist3 = sub_count[sub_count.cumulative > filter2].index

        #split them into three groups
        #seperate user stats into 3 sections
        u_df1 = us.user_stats(df[df.subject.isin(sunlist1)])
        u_df2 = us.user_stats(df[df.subject.isin(sunlist2)])
        u_df3 = us.user_stats(df[df.subject.isin(sunlist3)])

        #send user stats to their own .csv files
        u_df1.to_csv("user_sub1_" + domain + str(datetime.date.today()) + ".csv")
        u_df2.to_csv("user_sub2_" + domain + str(datetime.date.today()) + ".csv")
        u_df3.to_csv("user_sub3_" + domain + str(datetime.date.today()) + ".csv")
        
        #generate plots for the user stats
        us.gen_plot(u_df1, domain, 'sub1')
        us.gen_plot(u_df2, domain, 'sub2')
        us.gen_plot(u_df3, domain, 'sub3')

#call the main function to begin the process of executing the query
main(domain, isp)
