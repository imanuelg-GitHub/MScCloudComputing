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
import matplotlib.pyplot as plt
import numpy as np

global gv_region_name
gv_region_name = "eu-west-1"

def boto3_client(service, aws_access_key_id, aws_secret_access_key):
    connect = boto3.client(service, aws_access_key_id=aws_access_key_id,
                           aws_secret_access_key=aws_secret_access_key, region_name=gv_region_name)
    return connect



def MinandMaxSalaryByDept(dbName, usr, pwd, aws_access_key_id, aws_secret_access_key):
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
        mycommand = "select * from ( select e.dept, min(hourly_rate) over(partition by dept order by dept) as min_hr, max(hourly_rate) over(partition by dept order by dept) as max_hr from imanueldb.Employee e) as e group by e.dept, e.min_hr, e.max_hr"
        #print(mycommand)

        cur.execute(mycommand)

        myresult = cur.fetchall()

        mytitle = "Department\t\tMinHourlyRate\t\tMaxHourlyRate\n\n"

        
        deptlist = []
        minlist = []
        maxlist = []
        mycontents = mytitle

        for i in myresult:
           deptlist.append(i[0])
           minlist.append(float(i[1]))
           maxlist.append(float(i[2]))
           for j in i:
              mycontents += str(j) + "\t\t"
           mycontents += "\n\n\n"

        easygui.msgbox(mycontents, title="Min and Max Salary By Dept")
        
        data = {'MaxSalary': np.array([]),'MinSalary': np.array([]),}

        # Adding list as value
        data["MaxSalary"] = maxlist
        data["MinSalary"] = minlist

        width = 0.4
        plt.rcParams.update({'font.size': 30})
        fig, ax = plt.subplots()
        
        bottom = np.zeros(4)
        for ii, k in data.items():
           p = ax.bar(deptlist, k, width, label=ii, bottom=bottom)
           bottom += k
           ax.bar_label(p, label_type='center')

        ax.set_xlabel('Dept')
        ax.set_ylabel('Salary')
        ax.set_title('Min and Max Salary By Dept')
        ax.legend(fontsize=20, loc="upper right")
        plt.show()

        # To close the connection
        conn.close()
        #print("End : MinandMaxSalaryByDept\n")


def main():
   f = open("C:\\Users\\Owner\\OneDrive\\CIT\\Comp Research Project Implem. COMP9028_27794\\PythonScripts\\AWS_credentials.txt", "r")
   file_data = f.read()
   # splitting the file data into lines
   lines = file_data.splitlines()
   f.close()
   d = dict(map(lambda s: s.split('='), lines))

   AccessKeyId=d['AccessKeyID']
   SecretAccessKey=d['SecretAccessKey']

   connect_list = MinandMaxSalaryByDept(sys.argv[1], sys.argv[2], sys.argv[3], AccessKeyId, SecretAccessKey)
 



if __name__ == "__main__":
    main()











