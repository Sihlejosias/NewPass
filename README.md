# Password Manager

Light offline password manager, written in python. Using SQLite database, encrypted and locked with a master password.

## How to use use?
        git clone https://github.com/Sihlejosias/Newpass.git
        cd Newpass 

#### For the first time use run
        python setup.py 

With setup.py you will be required to set up a master password and the initial set up. then it will run main.py automatically. 

#### Therefore, run to add, delete and modify 
        chmod +x main.py
        source venv/bin/activate
        ./main.py [options]

#### Avaliable options
        -m = Shows a menu options
        -l = Add new entry to database 
        -u = Get usernsme of a given website 
        -e = Get email of a given website 
        -E = Edit entry of a given website
        -v = Copies the password of the given website into a clipbourd for 60 seconds 
        -g = Randomly generate a strong password and store to database
        -d = Delete enrty from database  

# Features 
[x] Login  
[x] Database  
[x] Password Encrypter  
[x] Password Decrypter  
[x] Password Generator  
[x] copy password to clipboard  
[x] get username  
[x] get email  
[x] delete passwords  
[x] Edit password  
[x] Edit username  
[x] Edit Email  
[x] Main  
[ ] GUI (graphical user interface)  
[ ] autofil  

# Notes:

Disclaimer: This is a personal project. 