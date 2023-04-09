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


def boto3_resource(service, aws_access_key_id, aws_secret_access_key):
    connect = boto3.resource(service, aws_access_key_id=aws_access_key_id,
                             aws_secret_access_key=aws_secret_access_key, region_name=gv_region_name)
    return connect

def aws_connectivity_rds123(dbName, usr, pwd, aws_access_key_id, aws_secret_access_key):
   print("dbName = [", dbName, "]")
   print("usr = [", usr, "]")
   print("pwd = [", pwd, "]")


def aws_connectivity_rds(dbName, usr, pwd, aws_access_key_id, aws_secret_access_key):
    rdsclient = boto3_client('rds', aws_access_key_id, aws_secret_access_key)
    resp = rdsclient.describe_db_instances()
    for i in resp["DBInstances"]:
        if i["DBInstanceIdentifier"] == dbName:
             print("\n\t\t\tCannot create", dbName, "as it already exists and in state", i["DBInstanceStatus"])
             time.sleep(SLEEP_DELAY * SLEEP_DELAY)
             break
    else:
            f = open("C:\\Users\\Owner\\OneDrive\\CIT\\Comp Research Project Implem. COMP9028_27794\\PythonScripts\\dbDetails.txt", "w")
            dbStr = "dbName=" + dbName + "\n"
            f.write(dbStr)
            dbPwd = "MasterUserPassword=" + pwd + "\n"
            f.write(dbPwd)
            dbUsr = "MasterUsername=" + usr + "\n"
            f.write(dbUsr)
            f.close()
            response = rdsclient.create_db_instance(
            AllocatedStorage=5,
            DBInstanceClass='db.t2.micro',
            DBInstanceIdentifier=dbName,
            DBName=dbName,
            Engine='MySQL',  # create MySQL database instance
            MasterUserPassword=pwd,  # just any root password
            MasterUsername=usr)  # just any root username
            print("\n\t\t\t", response["DBInstance"]["DBInstanceStatus"], ":", dbName, delay_message)
            waiter = rdsclient.get_waiter('db_instance_available')
            waiter.wait(DBInstanceIdentifier=dbName)




def main():

   f = open("C:\\Users\\Owner\\OneDrive\\CIT\\Comp Research Project Implem. COMP9028_27794\\PythonScripts\\AWS_credentials.txt", "r")
   file_data = f.read()
   # splitting the file data into lines
   lines = file_data.splitlines()
   f.close()
   d = dict(map(lambda s: s.split('='), lines))

   AccessKeyId=d['AccessKeyID']
   SecretAccessKey=d['SecretAccessKey']

   connect_list = aws_connectivity_rds(sys.argv[1], sys.argv[2], sys.argv[3], AccessKeyId, SecretAccessKey)
 
   print("Database ready")




if __name__ == "__main__":
    main()











