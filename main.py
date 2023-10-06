import os
from pw import passwordManager

run = passwordManager()

print("1. Get password\t", "2. Load new password\t", "3. Generate new password") 
print("4. Get username\t", "5. Get email address\t", "6. Delete Password")
print("7. Edit password\n")

menu = int(input("Enter option: "))

password = run.PassHash()
user = os.getlogin()

def call(val):
    if password == run.getMasterPassw():
        val()
    else:
        print(f"Incorrect password for {user}")

match menu:
    case 1:
        call(run.viewPass)
    case 2:
        call(run.loadPass)
    case 3:
        call(run.generatePass)
    case 4:
        call(run.getUsername)
    case 5:
        call(run.getEmail)
    case 6:
        call(run.deletePs)
    case 7:
        call(run.editEntry)
    case _:
        raise NotImplementedError("Invalid option selected, Please choose between 1 - 7")

run.closeCommit()