#!/usr/bin/env python
from subprocess import run, PIPE
from sys import platform, exit
from cryptography.fernet import Fernet
from getpass import getpass
import os
import hashlib
import sqlite3
import secrets
import random

class setup:
    def __init__(self) -> None:
        self.users = os.getlogin() 
        self.token = secrets.token_hex(random.randrange(8, 512))
        self.getPs1 = getpass("Create master password: ")
        self.getPs1 += self.token
        self.getPs2 = getpass("Confirm master password: ")
        self.getPs2 += self.token
        self.key = None

        if self.getPs1 != self.getPs2:
            print("Master password entered doesn't match! Please try again........")
            
            exit()
        else:
            self.master_password1 = hashlib.sha512(self.getPs2.encode("utf-8")).hexdigest()   

        def create_DB(base_path):
            try:
                os.makedirs(base_path, exist_ok=True)
                self.conn = sqlite3.connect(os.path.join(base_path, 'passdb.db'))
                self.encr = sqlite3.connect(os.path.join(base_path, 'keys.db'))
                return self.conn, self.encr
            except Exception as e:
                print(f'Failed to create directory or database: {e}')
                return None, None
        
        match platform:
            case "linux":
                base_path = f"/home/{self.users}/.config/newpass"
            case "win32":
                base_path = "C:\\Programs\\.newpass"
            case "darwin":
                base_path = f"/Users/{self.users}/.newpass"
            case _:
                print("Unsupported platform.")
                base_path = None

        if base_path:
            self.conn, self.encr = create_DB(base_path)
            if not self.conn or not self.encr:
                print("Database creation failed.") 

        self.d = self.encr.cursor()

    def db(self) -> None:
        try:
            self.cur = self.conn.cursor().execute("""CREATE TABLE IF NOT EXISTS users (username text NOT NULL, password text NOT NULL)""")
            self.d.execute("""CREATE TABLE IF NOT EXISTS encry_key (key text NOT NULL, token text NOT NULL)""")
            self.cur.execute("""CREATE TABLE IF NOT EXISTS passwords (site text NOT NULL, username text NOT NULL, email text, password text NOT NULL)""")
            self.cur.execute('INSERT INTO users VALUES (?, ?)', (self.users, self.master_password1))
        except sqlite3.Error as e:
            print(f"Failed to create tables and Inserting values: {e}")

    def keySetup(self) -> None:
        try:
            self.key = Fernet.generate_key()
        except:
            print("Could not generate key.")

        self.d.execute('INSERT INTO encry_key VALUES (?, ?)', (self.key, self.token))
        

    def closeCommit(self) -> None:
        try: 
            self.conn.commit()
            self.encr.commit()
            self.conn.close()
            self.encr.close()
        except:
            print("Could not commit and close to database.")
    
    def selfdelete(self) -> None:
        selfd = run(("rm", "setup.py"), stdout=PIPE, stderr=PIPE)
        if selfd.returncode == 0:
            print("Successcully deleted." + selfd.stdout)
        else:
            print(selfd.stderr)    

def main() -> None:
    sets = setup()
    sets.db()
    sets.keySetup()
    sets.closeCommit()
    print("Successfully Setup and ready!!")
    # sets.selfdelete()

if __name__ == "__main__":
    main()
    # getRequirments = run(("pip", "install", "-r", "requirements.txt"), stdout=PIPE, stderr=PIPE)
    # if getRequirments.returncode == 0: 
    #     makeExec = run(("chmod", "+x", "main.py"), stdout=PIPE, stderr=PIPE)
    #     if makeExec.returncode == 1:
    #         print(makeExec.stderr)
    #     else:
    #         main()  
    # else:
    #     print(getRequirments.stderr)
    #     print("It's ideal to run this script in a isolated environment. Create one by typing: \'python -m venv env\' and \'source env/bin/activte\'.")