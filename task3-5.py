import os
import csv
import datetime
import math

class Post:
    count = 0   # 포스트 자체 내에서 count 세주기. 의미 없지만, 일단 넣었습니다.
    
    def __init__(self, post_no, title, time, post_shown_status):   # 속성으로, 포스트 넘버, 제목, 작성 시간, 노출 여부를 받음
        Post.count += 1                     # 인스턴스 생성시마다 실행될 때마다 1 추가
        self.post_no = post_no             
        self.post_title = title
        self.post_time = time
        self.post_shown_status = post_shown_status

    @staticmethod
    def check_shown_status_decorator(func):
        def wrapper(self):
            try:
                if self.post_shown_status == "shown_denied":       # self.post_shown_status(노출 여부)가 shown_denied의 값이면 '존재하지 않는 게시글' 에러 발생
                    raise Exception
            except:
                print("존재하지 않는 게시글입니다.")
            func(self)
        return wrapper    

    @check_shown_status_decorator.__func__
    def update_title(self, updated_title):              # update_tilte로 title 수정 메서드 생성
        try:
            if self.post_shown_status == "shown_denied":       # self.post_shown_status(노출 여부)가 shown_denied의 값이면 '존재하지 않는 게시글' 에러 발생
                raise Exception
        except:
            print("존재하지 않는 게시글입니다.")
        if self.post_shown_status == "shown_permitted":        # self.post_shown_status(노출 여부)가 shown_permitted의 값이면, 제목 수정
            self.post_title = updated_title

    @check_shown_status_decorator.__func__
    def change_shown_status(self):                  # change_shown_status로 post_shown_status를 변경하는 메서드 생성
        try:
            if self.post_shown_status == "shown_denied":       # self.post_shown_status(노출 여부)가 shown_denied의 값이면 '존재하지 않는 게시글' 에러 발생
                raise Exception
        except:
            print("존재하지 않는 게시글입니다.")
        if self.post_shown_status == "shown_permitted":        # self.post_shown_status(노출 여부)가 shown_permitted의 값이면, 노출 여부 shown_denied로 변경
            self.post_shown_status = "shown_denied"

class Board:
    POSTS_PER_PAGE = 15     # 페이지당 게시글 수 저장

    def __init__(self):
        self.posts = list()       # Post 객체의 인스턴스들을 담을 리스트 생성
        self.posts_shown_list = list()          # 인스턴스 객체들 중에서 post_shown_status 값이 shown_permitted인 인스턴스를 담을 리스트 생성
        self.no_of_posts = 0                     # the number of posts로 포스트의 개수
        self.no_of_pages = 1                     # the number of pages로 총 페이지의 개수
        self.current_page_no = 1                # 현재 머물고 있는 페이지 no
        self.actions = [self.write_post, self.update_post, self.delete_post, self.save_posts, self.move_previous_page, self.move_next_page]
        self.load_data()                        # board 인스턴스가 생성될 때 데이터 로드

    def load_data(self):
        try:
            csvfile = open('posts.csv', 'r')
            readers = csv.readers(csvfile)
            for row in readers:
                globals()["post" + str(row[0])] = Post(row[0], row[1], row[2], row[3])  # post1, post2, post3... 과 같이 인스턴스 생성, row[0] = post_no, row[1] = post_title, row[2] = post_time, row[3] = post_time
                self.posts.append(globals()["post" + row[0]])     # self.posts에 인스턴스 추가
            self.no_of_posts = len(self.posts)            # 전체 포스트의 개수 할당
            csvfile.close()
        except:
            pass

    def show_posts(self):
        if self.posts == []:
            print('게시판에 아직 작성된 글이 없습니다.')
            print('한번 작성해보는 것은 어떨까요?')
            print('-------------------------------------')
            return
       
        self.posts_shown_list = [post for post in self.posts if post.post_shown_status == "shown_permitted"]     # 각 포스트마다 post_shown_status의 값이 shown_permitted인 값의 리스트 생성
        self.no_of_pages = math.ceil( len(self.posts_shown_list) / Board.POSTS_PER_PAGE )       # self.posts_shown_list를 페이지당 게시글 수로 나눠서 the number of pages 총 페이지 수 생성
       
        page = [post for index, post in enumerate(self.posts_shown_list) if Board.POSTS_PER_PAGE * (self.current_page_no - 1) <= index < Board.POSTS_PER_PAGE * self.current_page_no]     # self.posts_shown_list에서 Board.posts_per_page와 self.current_page_no로 인덱스 설정
        
        for post in page:       # self.current_page에 해당하는 페이지들에서 post를 하나씩 꺼내며 프린트
            print('{글번호:^8} | {글내용:60.60} | {작성일}'.format(글번호 = post.post_no, 글내용 = post.post_title, 작성일 = post.post_time))
        
        print('-------------------------------------')

    def save_posts(self):
        csvfile = open('posts.csv', 'w')
        writer = csv.writer(csvfile)
        list_for_save = list()
        for post in self.posts:       # 세이브를 위한 리스트를 만들어서, post_no, post_title, post_time, post_shown_status의 값을 저장.
            list_for_save.append([post.post_no, post.post_title, post.post_time, post.post_shown_status])
        writer.writerows(list_for_save)
        csvfile.close()    
    
    @staticmethod
    def auto_save_posts_decorator(func):            # 자동 저장용 staticmethod, 함수 실행 후 self.save_posts() 실행.
        def wrapper(self):
            func(self)
            self.save_posts()
        return wrapper

    @auto_save_posts_decorator.__func__
    def write_post(self):
        post_title = input('작성 >')            # post_title 받음
        written_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')       # 작성 시간 생성
        self.no_of_posts += 1           # post 개수 하나 추가
        globals()["post" + str(self.no_of_posts)] = Post(post_no = self.no_of_posts, title = post_title, time = written_time, post_shown_status = "shown_permitted")     # post1, post2 ...의 post 인스턴스 생성. no_of_posts로 post_no 설정, post_title, written_time, shown_permitted로 속성값 생성
        self.posts.insert(0, globals()["post" + str(self.no_of_posts)])   # 생성된 포스트 인스턴스를 self.posts_instance_list의 맨 앞에 추가.
        self.current_page_no = 1        # 작성시에는 최근글을 보여주어야 하기 때문에 현재 페이지를 1로 설정

    @auto_save_posts_decorator.__func__
    def update_post(self):
        try:
            post_no = int(input('몇 번 글을 수정할까요?'))
            if post_no < 1 or post_no > len(self.posts):
                raise IndexError
            updated_post = input('수정 >')
            self.posts[ len(self.posts) - post_no ].update_title(updated_post)  # 수정할 글 받아서 len(self.posts_instance_list) - post_no(=> index)에 update_tilte메서드 실행.
        except ValueError:
            print('숫자를 입력해주세요')
        except IndexError:
            print('해당하지 않는 숫자를 입력하셨습니다.')

    @auto_save_posts_decorator.__func__  
    def delete_post(self):
        try:
            post_no = int(input('몇 번 글을 지울까요?'))
            if post_no < 1 or post_no > len(self.posts):
                raise IndexError
            self.posts[ len(self.posts) - post_no ].change_shown_status()     # 삭제할 글 받아서 len(self.posts_instance_list) - post_no(=> index)에 change_shown_status메서드 실행
        except ValueError:
            print('숫자를 입력해주세요')
        except IndexError:
            print('해당하지 않는 숫자를 입력하셨습니다.')

    def move_previous_page(self):               # move_previous_page로 current_page_no 수정.
        self.current_page_no -= 1
        if self.current_page_no < 1:            # 1보다 작을 경우 1로 유지
            self.current_page_no = 1

    def move_next_page(self):                   # move_next_page로 current_page_no 수정.
        self.current_page_no += 1
        if self.current_page_no > self.no_of_pages:     # 전체 페이지 수보다 클 경우. 전체 페이지 수(마지막 페이지)로 유지.
            self.current_page_no = self.no_of_pages

    def list_actions(self):
        print('1. 작성하기')
        print('2. 수정하기')
        print('3. 삭제하기')
        print('4. 저장하기')
        print('5. 이전페이지')
        print('6. 다음페이지')
        print('-------------------------------------')

    def execute_action(self):
        try:
            action_no = int(input('>'))
            if  action_no < 1 or action_no > len(self.actions):
                raise IndexError
            self.actions[action_no - 1]()                           # action_no 받아서 인덱스로 해당 메서드 실행.
            print('-------------------------------------')
        except ValueError:
            print('숫자를 입력하세요')
        except IndexError:
            print('범위 밖의 숫자를 입력하셨습니다.')

        input('엔터를 누르세요.')
        clear_screen()

def intro():
    greeting = '''
    본 프로그램은 광일공방에서 중고거래 사이트를 기웃기웃 거리던 광일이가
    어느날 삘이 꽂혀 '아! 여기가 돈 나오는 방석이다!' 생각하자마자
    아주 급하게 만들어낸 불안정한 중고거래 사이트입니다. 물론 아직은
    허접한 게시판이지만 1000만 사용자를 꿈꾸는 광일이는 커다란 희망의 씨앗을
    마음에 품고서 오늘도 밤을 지새우며 코드를 작성합니다.

    프로그램을 시작하려면 엔터키를 입력하세요...'''
    print(greeting, end = '')
    input()
    clear_screen()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == "__main__":
    intro()
    board = Board()
    while True :
        board.show_posts()
        board.list_actions()
        board.execute_action()
