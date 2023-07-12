import base64
import os
from pathlib import Path
from argon2 import PasswordHasher, exceptions
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from .query import SQLProcedures, DatabaseConnection, User, Credential
from . import custom_errors


class PasswordManagerInterface:

    def __init__(self, db_user, db_password, db_name):
        self.__db = DatabaseConnection(db_user, db_password, db_name)
        self.__ph = PasswordHasher()
        self.__user = None
        self.__phash = None
        self.__key = None


    def __logged_in(self):
        if self.__user.id == None:
            raise custom_errors.NotLoggedIn("Login before calling this function")
        
    
    def __find_salt(self):
        paths = sorted(Path.home().glob("*secrets.bin"))
        for path in paths:
            if path.stem == f"{self.__user.username}_secrets":
                return path.read_bytes()


    def __create_key(self, root_password, salt):
        kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(root_password.encode("utf-8")))
        return key

    
    def login(self, username, password):
        user = self.__db.call_SQL_procedure(SQLProcedures.GET_USER, (username, ))
        hash = user[3]
        try:
            self.__ph.verify(hash, password)
            print(f"logged in as {user[1]}")
        except exceptions.VerifyMismatchError:
            print("Wrong password, try again!")

        if self.__ph.check_needs_rehash(hash):
            hash = self.__ph.hash(password)
            self.__db.call_SQL_procedure(SQLProcedures.UPDATE_USER, 
                                         (self.__user.id, None, None, hash))
            
        self.__user = User(*user[0:3], password)
        self.__phash = hash
        salt = self.__find_salt()
        self.__key = self.__create_key(password, salt)
        return self.__user
    

    def create_account(self, username, email, password):
        password = self.__ph.hash(password)

        data = (username, email, password)
        self.__db.call_SQL_procedure(SQLProcedures.CREATE_USER, data)
        user = self.__db.call_SQL_procedure(SQLProcedures.GET_USER, (username, ))

        salt = os.urandom(16)
        secrets_path = Path.home() / Path(f"{username}_secrets.bin")
        secrets_path.write_bytes(salt)
        return User(*user[0:3], password)
    

    def create_credential(self, site, username, password: str):
        self.__logged_in()

        f = Fernet(self.__key)
        encrypted_password = f.encrypt(password.encode("utf-8"))

        data = (self.__user.id, site, username, encrypted_password)
        credential = self.__db.call_SQL_procedure(SQLProcedures.CREATE_CREDENTIALS, data)

    
    def get_credentials(self):
        self.__logged_in()

        data = self.__db.call_SQL_procedure(SQLProcedures.GET_CREDENTIALS, (self.__user.id, ))

        f = Fernet(self.__key)
        credentials = []
        for credential in data:
            password = f.decrypt(credential[4])
            credential_data = (credential[0], self.__user, *credential[2:4], password)
            credentials.append(Credential(*credential_data))

        return credentials