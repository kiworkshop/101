import hashlib
import os
from user import User

USER_FILE_PATH = './광일공방중고나라_사용자목록.csv'

class Membership_manager():
    def __init__(self):
        self.actions = [self.log_in, self.sign_up]
    
    # 로그인 / 회원가입 메뉴
    def menu(self):
        print('-' * 100)
        print('1. 로그인')
        print('2. 회원가입')
        print('-' * 100)

    def action_handler(self):
        try:
            menuSel = int(input('> '))
            if menuSel <= 0:
                raise IndexError
            return self.actions[menuSel - 1]()
        except ValueError:
            input('잘못 입력하셨습니다. 올바른 번호를 선택하세요.')
        except IndexError:
            input('잘못 입력하셨습니다. 메뉴의 번호를 알맞게 입력하세요.')
        except Exception as e:
            input('잘못 입력하셨습니다.', e)
        
    # 입력한 ID와 사용자 목록에서의 아이디 비교 
    def check_existing_id(self, id):
        global USER_FILE_PATH
        if os.path.exists(USER_FILE_PATH) is False:
            return None
        
        f = open(USER_FILE_PATH, 'r', encoding='utf-8')
        users = f.readlines()
        target_user = None
        i = 0
        while i < len(users) and target_user is None:
            target_id, target_pwd = users[i][:-1].split(',')
            target_user = (target_id, target_pwd) if target_id == id else None
            i += 1
        f.close()
        return target_user
    
    def log_in(self):
        global USER_FILE_PATH

        id = input('아이디 : ')
        pwd = input('비밀번호 : ')
        target_id, target_pwd = self.check_existing_id(id) or (None, None)
        if target_id is None:
            input('로그인 실패 : 아이디가 존재하지 않습니다. 처음이시라면 회원가입을 선택해주세요.')
            return None
        if target_pwd != hashlib.sha256(pwd.encode()).hexdigest():
            input('로그인 실패 : 비밀번호가 틀렸습니다. 다시 시도해주세요.')
            return None

        input('로그인 성공 : 환영합니다 {}님!'.format(id))
        return id
        
    def sign_up(self):
        id = input('아이디 : ')
        pwd = input('비밀번호 : ')
        target_id, _ = self.check_existing_id(id) or (None, None)
        if target_id is not None:
            input('회원가입 실패 : 해당 아이디가 이미 존재합니다. 다른 아이디를 작성해주세요.')
            return None

        new_user = User(id, pwd)
        f = open(USER_FILE_PATH, 'a', encoding='utf-8')
        print(new_user.to_csv(), file=f)
        f.close()

        input('회원가입 및 로그인 성공 : 환영합니다 {}님!'.format(id))
        return id