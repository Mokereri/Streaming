#!/usr/bin/env python
# coding: utf-8

# In[1]:


import psycopg2
import pandas as pd

conn = None
cur = None
def connect():
    global conn, cur
    if conn is not None and cur is not None:
        return conn, cur
    username = "postgres"
    password = 'postgres'
    host = 'localhost'
    port = 5432
    database = 'postgres'

    conn = psycopg2.connect(host=host, database=database,
                            user=username, password=password, port=port)
    cur = conn.cursor()
    cur.execute("SET search_path TO public")

    return conn, cur


# In[2]:


def createSessionInfo():
    conn, cur = connect()
    cur.execute("CREATE TABLE IF NOT EXISTS session( session_id VARCHAR, event_id VARCHAR, data_source_id INTEGER, start_date VARCHAR, end_date VARCHAR, browser VARCHAR, latitude FLOAT, item_clicked VARCHAR, longitude FLOAT, country VARCHAR, region VARCHAR, city VARCHAR, click_through BOOLEAN, synced BOOLEAN );")

def createPageInfo():
    conn, cur = connect()
    cur.execute("CREATE TABLE IF NOT EXISTS page( page_id VARCHAR, page_name VARCHAR, session_id VARCHAR, start_date VARCHAR, end_date VARCHAR, is_terminal BOOLEAN, synced BOOLEAN );")

def populatePageInfo(table_dict):
    print("Populating page table with: ", table_dict)
    
    conn, cur = connect()
    columns = str(tuple([i for i in table_dict.keys()])).replace("'","")
    values = tuple(table_dict.values())
    print(values)
    try:
        cur.execute(f"""
            INSERT INTO page
            {columns}
            VALUES {values}
        """)
        conn.commit()
        print("Record added")
    except Exception as e:
        conn.rollback()
        print(e)

def populateSessionInfo(table_dict):
    createSessionTable()
    conn, cur = connect()
    columns = str(tuple([i for i in table_dict.keys()])).replace("'","")
    values = tuple(table_dict.values())
    print(values)
    try:
        cur.execute(f"""
            INSERT INTO session
            {columns}
            VALUES {values}
        """)
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(e)

def updateSessionInfo(table_dict):
    createSessionInfo()
    conn, cur = connect()
    try:
        cur.execute(f"""UPDATE session SET {' , '.join([str(i[0])+"="+"'"+str(i[1])+"'" for i in table_dict.items() if i[0] != "session_id"])} WHERE session_id={"'"+table_dict['session_id']+"'"};""")
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(e)

def getData(table_dict, table):
    conn, cur = connect()
    df = pd.read_sql("SELECT * FROM session", con=conn)
    print(df)
    return df
    

# getData("","")

