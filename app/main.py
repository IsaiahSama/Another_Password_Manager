#! python3
# The purpose of this program is to allow for an easy, official way for accessing the PWmanager API, and handling local versions as well.
# Application will use requests when dealing with online, and will otherwise store the data locally, supporting being uploaded after.
# API Documentation can be found https://github.com/IsaiahSama/LAPasswordManager

from mechanics import *
from pyinputplus import inputChoice, inputEmail, inputPassword
from os import system


def menu(mfunc:ManagerFunctions, online):
    """Function that accepts an instance of ManagerFunctions and online, and provides a menu interface for users.
    
    Arguments:
    Mfunc -> This is an instance of the ManagerFunctions class.

    online -> This is a bool. And decides whether to do only local, or online operations"""

    handler = TaskHandler(mfunc, online)
    while True:
        system("CLS")
        print("Press ctrl + c to exit at any time")

        # Gets the task to be done
        task = get_task(online)

        # Handles the task to be done
        handler.handle_task(task.lower(), online)  
        input("Press enter to continue:")      

def get_task(online:bool) -> str:
    """Function that prompts for user input, regarding what they want to do with their passwords, and returns the response.
    
    Arguments: Whether we are using the api or not"""
    
    options = ["Create", "View", "Update", "Delete"]
    if online:
        options.append("Sync")

    options.append("Help")
    options.append("Quit")
    prompt_options = '\n'.join(options)
    prompt = f"\nHow may I help you with your passwords today?\n{prompt_options}\n\n:"

    return inputChoice(options, prompt)

        
def main():
    email = inputEmail("What is your registered Look Another Password Manager email\n")
    password = inputPassword(prompt="What is your password for this email?\n")
    mfunc = ManagerFunctions(email, password)
    print("Attempting to activate account")
    online = True
    try:
        mfunc.activate_account()
    except FailedApiRequestException as err:
        mfunc.handle_bad_exception(loads(str(err)))
    # except Exception as err:
    #     online = False
    #     print("For now, we will just use our offline version.")

    input("Done. Press enter to continue")
    
    try:
        menu(mfunc, online)
    except KeyboardInterrupt:
        print("Thanks for using us. Press enter to exit")
        input()
    

main()