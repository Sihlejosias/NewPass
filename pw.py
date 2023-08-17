from cryptography.fernet import Fernet
import sqlite3
from sys import platform
import os
from getpass import getpass
import hashlib

class passwordManager:
    def __init__(self):
        self.users = os.getlogin()

        if platform == "linux":
            self.conn = sqlite3.connect(f"/home/{self.users}/.config/passwordM.db")
        elif platform == "win32":
            self.conn = sqlite3.connect("C:\Programs/.passwordM.db")
        elif platform == "darwin":
            self.conn = sqlite3.connect("")
        else:
            print("Failed to create database!")

        self.cur = self.conn.cursor()
    
    def getMasterPassw(self):
        passw = self.cur.execute("SELECT password FROM users WHERE username=?", (self.users,)).fetchone()
        
        return passw[0]

    def getKey(self):
        self.encryptKey = self.cur.execute("SELECT key FROM encry_key").fetchone()
        
        return self.encryptKey[0]
        
    def loadPass(self):
        #loads and encrypt password to database
        pass

    def viewPass(self):
        #fetch and decrypt password for database for viewing and copy
        pass

    def closeCommit(self):
        self.conn.close()

if __name__ == "__main__":
    run = passwordManager()
    print("1. Get password\t", "2. Load new password: ")
    menu = int(input("Enter option: "))

    if menu == 1:
        password = hashlib.sha256(getpass(f"Password for {os.getlogin()}: ").encode("utf-8")).hexdigest()

        if password == run.getMasterPassw():
            run.viewPass()
        else: 
            print(f"Incorrect password for {os.getlogin()}")

    elif menu == 2:
        password = hashlib.sha256(getpass(f"Password for {os.getlogin()}: ").encode("utf-8")).hexdigest()

        if password == run.getMasterPassw():
            run.loadPass()
        else: 
            print(f"Incorrect password for {os.getlogin()}")
         
    else:
        print("Invalid option!")

    run.closeCommit()