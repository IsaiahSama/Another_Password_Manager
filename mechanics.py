from os import system, path, mkdir
from json import load, dump, JSONDecodeError
from time import ctime, sleep



class Utilities:
    
    @staticmethod
    def setup():
        if not path.exists("C:\\Password_Manager"): mkdir("C:\\Password_Manager")

        try:
            with open("C:\\Passowrd_Manager\\mypw.json") as f:
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
    def create(mydict):
        pass

    @staticmethod
    def read(mydict):
        pass
    
    @staticmethod
    def update(mydict):
        pass

    @staticmethod
    def delete(mydict):
        pass
        
    @staticmethod
    def save(mydict):
        with open("C:\\Password_Manager\\mypw.json", "w") as f:
            dump(mydict, f, indent=4)
            

    @staticmethod
    def verifyResponse(prompt, numrange):
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