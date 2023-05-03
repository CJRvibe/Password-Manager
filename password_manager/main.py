from .query import SQLProcedures, DatabaseConnection
from argon2 import PasswordHasher, exceptions


class PasswordManagerInterface:

    def __init__(self, db_user, db_password, db_name):
        self.__db = DatabaseConnection(db_user, db_password, db_name)
        self.__ph = PasswordHasher()
        self.__user_id = None

    
    def login(self, username, password):
        user = self.__db.call_SQL_procedure(SQLProcedures.GET_USER, (username, ))
        hash = user[3]
        try:
            self.__ph.verify(hash, password)
            print(f"logged in as {user[1]}")
            self.__user_id = user[0] 
        except exceptions.VerifyMismatchError:
            print("Wrong password, try again!")