Instruction:

Config.txt
1- User first needs to create a config.txt file in working directory.
2- Structure of config.txt must looks like URL%%%keywords | URL%%%k1,k2,k3,k4,k5,k6,........
3- Each line in config.txt consists of URL and keywords seperated by three "%", which is used to split the structure in program.
4- Keywords must be seperated by ",".
5- File may contains as many URLS and keywords as administrator wants.

Program Execution:
1- User needs to enter an interval time between two executions.
2- Program generates responses both on console and in log.xlsx file which will automatically be created by program.
3- If there is an error in config.txt or in config.txt files, then program displays the error and needs user input from console.
4- log.txt file shows the time upto seconds but console displays the time upto millisecond interval.
5- Program controls the installation of dependencies as well as python version control.


Sample template of config.txt is provided with source code.

