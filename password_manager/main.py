import base64
import os
from pathlib import Path
from argon2 import PasswordHasher, exceptions
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from .query import SQLProcedures, DatabaseConnection
from .exceptions import NotLoggedIn


class PasswordManagerInterface:

    def __init__(self, db_user, db_password, db_name):
        self.__db = DatabaseConnection(db_user, db_password, db_name)
        self.__ph = PasswordHasher()
        self.__user_id = None
        self.__username = None
        self.__phash = None


    def __logged_in(self):
        if self.__user_id == None:
            raise NotLoggedIn("Login before calling this function")
        
    
    def __find_salt(self):
        paths = sorted(Path.home().glob("*secrets.bin"))
        for path in paths:
            if path.stem == f"{self.__username}_secrets":
                return path

    
    def login(self, username, password):
        user = self.__db.call_SQL_procedure(SQLProcedures.GET_USER, (username, ))
        hash = user[3]
        try:
            self.__ph.verify(hash, password)
            print(f"logged in as {user[1]}")
        except exceptions.VerifyMismatchError:
            print("Wrong password, try again!")

        if self.__ph.check_needs_rehash(hash):
            self.__db.call_SQL_procedure(SQLProcedures.UPDATE_USER, 
                                         (self.__user_id, None, None, self.__ph.hash(password)))
            
        self.__user_id = user[0] 
        self.__username = user[1]
        self.__phash = user[3]
        *data, hashed_password = user
        return tuple(data)
    

    def create_account(self, username, email, password):
        password = self.__ph.hash(password)

        data = (username, email, password)
        new = self.__db.call_SQL_procedure(SQLProcedures.CREATE_USER, data)

        salt = os.urandom(16)
        secrets_path = Path.home() / Path(f"{username}_secrets.bin")
        secrets_path.write_bytes(salt)
        print(f"New account created with username {username}")
    

    def create_credentials(self, root_password: str, site, username, password: str):
        self.__logged_in()
        self.__ph.verify(self.__phash, root_password)

        salt = self.__find_salt().read_bytes()
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=480000,
            )
        key = base64.urlsafe_b64encode(kdf.derive(root_password.encode("utf-8")))
        f = Fernet(key)
        encrypted_password = f.encrypt(password.encode("utf-8"))

        data = (self.__user_id, site, username, encrypted_password)
        credential = self.__db.call_SQL_procedure(SQLProcedures.CREATE_CREDENTIALS, data)

    
    def get_credentials(self, root_password):
        self.__logged_in()
        self.__ph.verify(self.__phash, root_password)

        data = self.__db.call_SQL_procedure(SQLProcedures.GET_CREDENTIALS, (self.__user_id, ))
        salt = self.__find_salt().read_bytes()
        print(salt)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=480000,
            )
        key = base64.urlsafe_b64encode(kdf.derive(root_password.encode("utf-8")))
        f = Fernet(key)
        new_data = []
        for credential in data:
            password = f.decrypt(credential[2])
            new_data.append((credential[0], credential[1], password))

        return new_data