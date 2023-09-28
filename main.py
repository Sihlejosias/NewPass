#Import Tkinter here
from getpass import getpass 
import os
from pw import passwordManager

run = passwordManager()

print("1. Get password\t", "2. Load new password\t", "3. Generate new password") 
print("4. Get username\t", "5. Get email address\t", "6. Delete Password")
print("7. Edit password\n")
menu = int(input("Enter option: "))

password = run.PassHash()
user = os.getlogin()

if menu == 1:
    if password == run.getMasterPassw():
        run.viewPass()
    else: 
        print(f"Incorrect password for {user}")

elif menu == 2:
    if password == run.getMasterPassw():
        run.loadPass()
    else: 
        print(f"Incorrect password for {user}")
    
elif menu == 3:
    if password == run.getMasterPassw():
        run.generatePass()
    else: 
        print(f"Incorrect password for {user}")
    
elif menu == 4:
    if password == run.getMasterPassw():
        run.getUsername()
    else: 
        print(f"Incorrect password for {user}")
    
elif menu == 5:
    if password == run.getMasterPassw():
        run.getEmail()
    else:
        print(f"Incorrect password for {user}")
    
elif menu == 6:
    if password == run.getMasterPassw():
        run.deletePs()
    else:
        print(f"Incorrect password for {user}")
elif menu == 7:
    if password == run.getMasterPassw():
        run.editEntry()
    else:
        print(f"Incorrect password for {user}")
else:
    raise NotImplementedError("Code not correctly implemented!")

run.closeCommit()