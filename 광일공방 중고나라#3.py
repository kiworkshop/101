import os
import sys
import datetime

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_greeting_message():
    clear_screen()
    greeting_message = '''
    본 프로그램은 광일공방에서 중고거래 사이트를 기웃기웃 거리던 광일이가
    어느날 삘이 꽂혀 '아! 여기가 돈 나오는 방석이다!' 생각하자마자 아주
    급하게 만들어낸 불안정한 중고거래 사이트입니다. 물론 아직은 허접한 
    게시판이지만 1000만 사용자를 꿈꾸는 광일이는 커다란 희망의 씨앗을 마음에
    품고서 오늘도 밤을 지새우며 코드를 작성합니다.
    '''
    print(greeting_message)
    input('프로그램을 시작하시려면 엔터키를 입력하세요...')

def auto_save(func):
    def wrapper(self):
        func(self)
        self.save_posts()
    return wrapper

class Post(): 
    def __init__(self):
        self.no = None
        self.title = None 
        self.created_time = None
        self.all_posts = list()

    @auto_save
    def create_post(self):
        self.title = input('작성 > ')
        try:
            self.no = self.all_posts[-1]['no'] + 1 
        except:
            self.no = 1
        current_time = datetime.datetime.today()
        self.created_time = current_time.strftime('%Y-%m-%d %H:%M')
        self.all_posts.append(dict(zip(['no', 'title', 'created_time'],
                                   [self.no, self.title, self.created_time])))
        input(f'{self.no}번 글이 성공적으로 작성되었습니다. ')

    @auto_save
    def update_post(self):
        try:
            post_no = int(input('몇 번 글을 수정할까요? '))
            all_posts_numbers = list()
            for post in self.all_posts:
                all_posts_numbers.append(post['no'])
            if post_no not in all_posts_numbers:
                input(f'{post_no}번 글을 찾을 수 없습니다. ')
        except:
            input('잘못된 입력입니다.')
            return
        
        for post in self.all_posts:
            if post['no'] == post_no:
                post.update(title = input('수정 > '))

    @auto_save
    def delete_post(self):
        try:
            post_no = int(input('몇 번 글을 지울까요? '))
            all_posts_numbers = list()
            for post in self.all_posts:
                all_posts_numbers.append(post['no'])
            if post_no not in all_posts_numbers:
                input(f'{post_no}번 글을 찾을 수 없습니다. ')  
        except:
            input('잘못된 입력입니다.')
            return           

        for post in self.all_posts:
            if post['no'] == post_no:
                 self.all_posts.remove(post)

    def save_posts(self):
        with open('posts.csv', 'w') as f:
            for post in self.all_posts:
                f.write('{}, {}, {}\n'.format(post['no'], post['title'], post['created_time']))
        input('파일이 저장되었습니다. ')

    def load_posts(self):
        try:
            with open('posts.csv', 'r') as f:
                for row in f:
                    no, title, created_time = row.strip('\n').split(', ')
                    no = int(no)
                    self.all_posts.append(dict(zip(['no', 'title', 'created_time'],
                                                    [no, title, created_time])))
        except:
            with open('posts.csv', 'w') as f:
                f.write('')      

class Board():
    def __init__(self, post):
        self.actions = [post.create_post, post.update_post, post.delete_post, post.save_posts, self.list_posts, self.list_posts]

    @staticmethod
    def print_actions():
        print('--------------------------------------------------')
        print('1. 작성하기')
        print('2. 수정하기')
        print('3. 삭제하기')
        print('4. 저장하기')
        print('5. 이전 페이지로')
        print('6. 다음 페이지로')
        print('--------------------------------------------------')
    
    page_no = 1
    def list_posts(self, post, page_count=0):
        if len(post.all_posts) == 0:
            print('게시판에 아직 작성된 글이 없습니다.')
            print('한 번 작성해보는 것은 어떨까요?')
            return
        
        self.page_no += page_count
        if self.page_no <= 0:
            self.page_no = 1
            return   
        if (self.page_no - 1) * 15 > len(post.all_posts):
            self.page_no -= 1
            return    

        i = (self.page_no - 1) * 15        
        while i < self.page_no * 15:
            try:
                posts = post.all_posts.copy()
                posts.reverse()
                no = posts[i]['no']
                title = posts[i]['title']
                created_time = posts[i]['created_time']
                print(str(no).center(8)[0:8], '|', title.ljust(60)[0:60], '|', created_time)
                i += 1
            except:
                return

    def get_user_action(self):
        try:
            user_action_index = int(input('> '))
        except:
            input('잘못된 입력입니다.')
            return

        if user_action_index > 0 and user_action_index <= 4:
            self.actions[user_action_index - 1]()
            return
        if user_action_index == 5:
            clear_screen()
            self.actions[4](post, page_count=-1)
            return
        if user_action_index == 6:
            clear_screen()
            self.actions[5](post, page_count=1)
            return    
        input('잘못된 입력입니다.')

if __name__ == "__main__":
    print_greeting_message()     
    post = Post()
    board = Board(post)
    post.load_posts()
    while True:
        clear_screen()
        board.list_posts(post)
        board.print_actions()
        board.get_user_action()