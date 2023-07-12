import base64
import copy
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
        if self.__user== None:
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
            return

        if self.__ph.check_needs_rehash(hash):
            hash = self.__ph.hash(password)
            self.__db.call_SQL_procedure(SQLProcedures.UPDATE_USER, 
                                         (self.__user.id, None, None, hash))
            
        self.__user = User(*user[0:3], password)
        user = copy.copy(self.__user)
        self.__phash = hash
        salt = self.__find_salt()
        self.__key = self.__create_key(password, salt)
        return user
    

    def create_account(self, username, email, password):
        self.__phash = self.__ph.hash(password)

        data = (username, email, self.__phash)
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
    

    def update_user(self, user: User):
        self.__logged_in()
        if user == self.__user:
            raise custom_errors.InvalidValue("There is no change in the data value")
        
        if self.__user.password == user.password:

            if self.__user.username != user.username:
                salt = self.__find_salt()
                old_path = Path.home() / Path(f"{self.__user.username}_secrets.bin")

                if old_path.exists(): old_path.unlink()

                secrets_path = Path.home() / Path(f"{user.username}_secrets.bin")
                secrets_path.write_bytes(salt)
            
            
            data = user.unpack()
            self.__db.call_SQL_procedure(SQLProcedures.UPDATE_USER, (*data[0:3], None))
            self.__user = copy.copy(user)
            return
        
        # get old credentials first before updating
        old_credentials = self.get_credentials()
        
        # update new file path
        old_path = Path.home() / Path(f"{self.__user.username}_secrets.bin")
        if old_path.exists: old_path.unlink()

        salt = os.urandom(16)
        secrets_path = Path.home() / Path(f"{user.username}_secrets.bin")
        secrets_path.write_bytes(salt)

        # update internal variables
        updated_key = self.__create_key(user.password, self.__find_salt())

        # update old credential
        f = Fernet(updated_key)
        new_credentials = list()
        for credential in old_credentials:
            new_password = f.encrypt(credential.password)
            partial_object = (credential.id, new_password)
            data = new_credentials.append(partial_object)
            
        print(new_credentials)
        self.__db.bulk_update_credentials(new_credentials)


        self.__key = updated_key
        self.__user = copy.copy(user)
        self.__phash = self.__ph.hash(user.password)
        data = (user.id, user.username, user.email, self.__phash)
        self.__db.call_SQL_procedure(SQLProcedures.UPDATE_USER, data)
        

