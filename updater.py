# updater

# Configuration
BaseURL = "https://raw.githubusercontent.com/Greenloop36/options-resetter-gl36/master/"
ToInstall = ["program.py", "install.py"]

# Modules
import requests
import os
import sys

# Variables
DownloadCache = {}

# Functions
def Install(FileName: str) -> tuple[bool, str | None]:
    Response = requests.get(BaseURL +  FileName)
    if Response.status_code == 200: # Success
        return True, Response.text
    else:
        print(Response)
        return False, f"HTTP {Response.status_code} ({Response.reason})"
    
def YesNo(prompt: str = None) -> bool:
    print(prompt,"(Y/n)")

    while True:
        selection: str = input("> ")
        selection = selection.lower()

        if selection == "y":
            return True
        elif selection == "n":
            return False

def Quit(Message: str | None):
    if Message:
        print(Message)
    
    DownloadCache = None
    input("\nThe program will now exit. Press ENTER/RETURN to leave.")

    sys.exit(0)

# Runtime
## install confirmation
if not YesNo(f"Installing in directory {__file__}"):
    Quit("User cancelled installation.")

## download files
print("\nOptions resetter will now be updated to the latest available version.\n\n")
print("Download files...")
for File in ToInstall:
    print(f"Downloading {File}...")
    Success, Result = Install(File)

    if Success:
        print(f"\t| {File} downloaded successfully.")
        DownloadCache[File] = Result
    else:
        print(f"\t| {File} failed to download! ({Result})")

print("\nDownloading of application files has completed successfully.")

## remove files
print("\n\nOld application files will now be removed. The following files will be deleted:")
for File in ToInstall:
    print(f"\t| {File}")

if YesNo("\nPlease confirm the deletion of the above files.") == False:
    Quit("User cancelled installation. (The removal of old files is required)")

print("\nOld files are now being removed.")
for File in ToInstall:
    print(f"\nDeleting {File}...")
    
    try:
        os.remove(File)
    except FileNotFoundError:
        print(f"\t| {File} does not exist, continuing")
    except PermissionError:
        print(f"\t| The application has insufficient permissions to delete this file!")
        Quit("Cannot remove old files due to insufficient permissions. Please attempt to run this script as administrator.")
    else:
        print(f"\t| {File} was removed")

## install files
print("\nOld application files have been removed.\n\nThe new files will now be installed.")

for Name, Content in DownloadCache.items():
    print(f"\nInstalling {Name}...")

    try:
        File = open(Name, "w")
        File.write(Content)
        File.close()
    except Exception as e:
        print(f"\t| {Name} failed to install!")
        print(f"\t| {e}")
        Quit("Failed to install files. Please try again.")
    else:
        print(f"\t| {Name} was installed.")

## finish
Quit("\n\nThe update is now complete. Please remember to run the \"install.py\" file before usage.")