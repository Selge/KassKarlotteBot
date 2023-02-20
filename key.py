def get_key():
    token = open("token.txt", "r")
    print(token.read())


get_key()
