#!/usr/bin/env python

import os
from pw import PasswordManager

run = PasswordManager()

print("1. Get password\t", "2. Load new password\t", "3. Generate new password") 
print("4. Get username\t", "5. Get email address\t", "6. Delete Password")
print("7. Edit password\n")

menu = int(input("Enter option: "))

user = os.getlogin()

def call(val):
    password = run.PassHash() 
    if password == run.getmasterpassw():
        val()
    else:
        print(f"Incorrect password for {user}")

match menu:
    case 1:
        call(run.viewpass)
    case 2:
        call(run.loadpass)
    case 3:
        call(run.generatepass)
    case 4:
        call(run.getusername)
    case 5:
        call(run.getemail)
    case 6:
        call(run.deleteps)
    case 7:
        call(run.editentry)
    case _:
        raise NotImplementedError("Invalid option selected, Please choose between 1 - 7")

run.closecommit()