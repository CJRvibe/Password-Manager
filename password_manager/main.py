from query import SQLFunctions, DatabaseConnection
from argon2 import PasswordHasher


class PasswordManagerInterface:

    def __init__(self, db_user, db_password, db_name):
        self.__db = DatabaseConnection(db_user, db_password, db_name)
        self.__ph = PasswordHasher()
        self.user = None
