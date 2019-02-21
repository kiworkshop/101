import hashlib
import os
import sys

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_hashed_password(password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    return hashed_password

class UserNotFoundError(Exception):
    pass

SAVE_FILE_PATH = 'User.csv'

class User:
    users = {}
    login_success = False

    def __init__(self, user_id):
        self.user_id = user_id

    @classmethod
    def is_success(cls, user_id, user_pw): 
        if cls.users[user_id] == user_pw:
            input('로그인에 성공하였습니다.')
            return True 

    @classmethod
    def check_existence_of_user_id(cls, user_id):
        try:
            cls.users[user_id]
            User.user_id_existence = True
        except (KeyError):
            print('아이디가 없습니다. 다시 입력해주세요.')

    @classmethod
    def get_user_id_and_pw(cls):
        User.user_id_existence = False
        while not User.user_id_existence:
            user_id = input('아이디 입력>')
            cls.check_existence_of_user_id(user_id)
        user_pw = get_hashed_password(input('비밀번호를 입력하세요>'))
        return (user_id, user_pw)
    
    @classmethod
    def login(cls):
        user_id, user_pw = cls.get_user_id_and_pw()
        User.login_success = cls.is_success(user_id, user_pw)
        while not User.login_success:
            input('비밀번호가 틀렸습니다. 엔터를 누르고 다시 입력해주세요.')
            user_pw = get_hashed_password(input('비밀번호를 입력하세요>'))
            User.login_success = cls.is_success(user_id, user_pw)
        return User(user_id)

    @classmethod
    def save(cls):
        global SAVE_FILE_PATH
        f = open(SAVE_FILE_PATH, 'w', encoding='utf-8')
        for user_id, user_pw in cls.users.items(): 
            print(cls.to_csv(user_id,user_pw), file = f)
        f.close()

    @classmethod
    def to_csv(cls, user_id, user_pw):
        return '{},{}'.format(user_id, user_pw)

    @classmethod
    def load(cls):
        global SAVE_FILE_PATH
        f = open(SAVE_FILE_PATH, 'r', encoding = 'utf-8')
        users = f.readlines()
        
        for user in users:
            user_id, user_pw = cls.from_csv(user)
            cls.users[user_id] = user_pw 
            
    @classmethod
    def create_user(cls):
        new_user_id = input('아이디 작성>')
        if new_user_id in User.users:
            input('이미 존재하는 ID입니다.')
            return
        new_user_pw = get_hashed_password(input('비밀번호를 입력하세요>'))
        cls.users[new_user_id] = new_user_pw
        cls.save()
        return User(new_user_id)

    @classmethod
    def from_csv(cls, csv):
        user_id, user_pw = csv[:-1].split(',')
        return (user_id, user_pw)

