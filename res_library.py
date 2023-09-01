#Place to store all extra functions required for the program.

def get_input(prompt, given_type, in_range):
    while True:
        value = input(prompt)
        if type(value) == given_type:
            pass
        elif given_type == int:
            try:
                value = int(value)
            except ValueError:
                print("Invalid Response, please re-enter value.")
                continue
        if (in_range == []) or (in_range != [] and value in in_range):
            return value
        else:
            print("Invalid Response, please re-enter value.")
            continue
