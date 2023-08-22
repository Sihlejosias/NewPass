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
            self.conn = sqlite3.connect(f"/home/{self.users}/.config/db.db")
        elif platform == "win32":
            self.conn = sqlite3.connect("C:\Programs/.newpass/db.db")
        elif platform == "darwin":
            self.conn = sqlite3.connect("")
        else:
            print("Failed to create database!")

        self.cur = self.conn.cursor()

        self.key = self.cur.execute("SELECT key FROM encry_key").fetchone()[0]
    
    def getMasterPassw(self):
        passw = self.cur.execute("SELECT password FROM users WHERE username=?", (self.users,)).fetchone()
        
        return passw[0]

    def loadPass(self):
        site = input("Enter site name: ")
        username = input("Enter site username: ")
        email = input("Enter email: ")
        passwword = getpass("Enter site password: ")

        passwd = Fernet(self.key).encrypt(passwword.encode())

        self.cur.execute("INSERT INTO passwords VALUES (?, ?, ?, ?)", (site, username, email, passwd))

    def viewPass(self):
        site = input("Enter site name: ")

        password = self.cur.execute('SELECT password FROM passwords WHERE site=(?)', (site,)).fetchone()[0]
        passwrd = Fernet(self.key).decrypt(password).decode()

        print(passwrd)


    def closeCommit(self):
        self.conn.commit()
        self.conn.close()

if __name__ == "__main__":
    run = passwordManager()
    print("1. Get password\t", "2. Load new password\t", "3. Generate new password\n", "4. Get username\t", "5. Get email address")
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
        raise NotImplementedError("Code not correctly implemented!")

    run.closeCommit()