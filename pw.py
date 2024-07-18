#!/usr/bin/env python
from cryptography.fernet import Fernet
from getpass import getpass
from sys import platform, exit
from time import sleep
import pyperclip, random
import hashlib
import sqlite3
import string
import secrets
import os
from requests import get

class PasswordManager:
    def __init__(self) -> None:
        self.users = os.getlogin()

        match platform:
            case "linux":
                self.conn = sqlite3.connect(f"/home/{self.users}/.config/newpass/passdb.db")
                self.encr = sqlite3.connect(f"/home/{self.users}/.config/newpass/keys.db")
            case "win32":
                self.conn = sqlite3.connect("C:\Programs/.newpass/passdb.db")
                self.encr = sqlite3.connect("C:\Programs/.newpass/keys.db")
            case "darwin":
                self.conn = sqlite3.connect(f"/Users/{self.users}/.newpass/passdb.db")
                self.encr = sqlite3.connect(f"/Users/{self.users}/.newpass/keys.db")
            case _:
                print("Failed to connect to database!")

        self.cur = self.conn.cursor()
        self.d = self.encr.cursor()

        self.key = self.d.execute("SELECT key FROM encry_key").fetchone()[0]
        self.token = self.d.execute("SELECT token FROM encry_key").fetchone()[0]

    def getmasterpassw(self) -> str:
        passw = self.cur.execute("SELECT password FROM users WHERE username=?", (self.users,)).fetchone()
        
        return passw[0]

    def loadpass(self) -> None:
        site = input("Website name: ")
        username = input("Username: ")
        email = input("Email: ")
        password = getpass("Password: ")

        passwd = Fernet(self.key).encrypt(password.encode())

        self.cur.execute("INSERT INTO passwords VALUES (?, ?, ?, ?)", (site, username, email, passwd))

        print("Values inserted into database!")

    def viewpass(self) -> None:
        site = input("Website name: ")
        if site == "":
            print("Please enter website name!")
        else:
            getPassword = self.cur.execute('SELECT password FROM passwords WHERE site=(?)', (site,)).fetchone()[0]
            password = Fernet(self.key).decrypt(getPassword).decode()

            pyperclip.copy(password)
            print("Password temporary copied to clipboard! You have approcimatly 60 seconds to use it")
            sleep(60)
            pyperclip.copy(" ")
            print("Clipboard cleared.")

    def generatepass(self) -> None:
        site = input("Website name: ")
        username = input("Username: ")
        email = input("Email: ")
        length = int(input("How long: "))

        char = string.ascii_lowercase + string.ascii_uppercase + string.digits + string.punctuation        

        if length == '':
            length = 20 

        try:
            # length = int(length)
            if length < 12:
                raise ValueError("Password cannot be less than 12 characters in length.")
        except Exception:
            print("Invalid type. Please enter a value equal/greater to 12")
            exit()
            
        genPass = "".join(secrets.choice(char) for _ in range(length))

        print(f"Generated password for website {site} with username {username} is {genPass}")

        password = Fernet(self.key).encrypt(genPass.encode())
        self.cur.execute("INSERT INTO passwords VALUES (?, ?, ?, ?)", (site, username, email, password))

    def getusername(self) -> None:
        site = input("Website name: ")
        if site == "":
            print("Please enter website name!")
        else:
            getUser = self.cur.execute('SELECT username FROM passwords WHERE site=(?)', (site,)).fetchone()[0]

            print(f"Username for {site}: {getUser}")
    
    def getemail(self) -> None:
        site = input("Webite name: ")
        if site == "":
            print("Please enter website name!")
        else:
            getmail = self.cur.execute('SELECT email FROM passwords WHERE site=(?)', (site,)).fetchone()[0]

            print(f"Username for {site}: {getmail}")

    def deleteps(self) -> None:
        site  = input("Website name: ")
        if site  == "":
            print("PLease enter website name!")
        else:
            self.cur.execute("DELETE FROM passwords WHERE site=(?)", (site,)).fetchone()[0]

            print(f'User informtion for {site} have been deleted')

    def editentry(self) -> None:
        site = input("Website name: ")
        if site == "":
            print("Please enter website name!")
        else:
            username = input("Update username: ")
            if username == "":
                old = self.cur.execute("SELECT username FROM passwords WHERE site=(?)", (site,)).fetchone()[0]
                print(f"Username: {old} not changed!")
            else:
                self.cur.execute("UPDATE passwords SET username=(?) WHERE site=(?)", (username, site))
                print("Username Updated!")
            
            email = input("Update email: ")
            if email == "":
                old = self.cur.execute("SELECT email FROM passwords WHERE site=(?)", (site,)).fetchone()[0]
                print(f"Email Address: {old} not changed!")
            else:
                self.cur.execute("UPDATE passwords SET email=(?) WHERE site=(?)", (email, site))
                print("Email Address Updated!")
            
            password = getpass("Update passowrd: ")
            if password == "":
                print(f"Password not changed!")
            else:
                hashPas = Fernet(self.key).encrypt(password.encode())

                self.cur.execute("UPDATE passwords SET password=(?) WHERE site=(?)", (hashPas, site))
                print("Password Updated!")

    def passhash(self) -> str:
        
        password = getpass("Master Password: ")
        password += self.token
        password = hashlib.sha512(password.encode("utf-8")).hexdigest()
        
        return password

    def closecommit(self) -> None:
        self.conn.commit()
        self.encr.commit()
        self.conn.close()
        self.encr.close()

    def commoncheker(self, paswd: str) -> str:
        #This fucntion checks if a password have been found in any of the data leaked 
        # cridential stuffing attacks and other database on the darknet
        prefix = paswd[:5]
        suffix = paswd[5:]

        response = get(f"https://api.pwnedpassowrds.com/range/{prefix}")

        if response.status_code == 200:
            suffixes = (line.split(":") for line in response.text.splitlines())
            for suf, count in suffixes:
                if suf == suffixes:
                    return f"The password have been found {count} times in known breaches. It's not safe to use this password."
                else:
                    return "The password has not been found in known breaches"
        else:
            return "Failed to check Password. Try agian later."


if __name__ == "__main__":
    PasswordManager()