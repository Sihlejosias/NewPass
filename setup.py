#import the cryptography module here
from sys import platform
from cryptography.fernet import Fernet
from getpass import getpass
import os
import hashlib
import sqlite3

class setup:
    def __init__(self):
        self.users = os.getlogin() 
        self.key  = None
        self.master_password1 = hashlib.sha256(getpass("Create master password: ").encode("utf-8")).hexdigest()   
        self.master_password2 = hashlib.sha256(getpass("Confirm master password: ").encode("utf-8")).hexdigest()

        if platform == "linux":
            # self.conn = sqlite3.connect(f"/home/{self.users}/.config/passwordM.db")
            self.conn = sqlite3.connect(":memory:")
        elif platform == "win32":
            self.conn = sqlite3.connect(f"C:\Programs/.passwordM.db")
        elif platform == "darwin":
            self.conn = sqlite3.connect(f"")
        else:
            print("Failed to create database!")

    def db(self):

        self.cur = self.conn.cursor()

        self.cur.execute("""CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username VARCHAR(255) NOT NULL, password VARCHAR(255) NOT NULL)""")
 
        self.cur.execute("""CREATE TABLE IF NOT EXISTS encry_key (key VARCHAR(255) NOT NULL)""")
 
        self.cur.execute(""" CREATE TABLE IF NOT EXISTS passwords (id INTEGER PRIMARY KEY, site VARCHAR(255) NOT NULL, username VARCHAR(255) NOT NULL, email VARCHAR(255) NOT NULL, password VARCHAR(255) NOT NULL)""")

        self.conn.commit()

    def createMaster(self):
        if self.master_password1 != self.master_password2:
            print("Master password entered doesn't match! Please try again........")
        else:
            self.cur.execute(f'INSERT INTO   users VALUES (1 ,"{self.users}", "{self.master_password1}")')
        
            

    def keySetup(self):
        self.cur.execute(f"SELECT key FROM encry_key")
        test = self.cur.fetchone()
        print(test[0])
        self.conn.close()

if __name__ == "__main__":
    run = setup()
    run.db()
    run.createMaster()
    run.keySetup()