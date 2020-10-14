import os
from os import system
from time import sleep

if not os.path.exists("./passwords"):
    os.mkdir("./passwords")
    with open("./passwords/Passwords.txt", "w") as f:
        print("Created your passwords file")

os.chdir("./passwords")


def save(x):
    to_save = []
    for k, v in x.items():
        to_save.append(f"{k}: {v}")
    with open("Passwords.txt", "w") as f:
        f.write("\n".join(to_save))

    print("Saved")
    sleep(1)
    system("CLS")


def request(x):
    if len(x) == 0: return 1
    while True:
        system("CLS")
        print("What would you like to do? Enter the number of the task you wish to do")
        print("1)Register a password\n2) Read a password\n3) Edit a password\n4)Delete a password\n5)Exit")
        try:
            to_do = int(input(": "))
        except ValueError:
            print("Invalid option")
            sleep(2)
            continue

        if to_do not in [1, 2, 3, 4, 5]: print("Invalid number"); sleep(2); continue
        return to_do

def register(x):
    while True:
        system("CLS")
        print("Register: ")
        while True:
            print("What is the account for which the password is for? Type Exit at any time to exit")
            account_name = input(": ")
            print(f"So you want to save a password with the name {account_name}? Yes or No?")
            response = input(": ")
            if response.lower().startswith("y"): break
            elif response.lower() == "exit": system("start core.py"); raise SystemExit
            else: sleep(1); continue
        while True:
            print(f"Ok. What is the password for {account_name}")
            password = input(": ")
            print(f"So the password for {account_name} is {password}")
            response = input(": ")
            if response.lower().startswith("y"): break
            elif response.lower() == "exit": system("start core.py"); raise SystemExit
            else: sleep(1); continue

        x[account_name] = password

        save(x)
        break

    sleep(1)
    system("CLS")

def read(x):
    system("CLS")
    print("Below is a list of all accounts. ")
    print(', '.join(x.keys()))
    print("Type the name of the one you want to view")
    answer = input(": ")
    try:
        to_send = x[answer]
        system("CLS")
        print(to_send)
        print("Press enter key to continue")
        input(": ")
    except KeyError:
        print("Could not find that account. Make sure your casing is correct")
        sleep(2)
        return

def editing(answer, to_edit):
    print(f"What is the new value you want for {answer}?")
    value = input(": ")
    print(f"Ok. The saved password for {answer} is now {value}")
    return value

def edit(x):
    system("CLS")
    print("Below is a list of all accounts. ")
    print(', '.join(x.keys()))
    print("Type the name of the one you want to edit")
    answer = input(": ")
    try:
        to_edit = x[answer]
        system("CLS")
        new_value = editing(answer, to_edit)
        x[answer] = new_value
        save(x)
        print("Press enter key to continue")
        input(": ")
    except KeyError:
        print("Could not find that account. Make sure your casing is correct")
        sleep(2)
        return

def delete(x):
    system("CLS")
    print("Below is a list of all accounts. ")
    print(', '.join(x.keys()))
    print("Type the name of the one you want to delete")
    answer = input(": ")
    try:
        del x[answer]
        system("CLS")
        print("Successfully deleted")
        save(x)
        print("Press enter key to continue")
        input(": ")
    except KeyError:
        print("Could not find that account. Make sure your casing is correct")
        sleep(2)
        return


def main():
    passwords = {}
    with open("Passwords.txt") as f:
        data = f.read()
        if len(data) > 0:
            split_data = data.split("\n")
            for line in split_data:
                new_line = line.split(": ")
                passwords[new_line[0]] = new_line[1]

    sleep(1)
    while True:
        todo = request(passwords)
        if todo == 1: register(passwords)
        elif todo == 2: read(passwords)
        elif todo == 3: edit(passwords)  
        elif todo == 4: delete(passwords) 
        else: raise SystemExit  

    
main()