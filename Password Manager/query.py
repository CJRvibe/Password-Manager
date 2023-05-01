from enum import Enum
from typing import Sequence
import mysql.connector

class SQLFunctions(Enum):
     GET_PASSWORD_HASH = "SELECT get_password_hash(%s)"
     GET_USER_ID = "SELECT get_user_id(%s)"
     GET_CREDENTIAL_ID = "SELECT get_credential_id(%s)"


class DatabaseConnection:

    def __init__(self, user, password, database) -> None:
        self.database_connect(user, password, database)
        self.logged_in_id = None

    
    def database_connect(self, user, password, database):
        connection = mysql.connector.connect(
            user=user,
            password=password,
            database=database)
        
        self.connection = connection

    
    def call_SQL_function(self, function: Enum, params: Sequence):
        with self.connection.cursor() as cursor:          
            cursor.execute(function.value, params)
            return cursor.fetchone()[0]
        

    def create_credentials(self, user_id, site, username, password, pin=None):
        args = (user_id, site, username, password, pin)

        with self.connection.cursor() as cursor:
            cursor.callproc("create_credentials", args)
            return cursor.fetchone()
    

    def create_user(self, name, email, root_password):
        args = (name, email, root_password)

        with self.connection.cursor() as cursor:
            cursor.callproc("create_user", args)
            return cursor.fetchone()


    def update_credential(self, credential_id, site=None, username=None, password=None, pin=None):
        args = (credential_id, site, username, password, pin)

        with self.connection.cursor() as cursor:
            cursor.callproc("get_credentials", args)
            return cursor.fetchone()

    def update_user(self, name=None, email=None, root_password=None):
        args = (name, email, root_password)

        with self.connection.cursor() as cursor:
            cursor.callproc("update", args)
            cursor.fetchone()
