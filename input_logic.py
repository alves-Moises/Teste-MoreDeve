import interface

#validating input...
def get_int_input():
    valid = False
    while not valid:
        try:
            x = int(input(interface.menu()))
        except ValueError:
            print("Digite um valor inteiro")
        else: valid = True

    return x
