from utils import *
from variables import *

import time
import json
from datetime import date

print("[Module Monitor Loaded]")

#################################################
#                  _       _     _              #
# __   ____ _ _ __(_) __ _| |__ | | ___  ___    #
# \ \ / / _` | '__| |/ _` | '_ \| |/ _ \/ __|   #
#  \ V / (_| | |  | | (_| | |_) | |  __/\__ \   #
#   \_/ \__,_|_|  |_|\__,_|_.__/|_|\___||___/   #
#################################################
APPLICATIONS_DICT   = dict()
TABS_DICT           = dict()


#################################################
#   __                  _   _                   #
#  / _|_   _ _ __   ___| |_(_) ___  _ __  ___   #
# | |_| | | | '_ \ / __| __| |/ _ \| '_ \/ __|  #
# |  _| |_| | | | | (__| |_| | (_) | | | \__ \  #
# |_|  \__,_|_| |_|\___|\__|_|\___/|_| |_|___/  #
#################################################

# creates directories if missing on initial install
# additionally if script is killed mid-day, will reset vars with existing data
def start():
    if not os.path.exists(f"{BASE_DIR}/"):
        execute(f"mkdir -p {BASE_DIR}/")
    if os.path.exists(f"{BASE_DIR}/applications.json"):
        # complete json parsing code
        pass
    if os.path.exists(f"{BASE_DIR}/tabs.json"):
        #complete this too
        pass

def copy_old_logs(argdate):
    global APPLICATIONS_DICT, TABS_DICT
    APPLICATIONS_DICT = {}
    TABS_DICT = {}
    execute(f"cp {BASE_DIR}/all {BASE_DIR}/all_{argdate}.json")
    execute(f"cp {BASE_DIR}/apps {BASE_DIR}/apps_{argdate}.json")
    execute(f"rm {BASE_DIR}/all {BASE_DIR}/apps.json")
    subprocess.Popen(['notify-send', "Logs Copied!"])

def init(today):
    try:
        flag = True
        with open (f"{BASE_DIR}/date", "r") as f:
            file_date = f.readlines()[0].strip()
            if file_date != today:
                flag = False
                copy_old_logs(file_date)
        if not flag:
            flag = not flag
            with open(f"{BASE_DIR}/date", "w") as f:
                f.write(today+'\n')
    except:
        with open(f"{BASE_DIR}/date", "w") as f:
            f.write(today+'/n')

def loop():
    try:
        time.sleep(POLLING_RATE)
        output_string = execute_fetch(APPLICATION_CMD)
        workspace = json.loads(output_string)['id']
        output_string = execute_fetch(TAB_CMD)
        windows = json.loads(output_string)
        repeaters = {}
        for window_iterator in windows:
            if window_iterator["workspace"]["id"] == workspace:
                subwindow = window_iterator['title']
                window = window_iterator['class']
                if subwindow not in TABS_DICT:
                    TABS_DICT[subwindow] = 1
                else:
                    TABS_DICT[subwindow] += 1
                if window not in APPLICATIONS_DICT:
                    APPLICATIONS_DICT[window] = 1
                    repeaters[window] = 1
                else:
                    if window not in repeaters:
                        repeaters[window] = 1
                        APPLICATIONS_DICT[window] += 1
            else:
                # code for special workspaces
                # hyprctl activeworkspace is a lil bitch 
                news = execute_fetch("hyprctl activewindow -j")
                news = json.loads(news)
                if news['workspace']['id'] < 0:
                    subwindow = news['title']
                    window = news['class']
                    if subwindow not in TABS_DICT:
                        TABS_DICT[subwindow] = 1
                    else:
                        TABS_DICT[subwindow] += 1
                    if window not in APPLICATIONS_DICT:
                        APPLICATIONS_DICT[window] = 1
                    else:
                        APPLICATIONS_DICT[window] += 1
                
            with open(f"{BASE_DIR}/all.json", "w") as f:
                dumper_obj = json.dumps(TABS_DICT, indent=4);
                f.write(dumper_obj)
            with open(f"{BASE_DIR}/apps.json", "w") as f:
                dumper_obj = json.dumps(APPLICATIONS_DICT, indent=4);
                f.write(dumper_obj)
    except KeyboardInterrupt:
        execute('hyprctl notify 5 2000 "rgb(b2d4fa)" "Ending monitor..."')
        return -1
    except:
        return -2


#############################################
#                        _ _                #
#  _ __ ___   ___  _ __ (_) |_ ___  _ __    #
# | '_ ` _ \ / _ \| '_ \| | __/ _ \| '__|   #
# | | | | | | (_) | | | | | || (_) | |      #
# |_| |_| |_|\___/|_| |_|_|\__\___/|_|      #
#############################################


print("Launching monitor")
execute("hyprctl notify 5 2000 'rgb(b2d4fa)' Launching monitor")
start()
while True:
    today = str(date.today())
    init(today=today)
    return_code = loop()
    if return_code == -1:
        break
    if return_code == -2:
        continue
