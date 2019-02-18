import hashlib
from user import User

SAVE_FILE_PATH = 'user.csv'

class LoginPage():    
    def __init__(self):
        self.authentication = False
        self.user_id = None
        self.user_pw = None
        self.users = list()
        try:
            self.load()
        except FileNotFoundError:
            pass
        self.actions = [self.login, self.join]

    def print_actions(self):
        print('-' * 100)
        print('1. 로그인')
        print('2. 회원가입')
        print('-' * 100)

    def get_user_action(self):
        try:
            user_action_index = int(input('> '))
        except:
            input('잘못된 입력입니다.')
            return

        if user_action_index > 0 and user_action_index <= len(self.actions):
            self.actions[user_action_index - 1]()
            return
        input('잘못된 입력입니다.')

    @staticmethod
    def encrypt_in_sha256(pw):
        pw = pw.encode()
        encrypted_pw = hashlib.sha256(pw).digest()
        return encrypted_pw

    def complete_authentication(self):
        self.authentication = True
        User.logged_in = self.user_id
        input(f'로그인 성공 : 환영합니다 {self.user_id}님!')    

    def verify_user(self):
        for user in self.users:
            if user.user_id == self.user_id and user.user_pw == self.user_pw:
                return True    

    def check_if_input_is_blank(self):
        blank = b"\xe3\xb0\xc4B\x98\xfc\x1c\x14\x9a\xfb\xf4\xc8\x99o\xb9$'\xaeA\xe4d\x9b\x93L\xa4\x95\x99\x1bxR\xb8U" 
        return self.user_id == '' or self.user_pw == blank

    def check_id_duplication(self):
        for user in self.users:
            if user.user_id == self.user_id:
                return False
        return True
        
    def login(self):      
        self.user_id = input('아이디 : ')
        self.user_pw = str(LoginPage.encrypt_in_sha256(input('비밀번호 : ')))  
        if self.verify_user():
            self.complete_authentication()
            return
        input('로그인에 실패하였습니다.')

    def join(self):
        self.user_id = input('아이디 : ')
        self.user_pw = LoginPage.encrypt_in_sha256(input('비밀번호 : ')) 
        if self.check_if_input_is_blank() is True:
            input('공백을 입력할 수 없습니다.')
            return 
        if self.check_id_duplication() is True:
            self.users.insert(0, User(self.user_id, self.user_pw))
            self.save()
            self.complete_authentication()
            return
        input('이미 존재하는 아이디입니다.')
    
    def load(self):
        global SAVE_FILE_PATH
        f = open(SAVE_FILE_PATH, 'r', encoding='utf-8')
        users = f.readlines()
        for user in users:
            self.users.append(User.from_csv(user))
        f.close()

    def save(self):
        global SAVE_FILE_PATH
        f = open(SAVE_FILE_PATH, 'w', encoding='utf-8')
        for user in self.users:
            print(user.to_csv(), file=f)
        f.close()