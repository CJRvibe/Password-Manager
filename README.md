# Password Manager
This is a project that test my knowledge on python programming and encryption skills. Please take note this is not a real application, it is possible to host this app on your device if you wish to
## Simple Usage
```python
import os
from dotenv import load_dotenv
from password_manager import PasswordManagerInterface

load_dotenv()
database_credential = (os.getenv("DB_USER"), os.getenv("DB_PASSWORD"), "password_manager")
manager = PasswordManagerInterface(*database_credential)

# This will create a new account and return a User object
new_user = manager.create_account(
    username="user1", 
    email="user1@gmail.com",
    password="1234"
) 

manager.login(new_user.username, new_user.password)

# credentials are the various respective passwords for a main user
manager.create_credential(site="Google", username="user1_google", password="1234")
manager.create_credential(site="safari", username="user1_safari", password="5678")
manager.create_credential(site="youtube", username="user1_youtube", password="9012")

credentials = manager.get_credentials()
# loop over to get each credential object
for credential in credentials:
    print(credential)
```


### Salt File
Please take note that a binary salt file will be instantly generated when you create a new account and stored in your computer. Do not delete the salt file as the program will regularly attempt to read the bytes of the salt file to generate encryption key for you.
To find the salt path, you can use:
```python
from pathlib import Path

salt_path = Path.home() / Path(f"{User.username}_secrets.bin")
```
The user object comes from your user account which the application will return it to you upon creating or logging in an account
