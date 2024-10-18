import subprocess


def runCommand(comm):
    try:
        subprocess.run(comm, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(e)
        print("Error running command: " + comm)
        exit(1)
    
def pushToPhone(toLocation):
    # Push all files in the current directory to the phone
    runCommand(f"adb push . {toLocation}")
    print("Files pushed to phone")

def connect(ip):
    runCommand(f"adb connect {ip}:5555")
    runCommand("adb devices")

pushToPhone(r'/storage/emulated/0/audiobooks/"HPMoR new"')