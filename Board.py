import os
import sys
from User import User
from Post import Post

SAVE_FILE_PATH = 'save.csv'

class PostNotFoundError(Exception):
    pass
    
def autosave(func):
    def decorated(caller, *args, **kwargs):
        func(caller, *args, **kwargs)
        caller.save()
    return decorated

def auto_check_authority(func):
    def decorated(caller, *args, **kwargs):
        article = func(caller, *args, **kwargs)   
        caller.check_authorization(article)
        return article
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
        try:
            User.load()
        except FileNotFoundError:
            pass
        self.login_actions = [
            {
                'title' : '로그인하기',
                'handler' : self.login
            },
            {
                'title' : '회원가입하기',
                'handler' : self.create_user
            }
        ]
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
            if post.has_pid(pid) and post.is_undeleted():
                return index, post
        raise PostNotFoundError
    
    def get_undeleted_posts(self, post):
        if post.is_undeleted():
            self.undeleted_posts.append(post)
    
    def list_posts(self):
        self.undeleted_posts = list()
        for post in self.posts:
            self.get_undeleted_posts(post)
        
        if len(self.undeleted_posts) == 0:
            print('게시판에 아직 작성된 글이 없습니다.')
            print('한 번 작성해보는 것은 어떨까요?')
            return

        page_from = (self.current_page - 1) * Board.POSTS_PER_PAGE
        page_to = self.current_page * Board.POSTS_PER_PAGE
        for post in self.undeleted_posts[page_from : page_to]:
            print(post)
    
    @autosave
    def create_post(self):
        title = input('작성 > ')
        self.posts.insert(0, Post(title, self.user.user_id, 'UNDELETED'))

    def check_authorization(self, post):
        self.post_authorization = self.user.user_id == post.user_id

    @auto_check_authority
    def get_updated_post(self):
        try:
            pid = input('몇 번 글을 수정할까요? ')
            _, post = self.search_post_by_id(pid)
            return post
        except (PostNotFoundError, IndexError):
            input('잘못된 글 번호를 입력하셨습니다.')
            pass
        
    @autosave
    def update_post(self):
        post = self.get_updated_post()

        if not self.post_authorization: 
            input('{}님은 글 수정 권한이 없습니다.'.format(self.user.user_id))
            return 

        try:
            new_title = input('수정 > ')
            post.update(new_title)
        except (PostNotFoundError, IndexError, ValueError): #indexerror를 만드신 이유가 있을까
            input('잘못된 글 번호를 입력하셨습니다.')

    @auto_check_authority
    def get_deleted_post(self):
        try:
            pid = input('몇 번 글을 삭제할까요?')
            _, post = self.search_post_by_id(pid)
        except (PostNotFoundError, IndexError):
            input('잘못된 글 번호를 입력하셨습니다.')
        return post

    @autosave
    def delete_post(self):
        post = self.get_deleted_post()

        if not self.post_authorization:
            input('{}님은 글 삭제 권한이 없습니다.'.format(self.user.user_id))
            return

        try:
            post.delete()
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
        if self.current_page == 1:
            return
        
        self.current_page -= 1

    def go_next_page(self):
        if self.current_page * Board.POSTS_PER_PAGE < len(self.posts):
            self.current_page += 1

    def print_login_actions(self):
        print('-' * 100)
        for index, action in enumerate(self.login_actions):
            print('{}. {}'.format(index + 1, action.get('title')))
        print('-' * 100)

    def get_user_login_action(self):
        try:
            login_action_index = int(input('> '))
            self.login_actions[login_action_index - 1]['handler']()
        except (IndexError, ValueError):
            input('잘못된 행동 번호를 입력하셨습니다.')

    def login(self):
        self.user = User.login()

    def create_user(self):
        self.user = User.create_user()
