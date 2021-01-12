from mechanics import Utilities

# Password Manager supporting basic CRUD


class Main():
    def __init__(self, pwords):
        self.pwords = pwords

    def menu(self):
        system("CLS")
        prompt = "How may I help you today?\n1)Add a new Password\n2)View a Password\n3)Update a Password\4)Delete a Password\n5)Exit the program\n"
        response = Utilities.verifyResponse(prompt, [1,2,3,4,5])
        if response == 1: Utilities.create(self.pwords)

pwords = Utilities.setup()
    
main = Main(pwords)

while True:
    main.menu()