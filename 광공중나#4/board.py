import os
import csv
from post import Post

SAVE_FILE_PATH = './광일공방중고나라_게시판목록.csv'

def auto_save(func):
    # caller.save가 구현되지 않은 곳에 데코레이터가 붙은 경우에 대한 예외 처리
    def decorated(caller, *args, **kwargs):
        func(caller, *args, **kwargs)
        caller.save()
    return decorated

class Board():
    PAGINATION_SIZE = 15

    def __init__(self, user_id):
        self.user_id = user_id
        self.posts = list()
        self.actions = [self.create_post, self.update_post, self.delete_post, self.save, self.go_to_previous_page, self.go_to_next_page]
        self.current_page_num = 1
        self.load()

    @staticmethod
    def print_actions():
        print('-' * 100)
        print('1. 작성하기')
        print('2. 수정하기')
        print('3. 삭제하기')
        print('4. 저장하기')
        print('5. 이전 페이지로')
        print('6. 다음 페이지로')
        print('-' * 100)

    # iterate posts and print
    def show_posts(self):
        reversed_posts = list(reversed(self.posts)) 
        reversed_existed_posts = [post for post in reversed_posts if post.existence_state] # filter soft_deleted posts

        fromIdx = Board.PAGINATION_SIZE * (self.current_page_num - 1)
        toIdx = Board.PAGINATION_SIZE * self.current_page_num
        for post in reversed_existed_posts[fromIdx:toIdx]:
            print('{:^6} | {:60.60} | {:^10} | {}'.format(post.posting_num, post.posting_title, post.posting_user, post.posting_time))

    # check existence of post in posts and handle messages
    def check_existence_of_posts(self):
        if len(self.posts) == 0:
            print('게시판에 아직 작성된 글이 없습니다.')
            print('한 번 작성해 보는 것은 어떨까요?')
            return
        self.show_posts()

    def find_target_post(self, target_posting_num):
        target_post = None
        i = 0
        while target_post is None and i < len(self.posts):
            target_post = self.posts[i] if self.posts[i].posting_num == target_posting_num else None
            i += 1
        return target_post

    @auto_save
    def create_post(self):
        post = Post(posting_user = self.user_id)
        self.posts.append(post)
        print('{}번 글이 성공적으로 작성되었습니다.'.format(post.posting_num))

    @auto_save
    def update_post(self):
        if len(self.posts) == 0:
            raise Exception('현재 글이 없습니다.')

        update_idx = int(input('몇 번 글을 수정할까요? '))
        post_to_update = self.find_target_post(update_idx)
        if post_to_update is None or post_to_update.existence_state is False:
            raise Exception('수정할 해당 번호 글이 없습니다.')

        post_to_update.update_posting_title(self.user_id)
        
    @auto_save
    def delete_post(self):
        if len(self.posts) == 0:
            raise Exception('현재 글이 없습니다.')

        delete_idx = int(input('몇 번 글을 지울까요? '))
        post_to_delete = self.find_target_post(delete_idx)
        if post_to_delete is None or post_to_delete.existence_state is False:
            raise Exception('삭제할 해당 번호 글이 없습니다.')
        
        post_to_delete.soft_delete_post(self.user_id)

    def save(self):
        global SAVE_FILE_PATH

        f = open(SAVE_FILE_PATH, 'w', encoding='utf-8')
        for post in self.posts:
            print(post.to_csv(), file=f)
        f.close()
    
    def load(self):
        global SAVE_FILE_PATH
        if os.path.exists(SAVE_FILE_PATH) is False:
            return
        
        f = open(SAVE_FILE_PATH, 'r', encoding='utf-8')
        posts = f.readlines()
        for post in posts:
            self.posts.append(Post.from_csv(post))
        f.close()
        
    def go_to_previous_page(self):
        if self.current_page_num == 1:
            input('이전 페이지가 없습니다.')
            return
        self.current_page_num -= 1
    
    def go_to_next_page(self):
        if (self.current_page_num - 1) * Board.PAGINATION_SIZE < len(self.posts) <= self.current_page_num * Board.PAGINATION_SIZE:
            input('다음 페이지가 없습니다.')
            return
        self.current_page_num += 1

    # manage CRUD of posts
    def post_CRUD_handler(self):
        try:
            menuSel = int(input('> '))
            self.actions[menuSel - 1]()
            return
        except TypeError:
            input('잘못 입력하셨습니다. 올바른 번호를 선택하세요.')
        except IndexError:
            input('잘못 입력하셨습니다. 현재 글 번호를 맞게 입력하세요.')
        except Exception as e:
            input('잘못 입력하셨습니다.', e)
