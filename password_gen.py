import string
from random import choice

class PasswordGenerator:
    def __init__(self) -> None:
        self.all_chars = []
        self.setup()

    def setup(self):
        for i in range(10):
            self.all_chars.append(str(i))

        for i in list(string.ascii_letters):
            self.all_chars.append(i)


    def main(self):
        print("Ah... so you wish to create a new password... How long do you want your password to be?")
        while True:
            try:
                length = int(input(": "))
                break
            except ValueError:
                print("Not a number my user.")

        print(f"Creating a password of length {length}")
        password = self.create(length)
        self.show_password(password)

    def create(self, length):
        password = []
        for i in range(length):
            password.append(choice(self.all_chars))

        return password

    def show_password(self, password):
        print("Now listen closely... your password is...")
        print(''.join(password))
        print("\nPress enter to continue: ")
    