#Import Tkinter here
import hashlib
from getpass import getpass 
import os
from pw import passwordManager

class PMGUI:
    def __init__(none):
        print("1. Get password\t", "2. Load new password: ")
        menu = int(input("Enter option: "))

        if menu == 1:
            password = hashlib.sha256(getpass(f"Password for {os.getlogin()}: ").encode("utf-8")).hexdigest()

            if password == passwordManager.getMasterPassw(none):
                passwordManager.viewPass()
            else: 
                print(f"Incorrect password for {os.getlogin()}")

        elif menu == 2:
            password = hashlib.sha256(getpass(f"Password for {os.getlogin()}: ").encode("utf-8")).hexdigest()

            if password == passwordManager.getMasterPassw():
                passwordManager.loadPass()
            else: 
                print(f"Incorrect password for {os.getlogin()}")
            
        else:
            print("Invalid option!")

if __name__ == "__main__":
    run = PMGUI()