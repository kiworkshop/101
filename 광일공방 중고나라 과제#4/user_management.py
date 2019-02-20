import csv
from user import User 


USER_DATA_PATH = 'second-hand_shop_user_data.csv'

class User_management:
    def __init__(self):
        self.actions = [self.sign_up, self.sign_in]
        self.users = []

    @staticmethod 
    def print_actions(): 
        print('---------------------------------------')
        print('1. 회원가입')
        print('2. 로그인')
        print('---------------------------------------')
    
    def get_user_action(self):
        try:
            user_action_no = int(input('> '))
        except:
            print('잘못된 입력입니다.')
            input()    
            return  
        if user_action_no >0 and user_action_no <= len(self.actions):
            signed_in_user_id = self.actions[user_action_no - 1]()
            return signed_in_user_id
        print('잘못된 입력입니다.')

    def load_users(self):
        with open (USER_DATA_PATH, 'r', encoding='utf8') as load_data:
            users_read = csv.reader(load_data)
            #print(posts_read)
            users_read = [User.load_from_file(*user) for user in users_read]
            self.users = list(users_read)

    def sign_up(self):
        user_id = input('아이디: ')
        user_password = input('비밀번호: ')
        new_user = User(user_id, user_password)
        self.users.append(new_user)

        save_data = open (USER_DATA_PATH, 'w', encoding='utf8', newline='')
        users_write = csv.writer(save_data)
        for user in self.users:
            users_write.writerow(user.save_to_file())
        save_data.close()
        
        self.sign_in_success(user_id)
        return user_id
        
    def sign_in(self):
        input_user_id = input('아이디: ')
        input_user_password = input('비밀번호: ')

        checked_user = list(user for user in self.users if user.user_id == input_user_id and user.user_password == input_user_password)
        if checked_user != []:
            self.sign_in_success(input_user_id)   
            return input_user_id
        if checked_user == []:
            input('로그인에 실패하였습니다')
        
    def sign_in_success(self, user_id):
        input('로그인 성공: 환영합니다, {} 님!'.format(user_id))

        