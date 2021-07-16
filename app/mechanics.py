from errors import *
from requests import post, Response
from json import dumps, loads
from copy import copy

BASE = "http://127.0.0.1:5000/api/v1/"

class ManagerFunctions:
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


    def get_inner_dict(self, response) -> dict:
        """This gets the JSON data from the response object, and returns the inner dictionary.
        
        Arguments:
        response -> This is the response object as returned from the post request
        
        returns Dict"""

        data = response.json()
        return data["LAPM"]

    def check_for_success(self, data_dict) -> bool:
        """Checks to see if the response was Successful or not
        
        Arguments:
        Data_dict - This is the dictionary returned from response.json
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
        self.display_good_data(data_dict)
        return True


    def display_good_data(self, good_dict:dict):
        """Function that accepts a succes dictionary, and displays the data to the user."""

        message = f"""Message: {good_dict['SUCCESS_OR_FAILURE']['MESSAGE']}\n"""
        resp = good_dict["RESPONSE"]
        if isinstance(resp, str):
            message += f"{resp}\n"
        elif isinstance(resp, dict):
            k, v = list(resp.items())
            message += f"Account Name: {k} : Password: {v}\n"
        elif isinstance(resp, list):
            for pair in resp:
                k, v = list(pair.items())
                message += f"Account Name: {k} : Password: {v}\n"
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
    def __init__(self, mfunc:ManagerFunctions, online:bool) -> None:
        self.mfunc = mfunc
        self.online = online

    def handle_task(self, task:str, online:bool) -> None:
        """Function that takes a string task, and the boolean Online, and executes the function accordingly"""

        print("\n\n")
        if task in ["create", "update"]:
            pass
        elif task == "delete":
            pass
        elif task == "view":
            pass 
        elif task == "sync":
            pass 
        elif task == "help":
            self.provide_help()

        print("\n\n")

    def provide_help(self):
        print("About: Look Another Password Manager provides a safe, easy to use place for you to store your passwords, both locally and online, for access by you anywhere")
        print("Showing Help".center(110, "="))
        print("Create -> This allows you to store one of your account - password pairs with us.")
        print("Update -> This allows you to update an account - password pair that you already have with us")
        print("Delete -> This will remove an account - password pair of your choice from our memory")
        print("View -> This allows you to view any of your account - password pairs that you have saved with us.")
        print("Sync -> For changes made while offline, this will send any updates that you made to sync with our servers.")
        print("Help -> Displays this help message :)")
        print("End of Help".center(110, "="))