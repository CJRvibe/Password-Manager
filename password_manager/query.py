from dataclasses import dataclass
from enum import Enum
from typing import Sequence
import pymysql

class SQLProcedures(Enum):
    CREATE_CREDENTIALS = "CALL create_credentials(%s, %s, %s, %s)"
    CREATE_USER = "CALL create_user(%s, %s, %s)"
    GET_CREDENTIALS = "CALL get_credentials(%s)"
    GET_USER = "CALL get_user(%s)"
    UPDATE_CREDENTIALS = "CALL update_credentials(%s, %s, %s, %s)"
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

    
    def call_SQL_procedure(self, function: Enum, params: Sequence):
        with self.connection.cursor() as cursor:          
            cursor.execute(function.value, params)

            if function is not SQLProcedures.GET_CREDENTIALS:
                result =  cursor.fetchone()
            else: result = cursor.fetchall()
        
        self.connection.commit()
        return result
        
    
    def close_connection(self):
        self.connection.close()


@dataclass
class User:
    id: int
    username: str
    email: str
    password: str

    def __repr__(self):
        class_name = type(self).__name__
        return f"{class_name}(username=\"{self.username}\")"


@dataclass
class Credential:
    id: int
    main_user: User
    site: str
    username: str
    password: str

    def __repr__(self):
        class_name = type(self).__name__
        return f"{class_name}(main_user=\"{self.main_user.username}\", site=\"{self.site}\")"