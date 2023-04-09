import sys
import datetime
import time
import fileinput
from typing import Final
import os
import pymysql
import logging
import boto3
import easygui
from botocore.exceptions import ClientError
from matplotlib import pylab as plt
import numpy as np
import pandas as pd
import matplotlib.patches as mpatches

global gv_region_name
gv_region_name = "eu-west-1"

def boto3_client(service, aws_access_key_id, aws_secret_access_key):
    connect = boto3.client(service, aws_access_key_id=aws_access_key_id,
                           aws_secret_access_key=aws_secret_access_key, region_name=gv_region_name)
    return connect



def WorkloadComparisonGenericVsPrivate(dbName, usr, pwd, aws_access_key_id, aws_secret_access_key):
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
	
        command = "imanueldb.Employee"
        cur = conn.cursor()
        mycommand = "select * from imanueldb.Workload"
        #print(mycommand)

        cur.execute(mycommand)

        myresult = cur.fetchall()

        mytitle = "Time\t\tG_Wards\t\tS_Wards\t\tG_AE\t\tS_AE\t\tG_GP\t\tS_GP\t\tG_Private\t\tS_Private\n\n"
        mytitle = "Time\n\n"
        
        deptlist = []
        minlist = []
        maxlist = []
        mycontents = mytitle
       
        listtime = []
        WardsGeneric = []
        WardsSpecialised = []
        AEGeneric = []
        AESpecialised = []
        GPGeneric = []
        GPSpecialised = []
        PrivateGeneric = []
        PrivateSpecialised = []
        for i in myresult:
           listtime.append(str(i[0]))
           WardsGeneric.append(int(i[1]))
           WardsSpecialised.append(int(i[2]))
           AEGeneric.append(int(i[3]))
           AESpecialised.append(int(i[4]))
           GPGeneric.append(int(i[5]))
           GPSpecialised.append(int(i[6]))
           PrivateGeneric.append(int(i[7]))
           PrivateSpecialised.append(int(i[8]))

        Wards = pd.DataFrame({"Time": listtime,
		    "Generic"        :  WardsGeneric,
                    "Specialised"    :  WardsSpecialised})

        AE = pd.DataFrame({"Time": listtime,
		    "Generic"        :  AEGeneric,
                    "Specialised"    :  AESpecialised})

        GP = pd.DataFrame({"Time": listtime,
		    "Generic"        :  GPGeneric,
                    "Specialised"    :  GPSpecialised})

        Private = pd.DataFrame({"Time": listtime,
		    "Generic"        :  PrivateGeneric,
                    "Specialised"    :  PrivateSpecialised})

        fig, axes = plt.subplots(nrows=1, ncols=4, figsize=(10,3))
        fig.subplots_adjust(hspace=1)

        Wards.plot(  ax = axes[0], x="Time", y=["Generic", "Specialised"], kind="bar")
        AE.plot(     ax = axes[1], x="Time", y=["Generic", "Specialised"], kind="bar")
        GP.plot(     ax = axes[2], x="Time", y=["Generic", "Specialised"], kind="bar")
        Private.plot(ax = axes[3], x="Time", y=["Generic", "Specialised"], kind="bar")

        axes[0].set_title('Wards')
        axes[0].set_ylabel('Number of Patient Samples', fontsize=10)
        axes[0].legend(loc="upper left", fontsize=8)

        axes[1].set_title('AE')
        axes[1].legend(loc="upper left", fontsize=8)

        axes[2].set_title('GP')
        axes[2].legend(loc="upper left", fontsize=8)

        axes[3].set_title('Private')
        axes[3].legend(loc="upper left", fontsize=8)

        plt.show()

        # To close the connection
        conn.close()
        #print("End : WorkloadComparisonGenericVsPrivate\n")


def main():
   f = open("C:\\Users\\Owner\\OneDrive\\CIT\\Comp Research Project Implem. COMP9028_27794\\PythonScripts\\AWS_credentials.txt", "r")
   file_data = f.read()
   # splitting the file data into lines
   lines = file_data.splitlines()
   f.close()
   d = dict(map(lambda s: s.split('='), lines))

   AccessKeyId=d['AccessKeyID']
   SecretAccessKey=d['SecretAccessKey']

   connect_list = WorkloadComparisonGenericVsPrivate(sys.argv[1], sys.argv[2], sys.argv[3], AccessKeyId, SecretAccessKey)
 



if __name__ == "__main__":
    main()











