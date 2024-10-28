# options resetter

# variables
import easygui as gui
import sys
import os
import shutil
import requests

# Configuration
ThisVersion = "1.0"
VersionPaste = "https://pastebin.com/raw/ZSQieT8b"
CopyConfiguration = {
    "settings": {
        "Display": "Settings",
        "Path": "options.txt",
        "IsDirectory": False,
    },
    "shaderpacks": {
        "Display": "Shaderpacks (includes shader settings)",
        "Path": "shaderpacks",
        "IsDirectory": True,
    },
    "config": {
        "Display": "Configuration (for mods) [UNSTABLE!]",
        "Path": "config",
        "IsDirectory": True,
    },
    "screenshots": {
        "Display": "Screenshots",
        "Path": "screenshots",
        "IsDirectory": True,
    },
    "saves": {
        "Display": "My Worlds [UNSTABLE!]",
        "Path": "saves",
        "IsDirectory": True,
    },
    "mods": {
        "Display": "Mods",
        "Path": "mods",
        "IsDirectory": True,
    },
}

ErrorMessageIfNoSuccess = """
The program did not successfully execute. See the console log for more information.
This is likely due to an incorrect configuration. Please follow the steps thoroughly before executing the program.

Some directories have been created during this operation. Please take care in removing them.
No files should have been edited or removed.

If you encounter further issues, please contact me on Discord (@gl36).
"""

Greeting = """
Welcome to options resetter, a program created by greenloop36 cause kai is a lazy bitch.

You will be given two prompts to select a folder.
The FIRST prompt will be where the program COPIES the settings from,
The SECOND prompt will be where the program COPIES TO.

Please ensure you select the correct folder!

A video tutorial is present within this folder. Please watch it before continuing.

Actions made by this program CANNOT BE UNDONE! You should create backups of your modpacks if necessary.
"""

ProgramTitle = "Options Resetter (Release " + ThisVersion + ")"

# Variables
AvailableOptionsToCopy = []

# Functions
def CheckForUpdate():
    print("Checking for updates...")
    response = None
    try:
        response = requests.get(VersionPaste)
    except Exception as e:
        print("[!] Failed to check for updates!")
        print(e, "\n")
        gui.msgbox(title = ProgramTitle, msg = f"Failed to check for updates.\n\n({e})")
    else:
        if response.status_code == 200:
            if ThisVersion != response.text:
                print(f"An update is available. ({ThisVersion} -> {response.text})")
                gui.msgbox(title = ProgramTitle, msg = f"An update is available! ({ThisVersion} -> {response.text})\n\nRe-install the file from the Google Drive link.\nRemember to re-run 'install.py'!")
            else:
                print(f"This version, {ThisVersion}, is up to date.")
        else:
            gui.msgbox(title = ProgramTitle, msg = f"Failed to check for updates.\n\n(HTTP {response.status_code})")

def Quit(Message: str | None = None):
    print("Quitting with message\n",str(Message))
    if Message:
        gui.msgbox(title = ProgramTitle, msg = f"{Message}\n\nThe program will now exit.")

    sys.exit(0)

def QuitIfNone(Input: any = None, Message: str | None = None):
    if Input == None:
        Quit(Message)

# def copy_files(source_dir, target_dir):
#     print("function copy_files")
#     os.makedirs(target_dir, exist_ok=True)
    
#     # Iterate over all files in the source directory
#     for filename in os.listdir(source_dir):
#         source_file = os.path.join(source_dir, filename)
        
#         # Only copy files, not directories
#         if os.path.isfile(source_file):
#             print(f"\t| Copy {source_file}")
#             shutil.copy(source_file, target_dir)
#         else:
#             print(f"\t| Ignore {source_file} (is a directory)")

#     return True

def copy_all_contents(source_dir, target_dir) -> bool: ## no debugging messages as it may slow the program down
    print("function copy_all_contents")
    # Check if target directory exists; return False if it doesn't
    if not os.path.isdir(target_dir):
        ##print("\t| Target directory does not exist!")
        return False

    # Iterate over all items in the source directory
    for item in os.listdir(source_dir):
        source_item = os.path.join(source_dir, item)
        target_item = os.path.join(target_dir, item)

        # If item is a directory, copy it recursively
        if os.path.isdir(source_item):
            ##print(f"\t| Item {source_item} is a directory, copying it and its contents")
            # Ensure the subdirectory exists in the target
            os.makedirs(target_item, exist_ok=True)
            # Recursively copy the contents of the subdirectory
            copy_all_contents(source_item, target_item)
        else:
            # If item is a file, copy it
            shutil.copy2(source_item, target_item)

    return True  # Indicate success


# Init
print("initialising...")
CheckForUpdate()
for key, data in CopyConfiguration.items():
    AvailableOptionsToCopy.append(data["Display"])

# Runtime
print("\n$ runtime")

# introduction
gui.msgbox(title = ProgramTitle, msg = Greeting)

# get copy from dir
gui.msgbox(title = ProgramTitle, msg = "Please now select the source (to copy FROM) folder")
CopyFrom = gui.diropenbox(title = ProgramTitle)
QuitIfNone(CopyFrom, "No directory was specified!")
print("CopyFrom:", CopyFrom)

# get target dir
gui.msgbox(title = ProgramTitle, msg = "Please now select the target (to copy TO) folder")
Target = gui.diropenbox(title = ProgramTitle)
QuitIfNone(Target, "No directory was specified!")
print("Target:", Target)

# choose which settings to copy
Selection = gui.multchoicebox(msg = "Select options to copy", title = ProgramTitle, choices = AvailableOptionsToCopy)
QuitIfNone(Selection, "No options were selected.")

# display continue confirmation
formattedMessage = f"You are copying the settings from:\n   {CopyFrom}\n\nto:\n    {Target}\n\nThe following setting(s) will be copied:\n    "

print("\nSelection (list)")
for i in Selection:
    print("\t|", i)
    formattedMessage = formattedMessage + i + "\n    "

Continue = gui.buttonbox(title = ProgramTitle, msg = formattedMessage, choices = ["Cancel", "Continue"], cancel_choice = "Cancel", default_choice = "Continue")
if Continue != "Continue":
    Quit("Cancelled")

# copy the files
result = "The operation is now finished. Below are the results of the program.\n\n"
Successful = False

print("\n\n$ begin copying\n")
for key, data in CopyConfiguration.items():
    if data["Display"] in Selection != None:
        if data["IsDirectory"] == False:
            print(f"{key} is a file:")
            Read = None
            Write = None
            
            # Read the file
            try:
                print(f'\t| Opening (read) {CopyFrom + "\\" + data["Path"]}')
                Read = open(CopyFrom + "\\" + data["Path"], "r")
                
                print(f'\t| Opening (write) {Target + "\\" + data["Path"]}')
                Write = open(Target + "\\" + data["Path"], "w")
            except Exception as e:
                result = result + "" + key.upper() + ": FAIL! (FILE NOT FOUND)\n"
                print(f'\t| Opening of {data["Path"]} failed!')
                print(e,"\n")
                continue

            # Attempt to write
            try:
                print(f'\t| Writing to {Target + "\\" + data["Path"]}')
                Write.write(Read.read())

                print(f'\t| Closing files')
                Read.close()
                Write.close()
            except Exception as e:
                result = result + "" + key.upper() + ": FAIL! (WRITE ERROR)\n"
                print(f'\t| Writing of {data["Path"]} failed!')
                print(e,"\n")
            else:
                print(f'\t| Successfully completed operation for {key}\n')
                result = result + "" + key.upper() + ": OK\n"
                Successful = True
        
        else:
            print(f"{key} is a directory:")
            ##print(Target + "\\" + data["Path"])
            Success, Result = None, None
            try:
                Result = copy_all_contents(CopyFrom + "\\" + data["Path"], Target + "\\" + data["Path"])
            except Exception as e:
                Success = False
                Result = e
            else:
                Success = True

            if Success and Result == True:
                result = result + "" + key.upper() + ": OK\n"
                Successful = True
                print(f'\t| Successfully completed operation for {key}\n')
            else:
                result = result + "" + key.upper() + ": FAIL! (WRITE)\n"
                print(f'\t| Writing of directory {data["Path"]} failed!')
                print(Result, "\n")

if Successful:
    print("\nOperation completed with at least one successful file or directory")
    Quit(result)
else:
    print("\nOperation failed with no success.")
    Quit(ErrorMessageIfNoSuccess)
    

























