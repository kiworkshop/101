import math
from POST import Post
from USER import User, UserManager
from SAVE import autosave, SAVE_PATH_POST

class PostNotFoundError(Exception):
    pass

class Board:
    POSTS_PER_PAGE = 15 

    def __init__(self):
        self.posts = list()       
        self.no_of_pages = 1                   
        self.current_page_no = 1 
        self.actions = [
            {
                "title" : "작성하기",
                "handler" : self.write_post 
            }, 
            { 
                "title" : "수정하기",
                "handler" : self.update_post
            },
            {
                "title" : "삭제하기",
                "handler" : self.delete_post
            }, 
            {  
                "title" : "저장하기",
                "handler" : self.save
            }, 
            {
                "title" : "이전페이지",
                "handler" : self.move_previous_page
            },
            {
                "title" : "다음페이지",
                "handler" : self.move_next_page
            }]
        try:
            self.load()              
        except:
            pass

    def save(self):
        global SAVE_PATH_POST
        f = open(SAVE_PATH_POST, 'w+')
        for post in self.posts:
            print(post.to_csv(), file = f)
        f.close()

    def load(self):
        global SAVE_PATH_POST
        f = open(SAVE_PATH_POST, 'r')
        posts = f.readlines()       
        for post in posts:
            self.posts.append(Post.from_csv(post)) 
        f.close()
       
    def show_posts(self):
        if self.posts == []:
            print('게시판에 아직 작성된 글이 없습니다.')
            print('한번 작성해보는 것은 어떨까요?')
            print('-' * 100)
            return
    
        self.posts_shown_list = list(filter(lambda x: x.post_shown_status == True, self.posts))
        # or self.posts_shown_list = [post for post in self.posts if post.post_shown_status ==True]
        self.no_of_pages = math.ceil( len(self.posts_shown_list) / Board.POSTS_PER_PAGE )      
       
        page = [post for index, post in enumerate(self.posts_shown_list) if Board.POSTS_PER_PAGE * (self.current_page_no - 1) <= index < Board.POSTS_PER_PAGE * self.current_page_no]
        for post in page:   
            print(post)
        print('-' * 100)

    def search_post_by_post_no(self, post_no):
        for post in self.posts:
            if post.has_post_no(post_no):
                return post
        raise PostNotFoundError

    @autosave
    def write_post(self):
        post_title = input('작성 >')
        self.posts.insert(0, Post(post_title, UserManager.LOGINNED_USER.user_id))
        self.current_page_no = 1 

    @autosave
    def update_post(self):        
        try:
            post_no = int(input('몇 번 글을 수정할까요?'))
            post = self.search_post_by_post_no(post_no)
            post.update_title()
        except (PostNotFoundError, ValueError, IndexError):
            print("잘못된 글 번호를 입력하셨습니다.")

    @autosave
    def delete_post(self):
        try:
            post_no = int(input('몇 번 글을 삭제할까요?'))
            post = self.search_post_by_post_no(post_no)
            post.change_shown_status()
        except (PostNotFoundError, ValueError, IndexError):
            print("잘못된 글 번호를 입력하셨습니다.")

    def move_previous_page(self):       
        self.current_page_no -= 1
        if self.current_page_no < 1:
            self.current_page_no = 1
            print("첫 페이지입니다.")

    def move_next_page(self):                  
        self.current_page_no += 1
        if self.current_page_no > self.no_of_pages:
            self.current_page_no = self.no_of_pages
            print("마지막 페이지입니다.")

    def show_actions(self):
        for index, action in enumerate(self.actions):
            print("{}. {}".format(index+1, action["title"]))
        print('-' * 100)

    def execute_action(self):
        try:
            action_no = int(input('>'))
            self.actions[action_no - 1]["handler"]()                       
        except (IndexError, ValueError):
            print("잘못된 입력입니다.")

        input('엔터를 누르세요.')