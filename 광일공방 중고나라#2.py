import os
import sys

class Board():
    def __init__(self):
        self.posts = list()
        self.actions = [self.create_post, self.update_post, self.delete_post]
    
    @staticmethod
    def print_actions():
        print('--------------------------------------------------')
        print('1. 작성하기')
        print('2. 수정하기')
        print('3. 삭제하기')
        print('--------------------------------------------------')
    
    def get_user_action(self):
        try:
            user_action_index = int(input('> '))
            self.actions[user_action_index - 1]()
        except (IndexError, ValueError):
            input('잘못된 행동 번호를 입력하셨습니다.')

    
    def list_posts(self):
        if len(self.posts) == 0:
            print('게시판에 아직 작성된 글이 없습니다.')
            print('한 번 작성해보는 것은 어떨까요?')
            return

        for index, post in enumerate(self.posts):
            post_no = index + 1
            print('{}. {}'.format(post_no, post))
    
    def create_post(self):
        self.posts.append(input('작성 > '))
        input('{}번째 글이 성공적으로 작성되었습니다.'.format(len(self.posts)))
    
    def update_post(self):
        try:
            post_no = int(input('몇 번 글을 수정할까요? '))
            self.posts[post_no - 1] = input('수정 > ')
        except (IndexError, ValueError):
            input('잘못된 글 번호를 입력하셨습니다.')

    def delete_post(self):
        try:
            post_no = int(input('몇 번 글을 지울까요? '))
            del self.posts[post_no - 1]
        except (IndexError, ValueError):
            input('잘못된 글 번호를 입력하셨습니다.')

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

if __name__ == "__main__":
    print_greeting_message()
    board = Board()
    while True:
        clear_screen()
        board.list_posts()
        board.print_actions()
        board.get_user_action()