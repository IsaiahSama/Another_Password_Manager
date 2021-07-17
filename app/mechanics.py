from sqlite3.dbapi2 import Row
from errors import *
from requests import post, Response
from json import dumps, loads
from copy import copy
from os import chdir, path, mkdir, system
from typing import Union
from pyinputplus import inputChoice, inputStr, inputYesNo
from time import sleep
import sqlite3

# For generating passwords
from random import choices
from string import hexdigits

hex_characters = list(hexdigits)

BASE = "http://127.0.0.1:5000/api/v1/"

class Database:
    def __init__(self) -> None:
        self.db = self.connect()

    def setup(self):
        """Creates the table if it doesn't exist"""
        self.db.execute("""CREATE TABLE IF NOT EXISTS AccountTable(
            ACCOUNT_NAME TEXT PRIMARY KEY UNIQUE,
            PASSWORD TEXT NOT NULL);""")
        self.commit_and_close()
        return True

    def connect(self):
        """Connects to the database"""
        return sqlite3.connect("./passwords/lapm.sqlite3")

    def insert_or_replace(self, acc_name, acc_pass):
        """Inserts the account name and password into the database."""

        self.db.execute("INSERT OR REPLACE INTO AccountTable (ACCOUNT_NAME, PASSWORD) VALUES (?, ?)", (acc_name, acc_pass))

    def query_all_accounts(self):
        """Queries the database for all of the users accounts."""

        cursor = self.db.execute("SELECT * FROM AccountTable")
        rows = cursor.fetchall()
        return rows

    def query_account_by_name(self, acc_name:str) -> Row:
        """Queries the database and searches for an account by the given name. Returns the row"""

        cursor = self.db.execute("SELECT * FROM AccountTable WHERE (ACCOUNT_NAME) == ?", (acc_name, ))
        value = cursor.fetchone()
        return value

    
    def check_for_duplicate(self, acc_name:str) -> bool:
        """Queries the database to see if a given account_name already exists. 
        
        Returns True if True, otherwise False"""
        value = self.query_account_by_name(acc_name)
        if value:
            return True 
        return False

    def delete_entry_by_name(self, acc_name:str) -> None:
        """Queries the database for the account with the given name, and then deletes it."""

        self.db.execute("DELETE FROM AccountTable WHERE ACCOUNT_NAME == (?)", (acc_name, ))

    def commit_and_close(self):
        """Commits all changes and then closes the database"""
        self.db.commit()
        self.close()

    def close(self):
        """Closes the database connection"""
        self.db.close()
        return True

class ApiHandler:
    def __init__(self, email, password) -> None:
        self.email = email
        self.password = password
        self.auth = {"EMAIL": self.email, "PASSWORD": self.password}


    # Responsible for handling API Calls    
        
    def make_request(self, url, inner_dict:dict) -> Response:
        """Function that makes the request, and returns the response
        
        Arguments: 
        url -> The url to make the request to
        json -> The inner dict to be put in the root of LAPM
        """

        # Takes the inner dict and puts it in the outer value.

        print("Making the request")
        json = {"LAPM": inner_dict}
        print(dumps(json, indent=4))

        response = None

        try:
            response = post(url, json=json)
            response.raise_for_status()
        except Exception as err:
            print(f"Something went wrong with the request: {err}")

        return response

    def activate_account(self) -> bool:
        """This function is called in order to use API request.
        
        Returns a bool"""
        url = BASE + "activate/"

        response = self.make_request(url, {"AUTH": self.auth})

        print("Gathering information")
        data = self.get_inner_dict(response)
        print("Information has been gathered")
        # Checks if the response is good or not
        if self.check_for_success(data):
            if data["RESPONSE"] == "200 OK TRUE":
                return True
                
            print("Visit your email, and then enter the 7 character code received.")
            code = input(": ")

            if self.verify_account(code):
                return True
        return False

    def verify_account(self, code) -> bool:
        """Function that handles the second part of the Verification process.
        
        Arguments: 
        The code that was entered
        
        Returns -> bool"""

        auth = copy(self.auth)
        auth.update({"VERICODE": code})
        inner_dict = {
            "AUTH": auth
        } 

        url = BASE + "activate/"

        response = self.make_request(url, inner_dict)
        data = self.get_inner_dict(response)

        # Returns True if successful, False otherwise
        return self.check_for_success(data)

    # CRUD Routes

    def create_or_update(self, entries, overwrite:bool):
        """API Function which accepts entries, and a goes to the `store` route of the API, to add the entries to the database
        
        Arguments:
        Entries -> This is a list of dictionaries of entries
        
        overwrite -> Bool, This is True if will update Entries, False otherwise"""

        url = BASE + "passwords/store/"

        to_send = {
            "AUTH": self.auth,
            "STORE": entries,
            "OVERWRITE": overwrite
        }

        response = self.make_request(url, to_send)
        data_dict = self.get_inner_dict(response)
        return self.check_for_success(data_dict)

    def query_all_accounts(self):
        """API Function which queries the API using the get route for ALL accounts. Returns the list of dictionaries."""

        d_dict = self.query_user_account([])

        if self.check_for_success(d_dict, False):
            return d_dict["RESPONSE"]

    def query_user_account(self, name:list) -> Union[None, dict]:
        """API Function that Queries the API using the GET url, for a specific Acc_Name / Acc_Pass pair.
        
        Arguments: 
        name -> A list containg the name of the account to return
        
        Returns, None, or d_dict if being called with an empty list as name"""

        url = BASE + "passwords/get/"

        to_send = {
            "AUTH": self.auth,
            "GET": name,
            "IGNOREMISSING": False
        }

        if name:
            to_send["IGNOREMISSING"] = True
        
        response = self.make_request(url, to_send)
        d_dict = self.get_inner_dict(response)
        if not name:
            return d_dict
        
        return self.check_for_success(d_dict)
        

    def get_inner_dict(self, response) -> dict:
        """This gets the JSON data from the response object, and returns the inner dictionary.
        
        Arguments:
        response -> This is the response object as returned from the post request
        
        returns Dict"""

        data = response.json()
        return data["LAPM"]

    def check_for_success(self, data_dict, display=True) -> bool:
        """Checks to see if the response was Successful or not
        
        Arguments:
        Data_dict - This is the dictionary returned from response.json
        display -> Bool, Chooses whether to display good data or not.
        Returns bool, or raises FailedApiRequestException"""

        # If an error occurred, Raise 
        print("Checking for success...")
        if not data_dict["SUCCESS_OR_FAILURE"]["SUCCESS"]:
            # Uses a temporary variable x, to make accessing easier
            
            x = data_dict["SUCCESS_OR_FAILURE"]

            error_dict = {
                "ERROR": x["ERROR"],
                "MESSAGE": x["MESSAGE"],
                "EXTRA": x["EXTRA"]
            }

            raise FailedApiRequestException(dumps(error_dict))
        if display: self.display_good_data(data_dict)
        return True


    def display_good_data(self, good_dict:dict):
        """Function that accepts a succes dictionary, and displays the data to the user."""

        message = f"""Message: {good_dict['SUCCESS_OR_FAILURE']['MESSAGE']}\n"""
        resp = good_dict["RESPONSE"]
        if isinstance(resp, str):
            message += f"{resp}\n"
        elif isinstance(resp, dict):
            k, v = list(resp.items())[0]
            message += f"Account Name: {k} - Password: {v}\n"
        elif isinstance(resp, list):
            for pair in resp:
                k, v = list(pair.items())[0]
                message += f"Account Name: {k} - Password: {v}\n"
        else:
            message += f"{resp}\n"
        
        if good_dict.get("FAILED"):
            message += f"Those that failed: {', '.join(good_dict['FAILED'])}"
        
        self.pprint(message)

    def handle_bad_exception(self, error_dict:dict):
        """Responsible for displaying the information as is stated in the error dict
        
        Arguments: 
        error_dict, A dictionary of the errors"""

        print("An error has occurred")
        
        to_send = f"""Error name: {error_dict['ERROR']}\nCause: {error_dict['MESSAGE']}"""
        if extra := error_dict["EXTRA"]:
            to_send += f"\nExtra: {extra}"

        self.pprint(to_send)

    def pprint(self, message:str) -> None:
        """Function that accepts a string, and formats it nicely for display."""

        print("\n")
        print("-------------------------------")
        print(message)
        print("-------------------------------")
        print("\n")

    

class TaskHandler:
    def __init__(self, api:ApiHandler, online:bool) -> None:
        self.api = api
        self.online = online

    def handle_task(self, task:str, online:bool) -> None:
        """Function that takes a string task, and the boolean Online, and executes the function accordingly"""

        print("\n\n")
        system("CLS")

        local = LocalChanges()
        
        print(task.center(100, "="))
        if task in ["create", "update"]:
            entries = self.prompt_for_new_entries()
            update = False if task == "create" else True

            if online:
                self.api.create_or_update(entries, update)
            else:
                local.create_or_update_local(entries, update)

        elif task == "view":
            # use_server = False
            # if online:
            #     prompt = "What do you want to view from?\nServer\nLocal\n:"
            #     resp = inputChoice(["server", "local"], prompt)
            #     if resp == "server":
            #        use_server = True
            
            acc_dict = self.display_keys(online)
            if acc_dict:
                to_find = self.prompt_for_entry(acc_dict)
                if online:
                    self.api.query_user_account([to_find])
                else:
                    local.display_pair(acc_dict, to_find)

        elif task == "delete":
            acc_dict = self.display_keys(online)
            if acc_dict:
                to_find = self.prompt_for_entry(acc_dict, "delete")
                if not online:
                    local.remove_entry_by_name(to_find)
        elif task == "sync":
            pass 
        elif task == "help":
            self.provide_help()
        elif task == "quit":
            raise KeyboardInterrupt
        else:
            print("I'm not quite sure what you want me to do")
        
        print(f"End {task}".center(100, "="))
        if online:
            if task in ["delete", "create", "update"]:
            # Syncs
                pass
            pass
        sleep(2)

        print("\n\n")

    def prompt_for_new_entries(self) -> Union[list, dict]:
        """Function that is used to get the data for new entries to either create, or update. 
        
        Returns a list of dictionaries, containing account_name:password pairs"""

        entries = []
        try:
            while len(entries) < 20:
                system("CLS")
                print("Press ctrl + c to quit when you are done.")
                
                name = inputStr("What is the name of the account whose password you wish to store?\n:")
                if len(name) > 75:
                    print("That account name is too long.")
                    continue
                pword = input(f"What is the password for {name}? If you leave blank, we will generate one for you:\n")
                if len(pword) > 50:
                    print("That password is far too long. Should be no more than 50 characters")
                    continue

                if not pword: pword = generate_password()
                entries.append({name:pword})

        except KeyboardInterrupt:
            pass
        
        print("Okay. Preparing to save.")
        if not entries: print("But... There's nothing for me to save :(")
        return entries

    def display_keys(self, use_server:bool) -> dict:
        """Function used to display all account names to a user.
        
        Arguments:
        Use_server -> If True, will get the keys from the Server. If False, will get the keys from the local database
        
        Returns -> All valid dictionaries with acc_name/acc_pass pairs"""

        if use_server:
            acc_dicts = self.api.query_all_accounts() 
        
        else:
            db = Database()
            accounts = db.query_all_accounts()
            db.close()

            acc_dicts = [{account[0]:account[1]} for account in accounts]

        acc_dict = {}
        [acc_dict.update(inner_dict) for inner_dict in acc_dicts]

        if not acc_dict:
            print("You have no existing accounts. Create some first :)")
        else:
            print("Account Names".center(100, "="))
            print("\n".join(list(acc_dict.keys())))
            print("End of Names".center(100, "="))

        return acc_dict

    def prompt_for_entry(self, acc_dict:dict, mode:str="view") -> str:
        """Function that asks the user for the name of the account whose password they wish to view or Delete.
        
        Arguments: 
        Acc_dict -> This is a dictionary of all existing accounts 
        Mode -> This is a string literal of either view or delete
        Returns the response.
        """
        print("Press ctrl + c to exit")
        try:
            response = inputChoice(list(acc_dict.keys()), prompt=f"Select the name of the account you wish to {mode}. Do note that they are case sensitive:\n")
            return response
        except KeyboardInterrupt:
            print("Cancelling")
        return False

    def provide_help(self):
        """Function that displays help and about the system."""
        print("About: Look Another Password Manager provides a safe, easy to use place for you to store your passwords, both locally and online, for access by you anywhere")
        print("Showing Help".center(110, "="))
        print("Create -> This allows you to store one of your account - password pairs with us.")
        print("Update -> This allows you to update an account - password pair that you already have with us. You can also create new ones as you would with the Create option.")
        print("Delete -> This will remove an account - password pair of your choice from our memory")
        print("View -> This allows you to view any of your account - password pairs that you have saved with us.")
        print("Sync -> For changes made while offline, this will sync our servers and your local changes. To see sync, you have to be signed in.")
        print("Help -> Displays this help message :)")
        print("End of Help".center(110, "="))


# Stores changes locally within a sqlite3 file
class LocalChanges:
    def __init__(self) -> None:
        self.setup()

    def setup(self):
        if path.exists("./app"):
            chdir("./app")
        
        if path.exists("../main.py"):
            chdir("..")
        if not path.exists("./passwords"):
            print("Performing first time local setup")
            mkdir("passwords")
            print("Created passwords folder.")
        
        db = Database()
        db.setup()


    def create_or_update_local(self, entries:list, update:bool):
        """Function that accesses the database, to store the new entries within it. 
        
        Arguments:
        Entries -> A list of entries to be addded to the db
        mode -> A boolean. If True, goes ahead with an update in case of a duplicate, else, ignores it"""
        db = Database()
        print("Inserting these new cool stuff.")
        for entry in entries:
            acc_name, acc_pass = list(entry.items())[0]
            
            if db.check_for_duplicate(acc_name):
                if not update:
                    print(f"Skipping {acc_name} because we already have it saved, and this is not an update.")
                    continue
            if not update:
                print(f"Stored {acc_name}")
            else:
                print(f"Successfully updated {acc_name}")
            db.insert_or_replace(acc_name, acc_pass)
        db.commit_and_close()
        print("All done.")

    def display_pair(self, acc_dict:dict, to_find:str) -> None:
        """Function that indexes the acc_Dict with the to_find, and displays it"""

        value = acc_dict[to_find]
        print(f"Ok. The account name is `{to_find}`, and the password is `{value}`")

    def remove_entry_by_name(self, to_find:str) -> None:
        """Function that queries the database and deletes the specified entry.
        
        Then displays the name and password of the deleted entry"""
        db = Database()
        to_delete = db.query_account_by_name(to_find)
        name, pword = [to_delete[0], to_delete[1]]
        prompt = f"Are you sure that you wish to delete the account `{name}` with password `{pword}`? Yes/No?\n"
        confirm = inputYesNo(prompt)
        if confirm == "yes":
            db.delete_entry_by_name(to_find)
            print(f"Deleted the account named {name}")
        else:
            print("ABORT ABORT!!!")
        db.commit_and_close()

def generate_password():
    """Generates a 12 character long password for use as a generated password"""
    return ''.join(choices(hex_characters, k=12))