def get_key():
    key = open("token.txt", "r")
    token = key.read()

    return token
