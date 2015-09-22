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

import sys, os

import user_stats as us
pd.options.mode.chained_assignment = None

domain = sys.argv[1]
isp = sys.argv[2]
update = sys.argv[3]
subject_split= sys.argv[4]

#Working/Saving Directory
os.chdir("/Users/wlee/wspace/EDS/output")

#N Day cutoff to determine when a user should be considered dropped for the dropped user variable
#We can also make this a strict definition
N_day = 14
csv_dump = 1
roll_date = 3
group_day = 14

#The funciton that calls the sql query
def sql_call(domain, isp="gmail"):
    #the sql call requires a domain and an isp... for what use?  UPDATE LATER.
    print("Connecting to Database and Running Query")

    #this is the database on which the query will run
    host = "emaildata.cqlai0yteoyb.us-east-1.redshift.amazonaws.com"

    #the following is connection information
    port = 5439
    user = "wlee"
    database = "eds" 

    #one method for providing your password in a more secure manner
    password = base64.b64decode(open("/Users/wlee/eds_sql.txt").read())

    #create a cursor, the object used to interact with a database
    cur = con.cursor(name="QTQueryDesuNe")

    #the query is broken down into multiple parts:
    #"the query we send should depend on whether or not we want it for a specific ISP."
    query_select = "SELECT message_id, user_id, message_time, from_domain, delivery_location, (CASE WHEN read_ts IS NOT NULL THEN 1 ELSE 0 END) email_read, (CASE WHEN trash_ts IS NOT NULL THEN 1 ELSE 0 END) email_trash, (CASE WHEN delete_ts IS NOT NULL THEN 1 ELSE 0 END) email_del, (CASE WHEN complaint_ts IS NOT NULL THEN 1 ELSE 0 END) email_comp, subject"

    table = " FROM eds.public.email_engagement_" + isp
    if "%" in domain:
        query_where = " WHERE from_domain LIKE \'" + domain + "\'"
        domain = domain.replace("%","")
    else:
        if type(domain) == type(" "):
            domainw = [domain]
        domains = '(\'' + "\',\'".join(domainw) + "\')"
        query_where = " WHERE from_domain IN " + domains
   query = 
