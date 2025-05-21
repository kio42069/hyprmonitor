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
        