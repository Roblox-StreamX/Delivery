# StreamX #
import subprocess
import os 


print("------------------ StreamX Launcher Script 1.0------------------")
print("2023 StreamX Developers")


print("------------------------------------------------------------------------")
print("For help, run the \"help\" commmand")
request = input("Make your request:").lower()

if not request:
    print("Error: request was not specified!")
    exit("Exiting due to request not being specified.")
if request == "start":
    print("Starting StreamX... Please hold")
    subprocess.run(["sudo", "systemctl", "start", "streamx"])
    exit("Success!")
    
elif request == "restart":
    print("Restarting StreamX...")
    subprocess.run(["sudo", "systemctl", "restart", "streamx"])
    exit("Success!")
elif request == "stop":
    print("Stopping StreamX...")
    subprocess.run(["sudo", "systemctl", "stop", "streamx"])
    exit("Success!")
elif request == "status":
    subprocess.run(["systemctl", "status", "streamx"])
    exit()
elif request == "install":
    print("Installing StreamX... This will take a while.")
    subprocess.run("python3 -m pip install -r requirements.txt")
    exit("Success! Run the script again and run \"start\" to start StreamX.")
elif request == "help":
    print("""
    StreamX Launcher Script

    Pretty basic but gets the job done.

    -- start: Starts StreamX
    -- stop: Stops StreamX
    -- restart: Restarts StreamX
    -- status: gives the status of StreamX.
    -- install: Installs StreamX. WARNING: Do NOT run this after the first time.

    
    """.split("\n"))
    exit()
else:
    exit("Request not found! Run \"help\" for more commands.")