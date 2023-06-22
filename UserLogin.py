import os
import hashlib

class UserLogin:
    def __init__(self, user_db_folder="./users"):
        self.user_db_folder = user_db_folder
        if not os.path.exists(user_db_folder):
            os.mkdir(user_db_folder)

    def login(self,):
        username = str(input('Username: '))
        password = str(input('Password: '))

        user_path = os.path.join(self.user_db_folder,  username + ".txt")
        if not os.path.exists(user_path):
            print("Username " + username + " does not exist!")
            return 0
        else:
            with open(user_path, 'r') as f:
                if f.readline() ==  hashlib.md5(password.encode()).hexdigest():
                    print("Login succes!")
                    return 1
                else:
                    return 0

    def register(self,):
        username = str(input('Username: '))
        password = str(input('Password: '))

        user_path = os.path.join(self.user_db_folder,  username + ".txt")
        if os.path.exists(user_path):
            print("Username " + username + " already exists!")
            return 0
        else:
            hashed_password = hashlib.md5(password.encode()).hexdigest()
            with open(user_path, "w") as f:
                f.write(hashed_password)
            print("User with username: " + username + " created succesfuly !")
            return 1
        
    def run(self):
        while True:
            print('1 - Login')
            print('2 - Register')
            print('3 - Exit')
            choice = int(input('Choice: '))
            if choice == 1:
                login_flag = self.login()
                if login_flag:
                    break
            elif choice == 2:
                _ = self.register()
            elif choice == 3:
                exit()
            else:
                print('Invalid choice !')

