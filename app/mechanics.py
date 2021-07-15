from errors import *
from requests import post, Response
from json import dumps, loads

BASE = "https://lapasswordmanager.heroku.app.com/api/v1/"

class ApiFunctions:
    def __init__(self, email, password) -> None:
        self.email = email
        self.password = password
        self.auth = {"EMAIL": self.email, "PASSWORD": self.password}
        
    def activate_account(self) -> bool:
        """This function is called before every API request.
        
        Returns a bool"""
        url = BASE + "activate"

        response = self.make_request(url, {"AUTH": self.auth})

        data = self.get_inner_dict(response)
        
        # Checks if the response is good or not
        if self.check_for_success(data):
            print(data["SUCCESS_OR_FAILURE"]["MESSAGE"])
            if data["RESPONSE"] == "200 OK TRUE":
                print("You are already verified.")
                return True
                
            print("Visit your email, and then enter the 7 character code received.")
            code = input(": ")

            if self.verify_account(code):
                return True
            

    def make_request(url, inner_dict:dict) -> Response:
        """Function that makes the request, and returns the response
        
        Arguments: 
        url -> The url to make the request to
        json -> The inner dict to be put in the root of LAPM
        """

        # Takes the inner dict and puts it in the outer value.

        json = {"LAPM": {inner_dict}}


        try:
            response = post(url, json=json)
            response.raise_for_status()
        except Exception:
            raise BadStatusException

        return response
        

    def get_inner_dict(response) -> dict:
        """This gets the JSON data from the response object, and returns the inner dictionary.
        
        Arguments:
        response -> This is the response object as returned from the post request
        
        returns Dict"""

        data = response.json()
        return data["LAPM"]

    def check_for_success(data_dict) -> bool:
        """Checks to see if the response was Successful or not
        
        Arguments:
        Data_dict - This is the dictionary returned from response.json
        Returns bool, or raises FailedApiRequestException"""

        # If an error occurred, Raise 
        if not data_dict["SUCCESS_OR_FAILURE"]["SUCCESS"]:
            # Uses a temporary variable x, to make accessing easier
            
            x = data_dict["SUCCESS_OR_FAILURE"]

            error_dict = {
                "ERROR": x["ERROR"],
                "MESSAGE": x["MESSAGE"],
                "EXTRA": x["EXTRA"]
            }

            raise FailedApiRequestException(dumps(error_dict))
        return True

    def verify_account(self, code) -> bool:
        """Function that handles the second part of the Verification process.
        
        Arguments: 
        The code that was entered
        
        Returns -> bool"""

        inner_dict = {
            "AUTH": self.auth.update({"VERICODE": code})
        } 

        response = self.make_request(inner_dict)
        data = self.get_inner_dict(response)

        # Returns True if successful, False otherwise
        return self.check_for_success(data)

    def handle_bad_exception(self, error_dict:dict):
        """Responsible for displaying the information as is stated in the error dict
        
        Arguments: 
        error_dict, A dictionary of the errors"""

        print("An error has occurred")
        
        to_send = f"""Error name: {error_dict['ERROR']}\nCause: {error_dict['MESSAGE']}"""
        if extra := error_dict["EXTRA"]:
            to_send += f"\n{extra}"

        print(to_send)
        print("Press Enter to continue")