#!/usr/bin/env python

from sys import platform
from cryptography.fernet import Fernet
from getpass import getpass
from subprocess import run, PIPE
from setuptools import setup
import os
import hashlib
import sqlite3
import secrets
import random

class setup:
    def __init__(self):
        self.users = os.getlogin() 
        self.token = secrets.token_hex(random.randrange(8, 512))
        getPs1 = getpass("Create master password: ")
        getPs1 += self.token
        getPs2 = getpass("Confirm master password: ")
        getPs2 += self.token
        self.master_password1 = hashlib.sha512(getPs1.encode("utf-8")).hexdigest()   
        self.master_password2 = hashlib.sha512(getPs2.encode("utf-8")).hexdigest()
        self.key = None

        match platform:
            case "linux":
                folder = run(("mkdir", f"/home/{self.users}/.config/newpass"), stdout=PIPE, stderr=PIPE)
                if folder.returncode == 0:
                    self.conn = sqlite3.connect(f"/home/{self.users}/.config/newpass/passdb.db")
                    self.encr = sqlite3.connect(f"/home/{self.users}/.config/newpass/keys.db")
                else:
                    print(folder.stderr)
            case "win32":
                folder = run(("mkdir", "C:\Programes\.newpass"), stdout=PIPE, stderr=PIPE)
                if folder.returncode == 0:
                    self.conn = sqlite3.connect("C:\Programs/.newpass/passdb.db")
                    self.encr = sqlite3.connect("C:\Programs/.newpass/keys.db")
                else: 
                    print(folder.stderr)
            case "darwin":
                folder = run(("mkdir", f"/Users/{self.users}/.newpass"), stdout=PIPE, stderr=PIPE)
                if folder.returncode == 0:
                    self.conn = sqlite3.connect(f"/Users/{self.users}/.newpass/passdb.db")
                    self.encr = sqlite3.connect(f"/Users/{self.users}/.newpass/keys.db")
                else: 
                    print(folder.stderr)
            case _:
                print("Failed to create database!")

    def db(self):
        self.cur = self.conn.cursor()
        self.d = self.encr.cursor()
        self.cur.execute("""CREATE TABLE IF NOT EXISTS users (username text NOT NULL, password text NOT NULL)""")
        self.d.execute("""CREATE TABLE IF NOT EXISTS encry_key (key text NOT NULL)""")
        self.d.execute("""CREATE TABLE IF NOT EXISTS salt (token text NOT NULL)""")
        self.cur.execute(""" CREATE TABLE IF NOT EXISTS passwords (site text NOT NULL, username text NOT NULL, email text, password text NOT NULL)""")

    def createMaster(self):
        if self.master_password1 != self.master_password2:
            print("Master password entered doesn't match! Please try again........")
        else:
            self.cur.execute('INSERT INTO users VALUES (?, ?)', (self.users, self.master_password1))
            self.d.execute('INSERT INTO salt VALUES (?)', (self.token,))
        
    def keySetup(self):
        self.key = Fernet.generate_key()
        self.d.execute('INSERT INTO encry_key VALUES (?)', (self.key,))
    
    def closeCommit(self):
        self.conn.commit()
        self.encr.commit()
        self.conn.close()
        self.encr.close()
    
    def selfdelete():
        try:
            run(("rm", "setup.py"), stdin=PIPE, stderr=PIPE)
        except:
            print("Could not delete file!")

    def requirements():
        # This function still needs work and testing
        setup(
            name='newpass',
            long_description=open('README.md').read(),
            long_dedcription_content_type="text/markdown",
            install_requires=[
                'pyperclip',
                'cryptography',
            ],
        )
    
def call():
    run = setup()
    # run.requirements()
    run.db()
    run.createMaster()
    run.keySetup()
    run.closeCommit()
    print("Successfully Setup and ready!!")
    # run.selfdelete()

if __name__ == "__main__":
    call()