import sys
import subprocess
import platform
import os
import re
from datetime import datetime
import time

####################This function checks operating system and manage terminal commands################################################
def operating_system_dependencies_install(name):
    if platform.system()=='Windows':
        subprocess.call(['pip', 'install', name])
    else:
        try:
            subprocess.call(['sudo','pip', 'install', name])
        except:
            subprocess.call(['sudo', 'easy_install', name])

####################This function checks if the program executes first time then install dependecies################################################
def dependencies_installation():
    if not os.path.isfile(location('log.xlsx')):
        operating_system_dependencies_install('xlsxwriter')
        operating_system_dependencies_install('openpyxl')
        operating_system_dependencies_install('requests')

####################This function checks version of python################################################
def version_control():
    if sys.version_info[0]>2:
        return True
    else:
        return False

####################This is one line function to print starts################################################
def stars():
    print("*********************************************************************************************************************************************")

####################This function returns location of current working directory################################################
def location(name):
    file_name=name
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    location = os.path.join(__location__, file_name)
    return location

####################This function checks existanve of log.xlsx file, create log file and also insert data to file###############################################
def write_url(url,status_code,reason,total,percentage_match):
   try:
    file_name='log.xlsx'
    if not os.path.isfile(location(file_name)):
        sheet_formation(file_name)
    wb = openpyxl.load_workbook(location(file_name))
    rows = [(datetime.now()), url,status_code,reason,total,percentage_match]
    ws = wb.active
    ws.append(rows)
    wb.save(location(file_name))
   except Exception:
       print("Excel File Error!!!! \nFirst close log.xlsx file then start program again")
       sys.exit()

####################This is log.xlsx sheet formation function################################################
def sheet_formation(file_name):
    workbook = xlsxwriter.Workbook(location(file_name))
    worksheet = workbook.add_worksheet('History Log')
    worksheet.set_column(0, 0, 19)
    worksheet.set_column(1, 1, 45)
    worksheet.set_column(2, 2, 11)
    worksheet.set_column(3, 3, 10)
    worksheet.set_column(4, 4, 14)
    worksheet.set_column(5, 5, 35)
    bold = workbook.add_format({'bold': True})
    worksheet.write_string('A1', 'Date', bold)
    worksheet.write_string('B1', 'URL', bold)
    worksheet.write_string('C1', 'Status Code', bold)
    worksheet.write_string('D1', 'Reason', bold)
    worksheet.write_string('E1', 'Time Required', bold)
    worksheet.write_string('F1', 'Verification Percentage', bold)
    workbook.close()

####################This function takes URL from file and find the verification status############################################
def file_read():
 stars()

 try:
    file_name='config.txt'
    if not os.path.isfile(location(file_name)):
        print("First create a config.txt file then start the program again")
        sys.exit()
    else:
        print(" %-45s %-20s %-18s %0s %30s" % ("url", "Status", "Status Code", "Execution Time", "Verification Status"))
        with open(file_name) as f:
            lines = f.read().splitlines()
            for line in lines:
                i=0
                if line=='':
                    pass
                else:
                    data=line.strip().split("%%%")
                    url=data[0]
                    try:
                        if url[0:4] == "http":
                            url=url
                        else:
                            url = "http://" + url

                        start = datetime.now()
                        res = requests.get(url)
                        if len(data)>1:
                            keywords=data[1].strip().split(",")
                            for keyword in keywords:
                                matches = re.findall(keyword, str(res.content));
                                if len(matches) != 0:
                                    i=i+1
                            if i == len(keywords):
                                verification = "Fullfilled"
                            else:
                                verification = "Requirements are not fulfilled"
                        else:
                            verification = "No requirements were added in file"

                        finish = datetime.now()
                        total=finish-start

                    except ValueError:
                        res.reason='Invalid URL | No host supplied'
                        res.status_code= 'Invalid code'


                    print(" %-45s %-20s %-18s %0s %30s" % (url, res.reason, res.status_code, total,verification))
                    write_url(url,res.status_code,res.reason,total,verification)
 except EnvironmentError or ValueError:
     print("File Error!!!!!\nCheck presence of config.txt file\nIf no file found then create a new config.txt file and follow the instruction in readme.txt")
     value=user_str_input("Press R to restart, Q to quit and C to resume the program as it is: ").lower()
     decision(value)

####################Below mentioned three function are to take different datatypes input from user################################################
def decision(value):
    if value == "r":
        main()
    elif value == "q":
        sys.exit()
    elif value == "c":
        pass
    else:
        print("Incorrect input try again !!!")
        file_read()

def user_str_input(statement):
     if version_control():
            user=input(statement)
     else:
            user=raw_input(statement)
     return user

def user_int_input(statement):
    try:
        if version_control():
            user=int(input(statement))
        else:
            user=eval(raw_input(statement))
        return user
    except ValueError:
        print("Wrong input!!!!!\nInput can only be numbers(integers)\nTry again")
        main()

####################This function calls other functions to execute the program################################################
def main():
    stars()
    duration=user_int_input("Specify the time duration in seconds between two consective executions: ")
    while 1:
        file_read()
        time.sleep(duration)

####################Program execution starts here#################################################
if __name__=="__main__":
    dependencies_installation()
    import xlsxwriter
    import openpyxl
    import requests
    app=main()



