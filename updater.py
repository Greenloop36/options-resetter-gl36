# updater

# Configuration
BaseURL = "https://raw.githubusercontent.com/Greenloop36/options-resetter-gl36/master/"
ToInstall = ["program.py", "install.py"]

# Modules
import requests
import os
import sys

# Variables
Installed = {}

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
    
    input("\nThe program will now exit. Press ENTER/RETURN to leave.")

    sys.exit(0)

# Runtime
## install confirmation
if not YesNo(f"Installing in directory {os.path}"):
    Quit("User cancelled installation.")

## install files

print("\nOptions resetter will now be updated to the latest available version.\n\n")
print("Download files...")
for File in ToInstall:
    print(f"Downloading {File}...")
    Success, Result = Install(File)

