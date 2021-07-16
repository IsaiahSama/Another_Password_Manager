#! python3
# The purpose of this program is to allow for an easy, official way for accessing the PWmanager API, and handling local versions as well.
# Application will use requests when dealing with online, and will otherwise store the data locally, supporting being uploaded after.

from mechanics import *
from pyinputplus import inputChoice, inputEmail, inputPassword
from os import system

email = ""
password = ""

def menu():
    system("CLS")
    response = inputChoice(["Create", "Get", "Update", "Delete"], "What would you like to do today? Create, Update, Get or Delete a account-password entry?\n")
    api = ApiFunctions(email, password)
    try:
        api.activate_account()
    except FailedApiRequestException as err:
        api.handle_bad_exception(loads(str(err)))
        input("Press Enter to continue\n:")
        exit()

def main():
    global email, password
    email = inputEmail("What is your registered Look Another Password Manager email\n")
    password = inputPassword(prompt="What is your password for this email?\n")
    while True:
        menu()

main()