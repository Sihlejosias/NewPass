from cryptography.fernet import Fernet
from getpass import getpass
from sys import platform
import pyperclip
import sqlite3
import string
import secrets
import os

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

        getPassword = self.cur.execute('SELECT password FROM passwords WHERE site=(?)', (site,)).fetchone()[0]
        passwrd = Fernet(self.key).decrypt(getPassword).decode()

        pyperclip.copy(passwrd)

        print("Password temporary copied to clipboard!!")

    def generatePass(self):
        site = input("Website name: ")
        username = input("Username: ")
        email = input("Email address: ")
        lenth = input("How long: ")

        char = string.ascii_letters + string.digits + string.punctuation
        if lenth == '':
            genPass = "".join(secrets.choice(char) for i in range(8))
        else:
            lenth = int(lenth)
            genPass = "".join(secrets.choice(char) for i in range(lenth))

        pas = Fernet(self.key).encrypt(genPass.encode())
        self.cur.execute("INSERT INTO passwords VALUES (?, ?, ?, ?)", (site, username, email, pas))

        print(f"Generated password for website {site} with username {username} is {genPass}")

    def getUsername(self):
        site = input("Enter site name: ")

        getUser = self.cur.execute('SELECT username FROM passwords WHERE site=(?)', (site,)).fetchone()[0]

        print(f"Username for {site}: {getUser}")
    
    def getEmail(self):
        site = input("Enter site name: ")

        getmail = self.cur.execute('SELECT email FROM passwords WHERE site=(?)', (site,)).fetchone()[0]

        print(f"Username for {site}: {getmail}")

    def deletePs(self):
        site  = input("Enter site name: ")

        self.cur.execute("DELETE FROM passwords WHERE site=(?)", (site,)).fetchone()[0]

        print(f'User informtion for {site} have been deleted')

    def PassHash(self):
        password = getpass(f"Password for {os.getlogin()}: ").encode("utf-8")
        password = hashlib.sha256(password).hexdigest()
        
        return password

    def closeCommit(self):
        self.conn.commit()
        self.conn.close()

if __name__ == "__main__":
    run = passwordManager()
    print("1. Get password\t", "2. Load new password\t", "3. Generate new password\n", "4. Get username\t", "5. Get email address\t", "6. Delete Password")
    menu = int(input("Enter option: "))

    password = run.PassHash()

    if menu == 1:
        if password == run.getMasterPassw():
            run.viewPass()
        else: 
            print(f"Incorrect password for {os.getlogin()}")

    elif menu == 2:
        if password == run.getMasterPassw():
            run.loadPass()
        else: 
            print(f"Incorrect password for {os.getlogin()}")
    
    elif menu == 3:
        if password == run.getMasterPassw():
            run.generatePass()
        else: 
            print(f"Incorrect password for {os.getlogin()}")
    
    elif menu == 4:
        if password == run.getMasterPassw():
            run.getUsername()
        else: 
            print(f"Incorrect password for {os.getlogin()}")
    
    elif menu == 5:
        if password == run.getMasterPassw():
            run.getEmail()
        else:
            print(f"Incorrect password for {os.getlogin()}")
    
    elif menu == 6:
        if password == run.getMasterPassw():
            run.deletePs()
        else:
            print(f"Incorrect password for {os.getlogin()}")
    
    else:
        raise NotImplementedError("Code not correctly implemented!")

    run.closeCommit()