# StreamX #
import subprocess
import os


print("------------------ StreamX Launcher Script 1.0------------------")
print("2023 StreamX Developers")


print("------------------------------------------------------------------------")
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
    subprocess.run("python3 -m pip install -r requirements.txt")
    exit("Success! Run the script again and run \"start\" to start StreamX.")


def _help():
    print("".join([n.lstrip() + "\n" for n in """
    StreamX Launcher Script

    Pretty basic but gets the job done.

    -- start: Starts StreamX
    -- stop: Stops StreamX
    -- restart: Restarts StreamX
    -- status: gives the status of StreamX.
    -- install: Installs StreamX. WARNING: Do NOT run this after the first time.""".split("\n")]))

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
    x = input("launcher/")
    if x not in cmds:
        print("Invalid command! Run \"help\" to get a list of commands.")

    cmds[x]()
