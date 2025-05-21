#!/usr/bin/python



# Begin variables.py
import os
from datetime import date

USER            = os.getlogin()
APPLICATION_CMD = "hyprctl activeworkspace -j"
TAB_CMD         = "hyprctl clients -j"
TODAY           = str(date.today())
BASE_DIR        = f"/home/{USER}/.config/hypr/hyprmonitor"
POLLING_RATE    = 1         # in seconds
# End variables.py

# Begin utils.py
import subprocess

# fetch command output from shell
def execute_fetch(cmd):
    try:
        process = subprocess.run(cmd, capture_output=True, 
                                 text=True, shell=True, check=True)
        output = process.stdout.strip()
        return output
    except subprocess.CalledProcessError as e:
        # print(f"Error executing command: {cmd}")
        # print(f"Exit code: {e.returncode}")
        # print(f"Error output: {e.stderr.strip()}")
        return ""
    
def format_time(num):
    hrs = num//3600
    mins = ((num)//60)%60
    return [hrs, mins, str(hrs) + "h ", str(mins) + "m"]

# just monika
def execute(cmd):
    try:
        subprocess.run(cmd, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Command failed with exit code {e.returncode}")
# End utils.py

import sys
import json

print("[Module Reader Loaded]")

#################################################
#                  _       _     _              #
# __   ____ _ _ __(_) __ _| |__ | | ___  ___    #
# \ \ / / _` | '__| |/ _` | '_ \| |/ _ \/ __|   #
#  \ V / (_| | |  | | (_| | |_) | |  __/\__ \   #
#   \_/ \__,_|_|  |_|\__,_|_.__/|_|\___||___/   #
#################################################
args = sys.argv

#################################################
#   __                  _   _                   #
#  / _|_   _ _ __   ___| |_(_) ___  _ __  ___   #
# | |_| | | | '_ \ / __| __| |/ _ \| '_ \/ __|  #
# |  _| |_| | | | | (__| |_| | (_) | | | \__ \  #
# |_|  \__,_|_| |_|\___|\__|_|\___/|_| |_|___/  #
#################################################

def sep():
    cols = execute_fetch("tput cols")
    print("-"*int(cols))
    return cols

def application_search():
    if len(args) < 3:
        execute("hyprctl notify 2 4000 'rgb(b2d4fa)' 'Usage: reader.py -a application_name'")
        return
    
    app = args[2]
    mins = 0
    hrs = 0
    
    # base statistics table
    e = execute_fetch(f'python reader.py -l 1000| grep -i "{app}"')
    
    if e == "":
        execute(f"hyprctl notify 2 4000 'rgb(b2d4fa)' 'Application: [{app}] not found'")
        return

    sep()
    print(e)
    sep()
    
    # total time calculation bs
    lst = e.split('\n')
    for i in lst:
        time = i[-2:-10:-1].strip().split()
        mins += int(time[0][1:][::-1])
        hrs += int(time[1][1:][::-1])
    hrs += mins // 60
    mins = mins % 60
    
    print(f"\033[34;1mTotal Time: {hrs}h {mins}m\033[m")

def list_tabs():
    try:
        with open(f"{BASE_DIR}/apps.json", "r") as file:
            a = json.load(file)
        a = dict(sorted(a.items(), key = lambda item: item[1], reverse=True))
        cols = sep()
        try:
            number_of_results = int(args[2])
        except:
            number_of_results = len(a)
        counter = 0
        for i in a:
            counter += 1
            timer = format_time(a[i])[2::]
            if("0h 0m" in timer):
                continue
            else:
                print("|", i,end = "")
                print(" "*(int(cols)-len(i)-len(timer[0])-len(timer[1]) - 4), end = "")
                print(timer[0]+timer[1], "|")
            if(counter == number_of_results):
                break
        sep()
    except:
        execute("hyprctl notify 4 4000 'rgb(b2d4fa)' 'log file not found, try running monitor first'")

def date_search():
    if len(args) < 3:
        execute("hyprctl notify 2 4000 'rgb(b2d4fa)' 'Usage: reader.py -d YYYY-MM-DD'")
        return

    date = args[2]
    print(f"fetching records from {date}")
    print("Enter \n 1. to view window stats \n 2. to view all application stats: ", end = "")
    choice = int(input())
    if choice == 1:
        try:
            with open(f"{BASE_DIR}/all_{date}.json", "r") as file:
                print()
                cols = sep()
                a = json.load(file)
                a = dict(sorted(a.items(), key = lambda item: item[1], reverse=True))
                for i in a:
                    timer = str(a[i]//3600)+"h"+" "+ str((a[i]//60)%60)+"m"
                    print("|", i, end = "")
                    print(" "*(int(cols)-len(i)-len(timer) - 5), end = "")
                    print(timer, "|")
                sep()
        except:
            execute("hyprctl notify 2 4000 'rgb(b2d4fa)' 'log file not found, check your date, should be YYYY-MM-DD'")

    elif choice == 2:
        try:
            with open(f"{BASE_DIR}/apps_{date}.json", "r") as file:
                print()
                a = json.load(file)
                a = dict(sorted(a.items(), key = lambda item: item[1], reverse=True))
                cols = sep()
                for i in a:
                    timer = str(a[i]//3600)+"h" + " " + str((a[i]//60)%60)+"m"
                    if("0h 0m" in timer):
                        continue
                    else:
                        print("|", i,end = "")
                        print(" "*(int(cols)-len(i)-len(timer) - 5), end = "")
                        print(timer, "|")
                sep()
        except:
            execute("hyprctl notify 2 4000 'rgb(b2d4fa)' 'log file not found, check your date, should be YYYY-MM-DD'")
    else:
        print("bro what")

def default_args():
    try:
        with open(f"{BASE_DIR}/all.json", "r") as file:
            json_obj = json.load(file)
        json_obj = dict(sorted(json_obj.items(), key = lambda item: item[1], reverse=True))
        hrs = 0
        mins = 0


        cols = sep()
        for i in json_obj:
            time_lst = format_time(json_obj[i])
            hrs += time_lst[0]
            mins += time_lst[1]
            timer = time_lst[2]
            print("|", i, end = "")
            print(" "*(int(cols)-len(i)-len(timer) - 5), end = "")
            print(timer, "|")
        sep()

    except:
        execute("hyprctl notify 2 4000 'rgb(b2d4fa)' 'log file not found, try running monitor first'")


#####################################
#                     _             #
#  _ __ ___  __ _  __| | ___ _ __   #
# | '__/ _ \/ _` |/ _` |/ _ \ '__|  #
# | | |  __/ (_| | (_| |  __/ |     #
# |_|  \___|\__,_|\__,_|\___|_|     #
#####################################

if len(args) == 1:
    default_args()
elif args[1] == '-l':
    list_tabs()
elif args[1] == '-d':
    date_search()
else:
    application_search()