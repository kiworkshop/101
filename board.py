from post import Post
from user import User

SAVE_FILE_PATH = 'save.csv'

class PostNotFoundError(Exception):
    pass
    
def autosave(func):
    def wrapper(caller, *args, **kwargs):
        func(caller, *args, **kwargs)
        caller.save()
    return wrapper

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
            if post.has_pid(pid) and post.is_not_deleted():
                return index, post
        raise PostNotFoundError
    
    def list_posts(self):
        if len(self.posts) == 0:
            print('게시판에 아직 작성된 글이 없습니다.')
            print('한 번 작성해보는 것은 어떨까요?')
            return

        page_from = (self.current_page - 1) * Board.POSTS_PER_PAGE
        page_to = self.current_page * Board.POSTS_PER_PAGE
        posts = [post for post in self.posts if post.is_not_deleted()]
        for post in posts[page_from : page_to]:
            print(post)

    @autosave
    def create_post(self):
        title = input('작성 > ')
        user_id = User.logged_in
        self.posts.insert(0, Post(title, user_id)) 
    
    @autosave
    def update_post(self):
        try:
            pid = int(input('몇 번 글을 수정할까요? '))
            _, post = self.search_post_by_id(pid)
            new_title = input('수정 > ')
            post.update(new_title)
        except (PostNotFoundError, IndexError, ValueError):
            input('잘못된 글 번호를 입력하셨습니다.')

    @autosave
    def delete_post(self):
        try:
            pid = int(input('몇 번 글을 지울까요? '))
            _, post = self.search_post_by_id(pid)
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
        if self.current_page > 1:
            self.current_page -= 1

    def go_next_page(self):
        if self.current_page * Board.POSTS_PER_PAGE < len(self.posts):
            self.current_page += 1