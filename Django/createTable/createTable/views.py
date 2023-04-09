from django.shortcuts import render
import requests
from django.db import connection
import sys
import subprocess
import os
from subprocess import run,Popen,PIPE
from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.template import loader


def homepage(request):
   return render(request, 'index.html')
   

def populateTab(request):
   out=""
   mystr=""
   if request.method=="POST":
       #print(request.POST.get('tableName'))
       f = open("C:\\Users\\Owner\\OneDrive\\CIT\\Comp Research Project Implem. COMP9028_27794\\PythonScripts\\dbDetails.txt", "r")
       file_data = f.read()
       # splitting the file data into lines
       lines = file_data.splitlines()
       f.close()
       d = dict(map(lambda s: s.split('='), lines))

       dbName=d['dbName']
       dbUser=d['MasterUsername']
       dbPwd=d['MasterUserPassword']

       command=request.POST.get('tableName')
       #print("command = [", command, "]")

       #out=run([sys.executable, "C:\\Users\\Owner\\OneDrive\\CIT\\Comp Research Project Implem. COMP9028_27794\\PythonScripts\populateTable.py",dbName, dbUser, dbPwd, command], shell=False, stdout=PIPE)
       #print("Table output:", out)
       cmd = "python \"C:\\Users\\Owner\\OneDrive\\CIT\\Comp Research Project Implem. COMP9028_27794\\PythonScripts\\populateTable.py\"" + " " + dbName + " " + dbUser + " " + dbPwd + " " + "\"" + command + "\""
       #print("cmd = [" + cmd + "]")
       out = os.popen(cmd).read().split('\n')
       #print("DB output :", out)
       mystr = " "
       for i in out:
         mystr += i + " " + "\n"
   return render(request, 'populateTab.html', {'data2':mystr})


def createTab(request):
   out=""
   mystr=""
   if request.method=="POST":
       #print(request.POST.get('tableName'))
       f = open("C:\\Users\\Owner\\OneDrive\\CIT\\Comp Research Project Implem. COMP9028_27794\\PythonScripts\\dbDetails.txt", "r")
       file_data = f.read()
       # splitting the file data into lines
       lines = file_data.splitlines()
       f.close()
       d = dict(map(lambda s: s.split('='), lines))

       dbName=d['dbName']
       dbUser=d['MasterUsername']
       dbPwd=d['MasterUserPassword']

       tableName=request.POST.get('tableName')
       newTableName = "create table " + d['dbName'] + "."
       command = tableName.replace('create table ', newTableName)
       #print(command)
       #out=run([sys.executable, "C:\\Users\\Owner\\OneDrive\\CIT\\Comp Research Project Implem. COMP9028_27794\\PythonScripts\createTable.py",dbName, dbUser, dbPwd, command], shell=False, stdout=PIPE)
       #print("Table output:", out)
       cmd = "python \"C:\\Users\\Owner\\OneDrive\\CIT\\Comp Research Project Implem. COMP9028_27794\\PythonScripts\\createTable.py\"" + " " + dbName + " " + dbUser + " " + dbPwd + " " + "\"" + command + "\""
       #print("cmd = [" + cmd + "]")
       out = os.popen(cmd).read().split('\n')
       #print("DB output :", out)
       mystr = " "
       for i in out:
         mystr += i + " " + "\n"
   return render(request, 'createTab.html', {'data1':mystr})


def createMySQLdb(request):
   out_db=""
   mystr=""
   #if request.method=="POST" and request.POST.get('dbName'):
   if request.method=="POST":
       #cursor=connection.cursor()
       #cursor.execute(request.POST.get('dbName'))
       dbName=request.POST.get('dbName')
       dbUser=request.POST.get('dbUser')
       dbPwd=request.POST.get('dbPwd')
       #out_db=run([sys.executable, "C:\\Users\\Owner\\OneDrive\\CIT\\Comp Research Project Implem. COMP9028_27794\\PythonScripts\createDatabase.py",dbName, dbUser, dbPwd], shell=False, stdout=PIPE)
       cmd = "python \"C:\\Users\\Owner\\OneDrive\\CIT\\Comp Research Project Implem. COMP9028_27794\\PythonScripts\\createDatabase.py\"" + " " + dbName + " " + dbUser + " " + dbPwd
       #print(cmd)
       out_db = os.popen(cmd).read().split('\n')
       #print("DB output :", out_db)
       mystr = " "
       for i in out_db:
         mystr += i + " " + "\n"
   return render(request, 'createMySQLdb.html', {'db_data1':mystr})


def listS3buckets(request):
   output=""
   mystr=""
   context={}
   if request.method=="POST":
       template = loader.get_template('template.html')
       #output=run([sys.executable, "C:\\Users\\Owner\\OneDrive\\CIT\\Comp Research Project Implem. COMP9028_27794\\PythonScripts\\s3.py"], shell=False, stdout=PIPE, universal_newlines=True)
       cmd = "python \"C:\\Users\\Owner\\OneDrive\\CIT\\Comp Research Project Implem. COMP9028_27794\\PythonScripts\\s3.py\""
       #print(cmd)
       output = os.popen(cmd).read().split('\n')
       mystr = " "
       for i in output:
         mystr += i + " " + "\n"
       context = {'s3_data':mystr}
       #print("typeoutput = ", type(output))
       #print("output.stdout = ", type(output.stdout))
       #print("typecontext = ", type(context))
       #print("types3_data = ", type('s3_data'))
   return render(request, 'listS3buckets.html', context)
   #return HttpResponse(template.render(context, request))
   #else:
   #    return render(request, 'listS3buckets.html')


def uploadS3(request):
   out_s3upload=""
   context={}
   if request.method=="POST":
       myfile=request.POST.get('myfile')
       bucketNumber=request.POST.get('bucketNumber')
       out_s3upload=run([sys.executable, "C:\\Users\\Owner\\OneDrive\\CIT\\Comp Research Project Implem. COMP9028_27794\\PythonScripts\s3_upload.py",myfile,bucketNumber], shell=False, stdout=PIPE)
       #print("S3 upload output :", out_s3upload)
   return render(request, 'uploadS3.html', context)


def viewTab(request):
   out=""
   mystr=""
   if request.method=="POST":
       #print(request.POST.get('tableName'))
       f = open("C:\\Users\\Owner\\OneDrive\\CIT\\Comp Research Project Implem. COMP9028_27794\\PythonScripts\\dbDetails.txt", "r")
       file_data = f.read()
       # splitting the file data into lines
       lines = file_data.splitlines()
       f.close()
       d = dict(map(lambda s: s.split('='), lines))

       dbName=d['dbName']
       dbUser=d['MasterUsername']
       dbPwd=d['MasterUserPassword']

       command=request.POST.get('tableName')
       cmd = "python \"C:\\Users\\Owner\\OneDrive\\CIT\\Comp Research Project Implem. COMP9028_27794\\PythonScripts\\viewTable.py\"" + " " + dbName + " " + dbUser + " " + dbPwd + " " + command
       #print(cmd)
       out = os.popen(cmd).read().split('\n')
       mystr = " "
       for i in out:
         mystr += i + " " + "\n"
   return render(request, 'viewTab.html', {'data4':mystr})


def RochevsAbbottAnalysersComparison(request):
   out=""
   mystr=""
   if request.method=="POST":
       #print(request.POST.get('tableName'))
       f = open("C:\\Users\\Owner\\OneDrive\\CIT\\Comp Research Project Implem. COMP9028_27794\\PythonScripts\\dbDetails.txt", "r")
       file_data = f.read()
       # splitting the file data into lines
       lines = file_data.splitlines()
       f.close()
       d = dict(map(lambda s: s.split('='), lines))

       dbName=d['dbName']
       dbUser=d['MasterUsername']
       dbPwd=d['MasterUserPassword']

       command=request.POST.get('tableName')
       cmd = "python \"C:\\Users\\Owner\\OneDrive\\CIT\\Comp Research Project Implem. COMP9028_27794\\PythonScripts\\AnalysersPerformance.py\"" + " " + dbName + " " + dbUser + " " + dbPwd + " " + command
       #print(cmd)
       out = os.popen(cmd).read().split('\n')
       mystr = " "
       for i in out:
         mystr += i + " " + "\n"
   return render(request, 'RochevsAbbottAnalysersComparison.html', {'data5':mystr})


def RochevsAbbottAnalysersResultsComparison(request):
   out=""
   mystr=""
   if request.method=="POST":
       #print(request.POST.get('tableName'))
       f = open("C:\\Users\\Owner\\OneDrive\\CIT\\Comp Research Project Implem. COMP9028_27794\\PythonScripts\\dbDetails.txt", "r")
       file_data = f.read()
       # splitting the file data into lines
       lines = file_data.splitlines()
       f.close()
       d = dict(map(lambda s: s.split('='), lines))

       dbName=d['dbName']
       dbUser=d['MasterUsername']
       dbPwd=d['MasterUserPassword']

       command=request.POST.get('tableName')
       cmd = "python \"C:\\Users\\Owner\\OneDrive\\CIT\\Comp Research Project Implem. COMP9028_27794\\PythonScripts\\AnalysersResultsComparison.py\"" + " " + dbName + " " + dbUser + " " + dbPwd + " " + command
       #print(cmd)
       out = os.popen(cmd).read().split('\n')
       mystr = " "
       for i in out:
         mystr += i + " " + "\n"
   return render(request, 'RochevsAbbottAnalysersResultsComparison.html', {'data6':mystr})


def MinandMaxSalaryByDept(request):
   output=""
   mystr=""
   context={}
   if request.method=="POST":
       #print(request.POST.get('tableName'))
       f = open("C:\\Users\\Owner\\OneDrive\\CIT\\Comp Research Project Implem. COMP9028_27794\\PythonScripts\\dbDetails.txt", "r")
       file_data = f.read()
       # splitting the file data into lines
       lines = file_data.splitlines()
       f.close()
       d = dict(map(lambda s: s.split('='), lines))

       dbName=d['dbName']
       dbUser=d['MasterUsername']
       dbPwd=d['MasterUserPassword']
       template = loader.get_template('template.html')
       #output=run([sys.executable, "C:\\Users\\Owner\\OneDrive\\CIT\\Comp Research Project Implem. COMP9028_27794\\PythonScripts\\MinandMaxSalaryByDept.py"], shell=False, stdout=PIPE, universal_newlines=True)
       cmd = "python \"C:\\Users\\Owner\\OneDrive\\CIT\\Comp Research Project Implem. COMP9028_27794\\PythonScripts\\MinandMaxSalaryByDept.py\"" + " " + dbName + " " + dbUser + " " + dbPwd
       #print(cmd)
       output = os.popen(cmd).read().split('\n')
       mystr = " "
       for i in output:
         mystr += i + " " + "\n"
       context = {'da1_data':mystr}
   return render(request, 'MinandMaxSalaryByDept.html', context)


def WorkloadComparisonGenericVsPrivate(request):
   output=""
   mystr=""
   context={}
   if request.method=="POST":
       #print(request.POST.get('tableName'))
       f = open("C:\\Users\\Owner\\OneDrive\\CIT\\Comp Research Project Implem. COMP9028_27794\\PythonScripts\\dbDetails.txt", "r")
       file_data = f.read()
       # splitting the file data into lines
       lines = file_data.splitlines()
       f.close()
       d = dict(map(lambda s: s.split('='), lines))

       dbName=d['dbName']
       dbUser=d['MasterUsername']
       dbPwd=d['MasterUserPassword']
       template = loader.get_template('template.html')
       #output=run([sys.executable, "C:\\Users\\Owner\\OneDrive\\CIT\\Comp Research Project Implem. COMP9028_27794\\PythonScripts\\WorkloadComparisonGenericVsPrivate.py"], shell=False, stdout=PIPE, universal_newlines=True)
       cmd = "python \"C:\\Users\\Owner\\OneDrive\\CIT\\Comp Research Project Implem. COMP9028_27794\\PythonScripts\\WorkloadComparisonGenericVsPrivate.py\"" + " " + dbName + " " + dbUser + " " + dbPwd
       #print(cmd)
       output = os.popen(cmd).read().split('\n')
       mystr = " "
       for i in output:
         mystr += i + " " + "\n"
       context = {'da2_data':mystr}
   return render(request, 'WorkloadComparisonGenericVsPrivate.html', context)
