from enum import Enum
from typing import Sequence
import pymysql

class SQLProcedures(Enum):
    CREATE_CREDENTIALS = "CALL create_credentials(%s, %s, %s, %s, %s)"
    CREATE_USER = "CALL create_user(%s, %s, %s)"
    GET_CREDENTIALS = "CALL get_credentials(%s)"
    GET_USER = "CALL get_user(%s)"
    UPDATE_CREDENTIALS = "CALL update_credentials(%s, %s, %s, %s, %s)"
    UPDATE_USER = "CALL update_user(%s, %s, %s, %s)"
    

class DatabaseConnection:

    def __init__(self, user, password, database) -> None:
        self.database_connect(user, password, database)

    
    def database_connect(self, user, password, database):
        connection = pymysql.connect(
            user=user,
            password=password,
            database=database)
        
        self.connection = connection

    
    def call_SQL_function(self, function: Enum, params: Sequence):
        with self.connection.cursor() as cursor:          
            cursor.execute(function.value, params)
            return cursor.fetchone()[0]
        
    
    def get_user(self, name):
        args = (name, )
        
        with self.connection.cursor() as cursor:
            cursor.callproc("get_user", args)
            return cursor.fetchone()
        
    
    def get_credentials(self, user_id):
        args = (user_id, )

        with self.connection.cursor() as cursor:
            cursor.callproc("get_credentials", args)
            return cursor.fetchall()

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
