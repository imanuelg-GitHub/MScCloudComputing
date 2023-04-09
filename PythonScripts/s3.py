import sys
import datetime
import time
import fileinput
from typing import Final
import os
import boto3
import easygui

global gv_region_name
gv_region_name = "eu-west-1"

def boto3_resource(service, aws_access_key_id, aws_secret_access_key):
    connect = boto3.resource(service, aws_access_key_id=aws_access_key_id,
                             aws_secret_access_key=aws_secret_access_key, region_name=gv_region_name)
    return connect


def aws_connectivity_s3(aws_access_key_id, aws_secret_access_key):    
    s3 = boto3_resource('s3', aws_access_key_id, aws_secret_access_key)
    mystr = ""
    for bucket in s3.buckets.all():
       #print(bucket.name + " : ")
       mystr += bucket.name + " : "
       for i in bucket.objects.all():
          #print("\t", i.key)
          mystr += "\t" + i.key
       #print(",\n")
       mystr += "\n"
    easygui.msgbox(mystr, title="S3 List Buckets Contents")
        



def main():
   f = open("C:\\Users\\Owner\\OneDrive\\CIT\\Comp Research Project Implem. COMP9028_27794\\PythonScripts\\AWS_credentials.txt", "r")
   file_data = f.read()
   # splitting the file data into lines
   lines = file_data.splitlines()
   f.close()
   d = dict(map(lambda s: s.split('='), lines))

   AccessKeyId=d['AccessKeyID']
   SecretAccessKey=d['SecretAccessKey']

   connect_list = aws_connectivity_s3(AccessKeyId, SecretAccessKey)
 

if __name__ == "__main__":
    main()











