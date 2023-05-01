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