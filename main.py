from mechanics import Utilities, system

# Password Manager supporting basic CRUD


class Main():
    def __init__(self, pwords):
        self.pwords = pwords

    def menu(self):
        sleep(2)
        system("CLS")
        prompt = "How may I help you today?\n1)Add a new Password\n2)View a Password\n3)Update a Password\4)Delete a Password\n5)Exit the program\n"
        response = Utilities.verifyResponse(prompt, [1,2,3,4,5])
        if response == 1: Utilities.create(self.pwords)
        if response == 2: Utilities.read(self.pwords)
        if response == 3: Utilities.update(self.pwords)
        if response == 4: Utilities.delete(self.pwords)
        else: raise SystemExit

pwords = Utilities.setup()
    
main = Main(pwords)

while True:
    main.menu()