import mysql.connector


class DatabaseConnection:

    def __init__(self, user, password, database) -> None:
        self.database_connect(user, password, database)

    
    def database_connect(self, user, password, database):
        connection = mysql.connector.connect(
            user=user,
            password=password,
            database=database)
        
        self.connection = connection