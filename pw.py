from cryptography.fernet import Fernet
from getpass import getpass
from sys import platform
import pyperclip
import hashlib
import sqlite3
import string
import secrets
import os

class passwordManager:
    def __init__(self):
        self.users = os.getlogin()

        match platform:
            case "linux":
                self.conn = sqlite3.connect(f"/home/{self.users}/.config/passdb.db")
                self.encr = sqlite3.connect(f"/home/{self.users}/.config/keys.db")
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
        self.token = self.d.execute("SELECT token FROM salt").fetchone()[0]

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

        print("Values inserted into database!")

    def viewPass(self):
        site = input("Enter site name: ")
        if site == "":
            print("Please enter site name!")
        else:
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
        if site == "":
            print("Please enter site name!")
        else:
            getUser = self.cur.execute('SELECT username FROM passwords WHERE site=(?)', (site,)).fetchone()[0]

            print(f"Username for {site}: {getUser}")
    
    def getEmail(self):
        site = input("Enter site name: ")
        if site == "":
            print("Please enter site name!")
        else:
            getmail = self.cur.execute('SELECT email FROM passwords WHERE site=(?)', (site,)).fetchone()[0]

            print(f"Username for {site}: {getmail}")

    def deletePs(self):
        site  = input("Enter site name: ")
        if site  == "":
            print("PLease enter site name!")
        else:
            self.cur.execute("DELETE FROM passwords WHERE site=(?)", (site,)).fetchone()[0]

            print(f'User informtion for {site} have been deleted')

    def editEntry(self):
        site = input("Enter site name: ")
        if site == "":
            print("Please enter site name!")
        else:
            username = input("Update username: ")
            if username == "":
                old = self.cur.execute("SELECT username FROM passwords WHERE site=(?)", (site,)).fetchone()[0]
                print(f"Userneme: {old} not changed!")
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

    def PassHash(self):
        
        password = getpass("Master Password: ")
        password += self.token
        password = hashlib.sha512(password.encode("utf-8")).hexdigest()
        
        return password

    def closeCommit(self):
        self.conn.commit()
        self.encr.commit()
        self.conn.close()
        self.encr.close()

if __name__ == "__main__":
    passwordManager()