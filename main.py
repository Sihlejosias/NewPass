#!/usr/bin/env python

import os
from pw import PasswordManager
import getopt, sys

run = PasswordManager()

user = os.getlogin()

def call(val) -> None:
    password = run.passhash() 
    if password == run.getmasterpassw():
        val()
    else:
        print(f"Incorrect password for {user}")

opts, args = getopt.getopt(sys.argv[1:], "lueEvgdmh")

for opt, arg in opts:
    match opt:
        case "-l":
            call(run.loadpass)
        case "-u": 
            call(run.getusername) 
        case "-e":
            call(run.getemail)
        case "-E":
            call(run.editentry)
        case "-v":
            call(run.viewpass)
        case "-g":
            call(run.generatepass)
        case "-d":
            call(run.deleteps)
        case "-h":
            raise NotImplementedError("Documentation not been properly implemented yet. ")
        case "-m":
            print("1. Get password\t", "2. Load new password\t", "3. Generate new password") 
            print("4. Get username\t", "5. Get email address\t", "6. Delete Password")
            print("7. Edit password\n")

            match int(input("Enter option(1 - 7): ")):
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
                    raise ValueError("Invalid option selected, please choose between 1 - 7!")
        case _: 
            print("Invalid option entered.")

run.closecommit()