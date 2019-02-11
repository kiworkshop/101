import hashlib
from SAVE import SAVE_PATH_USER, autosave

def get_hashed_password(password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    return hashed_password

class ExistingIdError(Exception):
    pass

class NotExistingIdError(Exception):
    pass

class InvalidPassword(Exception):
    pass

class UserManager:
    LOGINNED_USER = None

    def __init__(self):
        self.users = list()
        self.action_list = [
            {
                "title" : "로그인",
                "handler" : self.user_login
            },
            {
                "title" : "회원가입",
                "handler" : self.user_join
            }
        ]
        try:
            self.load()
        except FileNotFoundError:
            pass

    def load(self):
        global SAVE_PATH_USER
        f = open(SAVE_PATH_USER, 'r')
        users = f.readlines()
        for user in users:
            self.users.append(User.from_csv(user))
        f.close()
    
    def save(self):
        global SAVE_PATH_USER
        f = open(SAVE_PATH_USER, 'w')
        for user in self.users:
            print(user.to_csv(), file = f)
        f.close()

    def search_user_by_id_for_login(self, user_id):
        for user in self.users:
            if user.has_id(user_id):
                return user
        raise NotExistingIdError

    def search_user_by_id_for_join(self, user_id):
        for user in self.users:
            if user.has_id(user_id):
                raise ExistingIdError

    def user_login(self):
        try:
            user_id = input("ID를 입력하세요.")
            user = self.search_user_by_id_for_login(user_id)

            hashed_password = get_hashed_password(input("password를 입력하세요."))
            if not user.check_password(hashed_password):
                raise InvalidPassword
            if user.check_password(hashed_password):
                UserManager.LOGINNED_USER = user
                print("로그인 성공 : 환영합니다 {}님".format(UserManager.LOGINNED_USER.user_id))
        except NotExistingIdError:
            print("존재하지 않는 ID입니다.")
        except InvalidPassword:
            print("비밀번호가 일치하지 않습니다.")

    @autosave
    def user_join(self):
        try:
            user_id = input("ID를 입력하세요.")
            self.search_user_by_id_for_join(user_id)

            hashed_password = get_hashed_password(input("password를 입력하세요."))
            user = User(user_id, hashed_password)
            self.users.append(user)

            UserManager.LOGINNED_USER = user
            print("로그인 성공 : 환영합니다 {}님".format(user.user_id))
        except ExistingIdError:
            print("이미 존재하는 ID입니다.")            

    def print_actions(self):
        print('-' * 100)
        for index, action in enumerate(self.action_list):
            print("{}. {}".format(index + 1, action["title"]) )
        print('-' * 100)

    def execute_action(self):
        try:   
            action_no = int(input("번호를 입력하세요."))
            self.action_list[action_no - 1]["handler"]()
        except (IndexError, ValueError):
            print("잘못된 입력입니다.")

        input("엔터를 입력하세요.")

class User:

    def __init__(self, user_id, user_password):
        self.user_id = user_id
        self.user_password = user_password

    @classmethod
    def from_csv(cls, csv):
        user_id, user_password = csv.strip('\n').split(',')
        return cls(user_id, user_password)
    
    def to_csv(self):
        return f"{self.user_id},{self.user_password}"

    def has_id(self, user_id):
        return self.user_id == user_id
    
    def check_password(self, hashed_password):
        return self.user_password == hashed_password
