import os
import sys
import datetime

SAVE_FILE_PATH = 'save.csv'

class PostNotFoundError(Exception):
    pass
    
def autosave(func):
    # caller.save가 구현되지 않은 곳에 데코레이터가 붙은 경우에 대한 예외 처리
    def decorated(caller, *args, **kwargs):
        func(caller, *args, **kwargs)
        caller.save()
    return decorated

class Board():
    POSTS_PER_PAGE = 15

    def __init__(self):
        self.current_page = 1
        self.posts = list()
        try:
            self.load()
        except FileNotFoundError:
            pass
        self.actions = [
            {
                'title': '작성하기',
                'handler': self.create_post
            },
            {
                'title': '수정하기',
                'handler': self.update_post
            },
            {
                'title': '삭제하기',
                'handler': self.delete_post
            },
            {
                'title': '이전 페이지로',
                'handler': self.go_prev_page
            },
            {
                'title': '다음 페이지로',
                'handler': self.go_next_page
            }
        ]
    
    def print_actions(self):
        print('-' * 100)
        for index, action in enumerate(self.actions):
            print('{}. {}'.format(index + 1, action.get('title')))
        print('-' * 100)
    
    def get_user_action(self):
        try:
            user_action_index = int(input('> '))
            self.actions[user_action_index - 1]['handler']()
        except (IndexError, ValueError):
            input('잘못된 행동 번호를 입력하셨습니다.')
    
    def search_post_by_id(self, pid):
        for index, post in enumerate(self.posts):
            if post.has_pid(pid):
                return index, post
        raise PostNotFoundError
    
    def list_posts(self):
        if len(self.posts) == 0:
            print('게시판에 아직 작성된 글이 없습니다.')
            print('한 번 작성해보는 것은 어떨까요?')
            return

        page_from = (self.current_page - 1) * Board.POSTS_PER_PAGE
        page_to = self.current_page * Board.POSTS_PER_PAGE
        for post in self.posts[page_from : page_to]:
            print(post)
    
    @autosave
    def create_post(self):
        title = input('작성 > ')
        self.posts.insert(0, Post(title))
    
    @autosave
    def update_post(self):
        try:
            pid = int(input('몇 번 글을 수정할까요? '))
            new_title = input('수정 > ')
            _, post = self.search_post_by_id(pid)
            post.update(new_title)
        except (PostNotFoundError, IndexError, ValueError):
            input('잘못된 글 번호를 입력하셨습니다.')

    @autosave
    def delete_post(self):
        try:
            pid = int(input('몇 번 글을 지울까요? '))
            index, _ = self.search_post_by_id(pid)
            del self.posts[index]
        except (PostNotFoundError, IndexError, ValueError):
            input('잘못된 글 번호를 입력하셨습니다.')
    
    def load(self):
        global SAVE_FILE_PATH
        f = open(SAVE_FILE_PATH, 'r', encoding='utf-8')
        posts = f.readlines()
        for post in posts:
            self.posts.append(Post.from_csv(post))
        f.close()
    
    def save(self):
        global SAVE_FILE_PATH
        f = open(SAVE_FILE_PATH, 'w', encoding='utf-8')
        for post in self.posts:
            print(post.to_csv(), file=f)
        f.close()

    def go_prev_page(self):
        if self.current_page > 1:
            self.current_page -= 1

    def go_next_page(self):
        if self.current_page * Board.POSTS_PER_PAGE < len(self.posts):
            self.current_page += 1

class Post():
    pid = 1

    def __init__(self, title, pid=None, created_at=None):
        self.pid = Post.pid if pid is None else pid
        self.title = title
        self.created_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M") if created_at is None else created_at
        Post.pid += 1

    def __str__(self):
        return '{:^8} | {:60.60} | {}'.format(self.pid, self.title, self.created_at)
    
    def update(self, new):
        self.title = new
    
    def has_pid(self, pid):
        return self.pid == pid
        
    @classmethod
    def from_csv(cls, csv):
        pid, title, created_at = csv[:-1].split(',')
        return cls(title, pid, created_at)
    
    def to_csv(self):
        return '{},{},{}'.format(self.pid, self.title, self.created_at)

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