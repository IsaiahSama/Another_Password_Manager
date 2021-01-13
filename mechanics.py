from os import system, path, mkdir
from json import load, dump, JSONDecodeError
from time import sleep


class Utilities:
    
    @staticmethod
    def setup():
        if not path.exists("C:\\Password_Manager"): mkdir("C:\\Password_Manager")

        try:
            with open("C:\\Password_Manager\\mypw.json") as f:
                try:
                    data = load(f)
                except JSONDecodeError:
                    print("Something went wrong with your file")
                    data = {}

        except FileNotFoundError:
            data = {}
            
        sleep(1)
        return data

    @staticmethod
    def show_data(mydict):
        print("Oh ho? Below is a list of all of your accounts")
        print()
        for k in mydict.keys():
            print(k)
        print()
        print("What is the name of the account you wish to view? Press CTRL + C at any time to return to main menu")
        name = input(": ").capitalize()
        check = mydict.get(name, None)
        return name, check

    @staticmethod
    def create(mydict):
        try:
            print("So you wish to save a new password? Excellent. For what account will this password be for? Press CTRL + C at any time to quit")
            name = input(": ").capitalize()
            print(f"Noted. What is the password for {name}")
            password = input(": ")
            mydict[name] = password
            Utilities.save(mydict)
            print("Saved")
        except KeyboardInterrupt:
            print("Returning to main menu")

    @staticmethod
    def read(mydict):
        try:
            name, check = Utilities.show_data(mydict)

            if not check:
                print(f"Could not find an account for {name}")
                raise KeyboardInterrupt

            print(f"{name}: {mydict[name]}")
            input("press enter to proceed:")

        except KeyboardInterrupt:
            print("Returning to main menu")
            
    
    @staticmethod
    def update(mydict):
        try:
            name, check = Utilities.show_data(mydict)            
            if not check:
                print(f"Could not find an account for {name}")
                raise KeyboardInterrupt

            print(f"The current password for {name} is {mydict[name]}...")
            print("What would you like the new password to be?")
            new_password = input(": ")
            mydict[name] = new_password
            Utilities.save(mydict)
            print("Password has been updated successfully")

        except KeyboardInterrupt:
            print("Returning to main menu")

    @staticmethod
    def delete(mydict):
        try:
            name, check = Utilities.show_data(mydict)
            if not check:
                print(f"Could not find an account for {name}")
                raise KeyboardInterrupt

            prompt = f"Are you sure you wish to delete {name}?\n1)Yes\n2)No"
            answer = Utilities.verifyResponse(prompt, [1,2])
            if answer == 2: raise KeyboardInterrupt
            del mydict[name]
            print("Deleted")
            Utilities.save(mydict)

        except KeyboardInterrupt:
            print("Returning to main menu")
        
    @staticmethod
    def save(mydict):
        with open("C:\\Password_Manager\\mypw.json", "w") as f:
            dump(mydict, f, indent=4)
            

    @staticmethod
    def verifyResponse(prompt, numrange) -> int:
        while True:
            system("CLS")
            print(prompt)
            response = input(":")
            while not response.isnumeric():
                print("Your input is not a number")
                sleep(1)
                system("CLS")
                print(prompt)
                response = input(": ")
            
            if int(response) not in numrange:
                print(f"Your response must be in the range {numrange}")
                sleep(1)
                continue
            return int(response)