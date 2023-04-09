import sys
import datetime
import time
import fileinput
from typing import Final
import os
import pymysql
import logging
import boto3
from botocore.exceptions import ClientError

global gv_region_name
gv_region_name = "eu-west-1"

def boto3_client(service, aws_access_key_id, aws_secret_access_key):
    connect = boto3.client(service, aws_access_key_id=aws_access_key_id,
                           aws_secret_access_key=aws_secret_access_key, region_name=gv_region_name)
    return connect



def mysqlCreateTable(dbName, usr, pwd, command, aws_access_key_id, aws_secret_access_key):
        rdsclient = boto3_client('rds', aws_access_key_id, aws_secret_access_key)
        resp = rdsclient.describe_db_instances()
        for i in resp["DBInstances"]:
           #print(i["Endpoint"]["Address"])
           break

	# To connect MySQL database
        conn = pymysql.connect(
               host=i["Endpoint"]["Address"],
               user=usr,
               password = pwd)
	
        cur = conn.cursor()
        cur.execute(command)
        
        # To close the connection
        conn.close()

        filename = command.replace("create table ", "")
        index = filename.index("(")
        #print("[" + str(filename[0:index]) + "]")
        myfile = "C:\\Users\\Owner\\OneDrive\\CIT\\Comp Research Project Implem. COMP9028_27794\\PythonScripts\\" + str(filename[0:index]) + ".txt"
        #print(myfile)
        f = open(myfile, "w")
        f.write(command)   
        f.close()
        print("Table created ", command)


def main():
   f = open("C:\\Users\\Owner\\OneDrive\\CIT\\Comp Research Project Implem. COMP9028_27794\\PythonScripts\\AWS_credentials.txt", "r")
   file_data = f.read()
   # splitting the file data into lines
   lines = file_data.splitlines()
   f.close()
   d = dict(map(lambda s: s.split('='), lines))

   AccessKeyId=d['AccessKeyID']
   SecretAccessKey=d['SecretAccessKey']
   connect_list = mysqlCreateTable(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], AccessKeyId, SecretAccessKey)
 



if __name__ == "__main__":
    main()











