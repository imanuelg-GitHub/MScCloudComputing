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
import re

global gv_region_name
gv_region_name = "eu-west-1"

def boto3_client(service, aws_access_key_id, aws_secret_access_key):
    connect = boto3.client(service, aws_access_key_id=aws_access_key_id,
                           aws_secret_access_key=aws_secret_access_key, region_name=gv_region_name)
    return connect



def viewDetails(dbName, usr, pwd, command, aws_access_key_id, aws_secret_access_key):
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

        mycontents = "Test\t\tRoche\t\tAbbott\t\tDifference\t\tValidity\n\n"
        mycommand = "SELECT count(*) from " + command
        cur.execute(mycommand)
        myresultcount = cur.fetchall()

        res = int(re.sub(r'\D', '', ''.join(map(str, myresultcount)))) # convert tuple to integer

        for x in range(1,res):
           cur.execute('SET @row_number = ' + str(x))
           mycommand = "select * from ( \
                         SELECT *, \
		         CASE \
		            WHEN (test_conducted = 'HIV' and difference > 1) THEN 'Abnormal' \
                            WHEN (test_conducted = 'Glucose' and difference > 6.5) THEN 'Abnormal' \
                            WHEN (test_conducted = 'Pregnancy' and difference > 1 and difference < 60000) THEN 'Abnormal' \
                            WHEN (test_conducted = 'Cholesterol' and difference > 6.5) THEN 'Abnormal' \
                           ELSE 'Normal' \
		         END AS Validity \
                     from \
                     ( \
			SELECT * from \
			( \
				SELECT test_conducted, result as Roche, next_result as Abbott, round(abs(result-next_result),2) as difference from \
				( \
				SELECT \
					test_conducted, result, LEAD(result) over(partition by test_conducted) as next_result, \
					row_number() over(partition by test_conducted) as rn \
				FROM " + command + "\
				) a \
				WHERE rn = @row_number \
			) b \
                     ) c \
                    ) d where Validity = 'Abnormal'"

           #print(mycommand + "\n\n")
           cur.execute(mycommand)

           myresult = cur.fetchall()

           
           for i in myresult:
              iList = list(i)
              #print("***************" + str(iList) + "*******************\n\n\n")
              for x in iList:
                mycontents += str(x) + "\t\t"
              mycontents += "\n"
           

        #mycontents = "Analyser\t\tTest\t\tmin(minutes)\t\tmax(minutes)\t\tavg(minutes)\n"
        
        #for i in myresult:
        #   for j in i:
        #      mycontents += str(j) + "\t\t"
        #   mycontents += "\n"
        
        #print(test_conducted_dict)
        easygui.msgbox(mycontents, title="Roche vs. Abbott analysers results analysis comparison")

        # To close the connection
        conn.close()
        #print("End : viewDetails\n")


def main():
   f = open("C:\\Users\\Owner\\OneDrive\\CIT\\Comp Research Project Implem. COMP9028_27794\\PythonScripts\\AWS_credentials.txt", "r")
   file_data = f.read()
   # splitting the file data into lines
   lines = file_data.splitlines()
   f.close()
   d = dict(map(lambda s: s.split('='), lines))

   AccessKeyId=d['AccessKeyID']
   SecretAccessKey=d['SecretAccessKey']

   connect_list = viewDetails(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], AccessKeyId, SecretAccessKey)
 



if __name__ == "__main__":
    main()











