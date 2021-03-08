from mechanics import Utilities, system, sleep, CRUD

# Password Manager supporting basic CRUD


class Main():
    def __init__(self, pwords):
        self.pwords = pwords
        self.crud = CRUD(self.pwords)

    def menu(self):
        sleep(2)
        system("CLS")
        prompt = "How may I help you today?\n1)Generate a new password\n2)Add a new Password\n3)View a Password\n4)Update a Password\n5)Delete a Password\n6)Exit the program\n"
        response = Utilities.verifyResponse(prompt, [1,2,3,4,5,6])
        if response == 1: self.crud.generate()
        elif response == 2: self.crud.create()
        elif response == 3: self.crud.read()
        elif response == 4: self.crud.update()
        elif response == 5: self.crud.delete()
        elif response == 6: raise SystemExit

pwords = Utilities.setup()
    
main = Main(pwords)

while True:
    try:
        main.menu()
    except KeyboardInterrupt:
        print("Returning to main menu")