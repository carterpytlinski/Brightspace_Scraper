import os

def getUserCredentials():
    USER_USERNAME, USER_PASSWORD = os.environ.get('USERNAME'), os.environ.get('PASSWORD')
    return {'username': USER_USERNAME, 'password': USER_PASSWORD}

