import sys
import datetime
import time
import fileinput
from typing import Final
import os
import boto3

global gv_region_name
gv_region_name = "eu-west-1"

SLEEP_DELAY: Final = 2
delay_message = "this could take up to 10 minutes... Please wait..."


def boto3_client(service, aws_access_key_id, aws_secret_access_key):
    connect = boto3.client(service, aws_access_key_id=aws_access_key_id,
                           aws_secret_access_key=aws_secret_access_key, region_name=gv_region_name)
    return connect







def listDatabases(aws_access_key_id, aws_secret_access_key):
    rdsclient = boto3_client('rds', aws_access_key_id, aws_secret_access_key)
    resp = rdsclient.describe_db_instances()
    #print(resp)
    for i in resp["DBInstances"]:
        print(i["Endpoint"]["Address"])
    

def main():

   f = open("C:\\Users\\Owner\\OneDrive\\CIT\\Comp Research Project Implem. COMP9028_27794\\PythonScripts\\AWS_credentials.txt", "r")
   file_data = f.read()
   # splitting the file data into lines
   lines = file_data.splitlines()
   f.close()
   d = dict(map(lambda s: s.split('='), lines))

   AccessKeyId=d['AccessKeyID']
   SecretAccessKey=d['SecretAccessKey']

   connect_list = listDatabases(AccessKeyId, SecretAccessKey)
 





if __name__ == "__main__":
    main()











