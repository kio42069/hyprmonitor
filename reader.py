from variables import *
from utils import *
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

def application_search():
    hrs = 0
    cols = execute_fetch("tput cols")
    print("-"*int(cols))
    e = execute_fetch(f'py reader -l 1000| grep -i "{args[2]}"')
    print(e)
    print("-"*int(cols))
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
        cols = execute_fetch("tput cols")
        print("-"*int(cols))
        flag = False
        try:
            number_of_results = int(args[2])
        except:
            number_of_results = len(a)
        counter = 0
        for i in a:
            counter += 1
            timer = format_time(a[i])[2]
            if("0h 0m" in timer):
                continue
            else:
                print("|", i,end = "")
                print(" "*(int(cols)-len(i)-len(timer) - 5), end = "")
                print(timer, "|")
            if(counter == number_of_results):
                break
        print("-"*int(cols))
    except:
        execute("notify-send 'log file not found, try running monitor first'")

def date_search():
    date = args[2]
    print(f"fetching records from {date}")
    print("Enter \n 1. to view window stats \n 2. to view all application stats: ", end = "")
    choice = int(input())
    if choice == 1:
        try:
            with open(f"{BASE_DIR}/all_{date}.json", "r") as file:
                print()
                cols = execute_fetch("tput cols")
                print("-"*int(cols))
                a = json.load(file)
                a = dict(sorted(a.items(), key = lambda item: item[1], reverse=True))
                for i in a:
                    timer = str(a[i]//3600)+"h"+" "+ str((a[i]//60)%60)+"m"
                    print("|", i, end = "")
                    print(" "*(int(cols)-len(i)-len(timer) - 5), end = "")
                    print(timer, "|")
                print("-"*int(cols))
        except:
            execute("notify-send 'log file not found, check your date, should be YYYY-MM-DD'")

    elif choice == 2:
        try:
            with open(f"{BASE_DIR}/apps_{date}.json", "r") as file:
                print()
                a = json.load(file)
                a = dict(sorted(a.items(), key = lambda item: item[1], reverse=True))
                cols = execute("tput cols")
                print("-"*int(cols))
                flag = False
                for i in a:
                    timer = str(a[i]//3600)+"h" + " " + str((a[i]//60)%60)+"m"
                    if("0h 0m" in timer):
                        continue
                    else:
                        print("|", i,end = "")
                        print(" "*(int(cols)-len(i)-len(timer) - 5), end = "")
                        print(timer, "|")
                print("-"*int(cols))
        except:
            execute("notify-send 'log file not found, check your date, should be YYYY-MM-DD'")
    else:
        print("bro what")

def default_args():
    try:
        with open(f"{BASE_DIR}/all.json", "r") as file:
            a = json.load(file)
        print()
        cols = execute_fetch("tput cols")
        print("-"*int(cols))
        a = dict(sorted(a.items(), key = lambda item: item[1], reverse=True))
        hrs = 0
        mins = 0
        for i in a:
            time_lst = format_time(a[i])
            hrs += time_lst[0]
            mins += time_lst[1]
            timer = time_lst[2]
            print("|", i, end = "")
            print(" "*(int(cols)-len(i)-len(timer) - 5), end = "")
            print(timer, "|")
        
        print("-"*int(cols))
    except:
        execute("notify-send 'log file not found, try running monitor first'")


#####################################
#                     _             #
#  _ __ ___  __ _  __| | ___ _ __   #
# | '__/ _ \/ _` |/ _` |/ _ \ '__|  #
# | | |  __/ (_| | (_| |  __/ |     #
# |_|  \___|\__,_|\__,_|\___|_|     #
#####################################

print(args)
if len(args) == 1:
    default_args()
elif args[1] == '-l':
    list_tabs()
elif args[1] == '-d':
    date_search()
else:
    application_search()