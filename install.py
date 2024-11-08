# installer

import subprocess
import sys

# Configuration
required_modules = ["easygui", "requests"]

# Functions
def Quit(Message: str = "The program will now exit."):
    print(Message)
    input("\nPress ENTER/RETURN to exit.")
    sys.exit(0)

def ModuleInstall(Name: str):
    Result = None

    try:
        Result = subprocess.run(['cmd', '/c', f'pip install {Name}'], shell=True, capture_output=True, text=True)
    except Exception as e:
        return False, e
    else:
        if Result.returncode == 0:
            return True, 1
        else:
            return False, Result.stderr

def IsModuleInstalled(Name):
    return_code = None
    module = None
    
    try:
        module = __import__(Name)
    except ImportError as e:
        return False, e
    else:
        module = None
        return True, 1
        
# Checks

## PIP
print("Checking if PIP is installed...")
pip_installed = True
Result = -1
try:
    Result = subprocess.run(['cmd', '/c', f'pip'], shell=True, capture_output=True, text=True)
except FileNotFoundError as e:
    pip_installed = False
finally:
    if Result.returncode != 0:
        pip_installed = False


if pip_installed == False:
    Quit("PIP is not installed! Please install PIP and then continue.\nSee: https://www.geeksforgeeks.org/how-to-install-pip-on-windows/")
else:
    print(f"    | PIP is installed.\n")

# Module Dependencies
print("The required modules will now be checked, and installed if not present.")
for name in required_modules:
    print(f"Checking dependency '{name}'...")
    installed, msg = IsModuleInstalled(name)
    if installed:
        print(f"    | Dependency '{name}' is installed.")
    else:
        print(f"    | Dependency '{name}' is not installed!")
        print(f"    | Installing '{name}'...")
        Success, Result = ModuleInstall(name)

        if Success == True:
            print(f"    | Dependency '{name}' was installed.")
        else:
            print(f"    | [!] Dependency '{name}' failed to install!\n\n")
            print(Result)


print("\n\nThe required dependencies are installed. You may exit the installer and use the program.")
Quit()



















