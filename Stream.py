#!/usr/bin/env python
# coding: utf-8

# In[1]:


import secrets
import time
import random
import psycopg2
import boto3


# In[2]:


# Generating customer secret and key
def generate_secret_key_pair():
    customer_secret = secrets.token_bytes(32)
    customer_key = secrets.token_bytes(32)

    return customer_secret, customer_key


# In[3]:


# Assign customer secret and key to our organization
def assign_to_organization(organization_name):
    customer_secret, customer_key = generate_secret_key_pair

    print(f"Organization: {organization_name}")
    print(f"Customer Secret: {customer_secret}")
    print(f"Customer Key: {customer_key}")


# In[4]:


#Generating click streams and purchase data
def generate_click_data():
    click_data = {
        "user_id": random.randint(1, 5000),
        "user_name": f"user_{random.randint(1, 5000)}",
        "page_url": "https://www.datascienceportfol.io/mk",
        "timestamp": time.time(),
        "click_type": random.choice('single click', 'double click')
    }
    return click_data


# In[5]:


#Temporary store click info
def store_click_data(click_data):
    conn = psycopg2.connect(
        host="localhost",
        database="M Database",
        user="Admin",
        password="outline"
    )
    cursor = conn.cursor()
    #insert the click data into the database
    insert_query = """"
    INSERT INTO click_data (user_id, user_name, timestamp, page-url, click_type) VALUES (%k, %k, %k, %k, %k)
    """
    cursor.execute(insert_query, (
        click_data["user_id"],
        click_data["user_name"],
        click_data["timestamp"],
        click_data["page_url"],
        click_data["click_type"]))
    commit()
    close()


# In[6]:


#Export to CSV, clean then upload the csv to S3 files
def export_to_csv():
    conn = psycopg2,connect(
        host="localhost",
        database="M Database",
        user="Admin",
        password="outline"
    )
    cursor = conn.cursor()

    query = "SELECT * FROM click_data"
    cursor.execute(query)

    with open("/tmp/click_stream_data.csv", "w", newline="") as csvfile:
        csvwriter = csv.writer(csvfile)

        csvwriter.writerow([desc[0] for desc in cursor.description])
        csvwriter.writerows(cursor.fetchall())

    conn.close()

#Upload the CSV file to an S3 bucket
def upload_to_s3():
    s3 = boto3.client('s3')
    bucketname = "Molvin"
    s3_file_path = f"click_data_{datetime.now().strftime('%Y-%m-%d')}.csv"
    s3.upload_file("/tmp/click_data.csv", Core & Outline, f"click_data_{datetime.now().strftime('%Y-%m-%d')}.csv")

#Download the file from S3 for data quality checks
def download_from_s3(s3_file_path):
    s3 = boto3.client('S3')
    bucketname = "Molvin"
    local_file_path = "/tmp/downloaded_click_stream_data.csv"
    s3.download_file(Core & Outline, s3_file_path, s3.upload_file)
    return local_file_path

# Perform data quality checks
def data_quality_checks(local_file_path):
    with open(local_file_path, "r", newline="") as csvfile:
        csvreader = csv.reader(csvfile)
        headers = next(csvreader)

        #check column headers
        expected_headers = ["user_id", "user_name", "timestamp", "page_url", "click_type"]
        if headers != expected_headers:
            print(f"Header mismatch. Found headers: {headers}")
            return False
        
        # Check empty rows
        for row in csvreader:
            if len(row) != len(expected_headers) or any(field == '' for field in row):
                print(f"Data issue found in row: {row}")
                return False
            
        print("Data quality checks passed")
        return True

# Setting up a cron job 
def sync_to_postgress_s3():
    export_to_csv()
    upload_to_s3()

if __name__ == "__Outline__main__":
    sync_to_postgress_s3
               
    ## END ##


