from getpass import getpass
from nxapi_class import NxAaa,NxL2,NxSystem

def nx_login(switch):
    user = input('What is your username: ')
    pw = getpass('What is your password ')

    return NxAaa(user, switch, pw).nx_login()
