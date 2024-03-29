# StreamX #
import subprocess
import os


print("------------------ StreamX Launcher Script 1.0 ------------------")
print("2023 StreamX Developers")


print("-----------------------------------------------------------------")
print("For help, run the \"help\" commmand")


def start():
    print("Starting StreamX... Please hold")
    subprocess.run(["sudo", "systemctl", "start", "streamx"])
    exit("Success!")


def restart():
    print("Restarting StreamX...")
    subprocess.run(["sudo", "systemctl", "restart", "streamx"])
    exit("Success!")


def stop():
    print("Stopping StreamX...")
    subprocess.run(["sudo", "systemctl", "stop", "streamx"])
    exit("Success!")


def status():
    subprocess.run(["systemctl", "status", "streamx"])
    exit()


def install():
    print("Installing StreamX... This will take a while.")
    subprocess.run(["python3", "-m", "pip", "install", "-r", "requirements.txt"])
    print("Successfully installed all packages!\nAttempting to start StreamX...")
    start()
    exit("Complete.")


def _help():
    print("".join([n.lstrip() + "\n" for n in """
    StreamX Launcher Script

    Pretty basic but gets the job done.

    -- start: Starts StreamX
    -- stop: Stops StreamX
    -- restart: Restarts StreamX
    -- status: gives the status of StreamX.
    -- install: Installs StreamX packages. WARNING: Do NOT run this after the first time.""".split("\n")]))
    

###################


cmds = {
    "start": start,
    "stop": stop,
    "restart": restart,
    "install": install,
    "help": _help,
    "status": status
}
while True:
    x = input("launcher/>")
    if x not in cmds:
        print("Invalid command! Run \"help\" to get a list of commands.")
        
    try:
         cmds[x]()
    except:
        print(f"Something went wrong running {x}. This could be an installation error.\nTo reinstall the packages, run the install command.")
