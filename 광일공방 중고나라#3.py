import os
import csv
import datetime

class Post:
    def __init__(self, *post):
        self.post_no = post[0]
        self.post_content = post[1]
        self.post_time = post[2]
        self.delete_at = post[3]

    def update_content(self, new_content):
        self.post_content = new_content

    def delete_content(self):
        self.delete_at = 'DELETE'

    def get_data(self):
        return [self.post_no,self.post_content,self.post_time,self.delete_at]

class Board:
    def __init__(self):
        self.post = list()
        self.load_post()
        self.actions = [self.wrtie_post,self.update_post,self.delete_post,self.save_post,self.prev_page,self.next_page]
        self.PAGE_NUMBER_RANGE = 15
        self.page_no = 0
    
    class auto_save:
        def __call__(self, func):
            def wrapped(*args, **kwargs):
                changed_post = func(*args)
                file = open('post.csv', 'w', encoding='euc_kr',newline='')
                post_data_writer = csv.writer(file)
                for post in changed_post:
                    post_data_writer.writerow(post.get_data())
                file.close()
                return changed_post
            return wrapped

    @auto_save()            
    def wrtie_post(self):
        new_post = [len(self.post) + 1, input('작성해주세요:'), self.calculate_current_time(),'TRUE']
        globals()['post{}'.format(new_post[0])] = Post(*new_post)
        self.post.append(globals()['post{}'.format(new_post[0])])
        return self.post

    def load_post(self):
        file = open('post.csv', 'r', encoding = 'euc_kr')
        post_data_reader = csv.reader(file)#네이밍 다시
        for post in post_data_reader:
            globals()['post{}'.format(post[0])]= Post(*post)
            self.post.append(globals()['post{}'.format(post[0])])
        file.close()

    def is_undeleted(self, undeleted_post, post):
        if post.delete_at == 'TRUE':
            undeleted_post.append(post)

    def get_undeleted_post(self):
        self.undeleted_post = list()
        for post in self.post:
            self.is_undeleted(self.undeleted_post, post)

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def calculate_current_time(self):
        date_time = datetime.datetime.now()
        return date_time.strftime("%Y-%m-%d %H:%M")

    @auto_save()
    def update_post(self):
        try:
            update_post_no = input('몇 번 글을 수정 할까요?') 
            if not globals()['post{}'.format(update_post_no)] in self.undeleted_post:
                raise Exception('글 목록에 없습니다.')
            globals()['post{}'.format(update_post_no)].update_content(input('수정:')) 
        except KeyError:#에러는 1. 키값에 없거나 2. 보관한 글에 없거나 
            print('범위 밖의 값을 입력하였습니다..')
            input('엔터를 누르세요.')
        except Exception as e:
            print(e)
            input('엔터를 누르세요.')
        return self.post

    @auto_save()
    def delete_post(self):
        try:
            delete_post_no = input('몇 번 글을 삭제 할까요?') 
            if not globals()['post{}'.format(delete_post_no)] in self.undeleted_post:
                raise Exception('글 목록에 없습니다.') 
            globals()['post{}'.format(delete_post_no)].delete_content()
        except KeyError:
            print('범위 밖의 값을 입력하였습니다..')
            input('엔터를 누르세요.')
        except Exception as e:
            print(e)
            input('엔터를 누르세요.')
        return self.post

    def save_post(self):
        file = open('post.csv', 'w', encoding='euc_kr',newline='')
        post_data_writer = csv.writer(file)
        for post in self.post:
            post_data_writer.writerow(post.get_data())
        file.close()
            
    def prev_page(self):
        if self.page_no == 0 :
            return
        self.page_no = self.page_no - 1

    def next_page(self):
        if self.page_no == (len(self.undeleted_post) - 1) // self.PAGE_NUMBER_RANGE:
            return
        self.page_no = self.page_no + 1

    def get_current_page_post(self): 
        self.get_undeleted_post()
        self.current_page_post = list()
        post_index = -1 - self.page_no * self.PAGE_NUMBER_RANGE
        while post_index >= -len(self.undeleted_post) and len(self.current_page_post) < self.PAGE_NUMBER_RANGE:
            self.current_page_post.append(self.undeleted_post[post_index])
            post_index = post_index - 1 
        
    @staticmethod
    def display_intro():
        print('본 프로그램은 중고거래 사이트를 만들기 위한 게시판 프로그램입니다.')
        input('프로그램을 시작하시려면 엔터키를 입력하세요...')
        os.system('cls')
    
    def display_post_page(self):
        self.get_current_page_post()
        for post in self.current_page_post:
            print('{:^8}|{:<60}|{}'.format(post.post_no,post.post_content,post.post_time))

    def display_actions(self):
        print('------------------------------------페이지 목록------------------------------------')
        print('1. 작성하기')
        print('2. 수정하기')
        print('3. 삭제하기')
        print('4. 저장하기')
        print('5. 이전 페이지')
        print('6. 다음 페이지')
        print('----------------------------------------------------------------------------------')

    def execute_action(self):
        try:
            action_no = int(input('번호를 입력하세요:'))
            self.actions[action_no - 1]()
        except ValueError:
            print('숫자를 입력하셔야 합니다.')
            input('엔터를 누르고 다시 입력해주세요.')
        except IndexError:
            print('범위를 벗어났습니다.')
            input('엔터를 누르고 다시 입력해주세요.')
            

if __name__ == "__main__":
    Board.display_intro()
    board = Board()
    while True:
        board.clear_screen()
        board.display_post_page()
        board.display_actions()
        board.execute_action()
        