import sys
import datetime
import time
import fileinput
from typing import Final
import os
import boto3

global gv_region_name
gv_region_name = "eu-west-1"

def boto3_resource(service, aws_access_key_id, aws_secret_access_key):
    connect = boto3.resource(service, aws_access_key_id=aws_access_key_id,
                             aws_secret_access_key=aws_secret_access_key, region_name=gv_region_name)
    return connect


def populate_buckets_dict(aws_access_key_id, aws_secret_access_key):
    s3 = boto3_resource('s3', aws_access_key_id, aws_secret_access_key) 
    buckets_dict = {}
    j = 1
    for bucket in s3.buckets.all():
        buckets_dict[j] = bucket.name  # populate dict using bucket names
        #print("\t\t\t\t", j, ":", buckets_dict[j])
        j = j + 1

    return buckets_dict

        
def uploadObject(myfile, bucket_selection, aws_access_key_id, aws_secret_access_key, buckets_dict):
    print("myfile = [", myfile, "]")
    s3 = boto3_resource('s3', aws_access_key_id, aws_secret_access_key) 
    data = open(myfile, 'rb')
    s3.Bucket(buckets_dict[int(bucket_selection)]).put_object(Key=myfile, Body=data)
    


def main():
   f = open("C:\\Users\\Owner\\OneDrive\\CIT\\Comp Research Project Implem. COMP9028_27794\\PythonScripts\\AWS_credentials.txt", "r")
   file_data = f.read()
   # splitting the file data into lines
   lines = file_data.splitlines()
   f.close()
   d = dict(map(lambda s: s.split('='), lines))

   AccessKeyId=d['AccessKeyID']
   SecretAccessKey=d['SecretAccessKey']

   buckets_dict = {}
   buckets_dict = populate_buckets_dict(AccessKeyId, SecretAccessKey)
   
   for x, y in buckets_dict.items():
      print(x, y)
 
   uploadObject(sys.argv[1], sys.argv[2], AccessKeyId, SecretAccessKey, buckets_dict)



if __name__ == "__main__":
    main()











