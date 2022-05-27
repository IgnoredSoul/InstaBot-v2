def create_token():
    Rcreds = {}
    Rcreds["client_id"] = input("Client_id: ")
    Rcreds["client_secret"] = input("Client_secret: ")
    Rcreds["user_agent"] = input("User_agent: ")
    Rcreds["username"] = input("Username: ")
    Rcreds["password"] = input("Password: ")
    return Rcreds

def create_login():
    Icreds = {}
    Icreds["username"] = input("Username: ")
    Icreds["password"] = input("Password: ")
    return Icreds