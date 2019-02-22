from time import gmtime, strftime
import os
import pickle
from Post import Post
from User import User


def autosave(func):
    def decorated(caller, *args, **kwargs):
        func(caller, *args, **kwargs)
        caller.save()

    return decorated


class Board():
    posts_per_page = 15

    def __init__(self):
        # 게시글 데이터 세팅
        try:
            self.load()
            Post.index = self.posts[0].index + 1
        except:
            self.posts = []

        # 유저 데이터 세팅
        try:
            self.load_user_data()
        except:
            self.user_data = []

        # 로그인 접속 유저 정보
        self.user_name = str
        self.user_index = int

        self.intro()

        self.login_action = [self.login, self.join]
        self.user_action = [self.write, self.edit, self.delete, self.save, self.previous_page, self.next_page]
        self.page_num = 1

    #######################
    ######## 로그인 ########
    #######################

    def login_menu(self):
        print("--------------------------------------------------")
        print("1. 로그인")
        print("2. 회원가입")
        print("--------------------------------------------------")
        select_menu_num = int(input("> "))
        return select_menu_num

    def login_act(self, select_menu_num):
        self.login_action[select_menu_num - 1]()

    def login(self):
        id = input("아이디 : ")
        password = input("비밀번호 : ")
        try:
            self.user_index = self.user_find(id, password)
            print("로그인 성공 : 환영합니다 {}님!".format(id))
            self.user_name = id

        except:
            print("로그인에 실패하셨습니다")
            select_menu_num = self.login_menu()
            self.login_act(select_menu_num)

    def join(self):
        id = input("아이디 : ")
        password = input("비밀번호 : ")
        self.user_data.append(User(id, password))
        print("로그인 성공 : 환영합니다 {}님!".format(id))
        self.user_index = self.user_find(id, password)
        self.user_name = id
        self.save_user_data()

    def user_find(self, id, password):
        for user_index, user in enumerate(self.user_data):
            if (user.id == id) & (user.password == password):
                return user_index

    def save_user_data(self):
        pickle.dump(self.user_data, open("user_data.pickle", "wb"))

    def load_user_data(self):
        self.user_data = pickle.load(open("user_data.pickle", "rb"))

    #####################
    ######## 시작 #######
    #####################

    def intro(self):
        print("""본 프로그램은 광일공방에서 중고거래 사이트를 기웃기웃 거리던
              광일이가 어느날 삘이 꽂혀 '아! 여기가 돈 나오는 방석이다!' 
              생각하자마자 아주 급하게 만들어낸 불안정한 중고거래 사이트입니다.
              물론 아직은 허접한 게시판이지만 1000만 사용자를 꿈꾸는 광일이는 
              커다란 희망의 씨앗을 마음에 품고서 오늘도 밤을 지새우며 코드를 작성합니다.""")

        n = input('프로그램을 시작하시려면 로그인하세요.')
        if n != '':
            print("프로그램을 종료합니다")
            exit()

    #######################
    ####### 메인메뉴 #######
    #######################

    def main_menu(self):
        print("--------------------------------------------------")
        print("1. 작성하기")
        print("2. 수정하기")
        print("3. 삭제하기")
        print("4. 저장하기")
        print("5. 이전 페이지로")
        print("6. 다음 페이지로")
        print("--------------------------------------------------")
        select_menu_num = int(input("> "))
        return select_menu_num

    def show(self):
        if len(self.posts) == 0:
            print("게시판에 아직 작성된 글이 없습니다.")
            print("한번 작성해보는것은 어떨까요?")
            print("--------------------------------------------------")
            return

        page_from = (self.page_num - 1) * Board.posts_per_page
        page_to = self.page_num * Board.posts_per_page
        for post in self.posts[page_from: page_to]:
            post.show()
        print("--------------------------------------------------")

    def user_act(self, select_menu_num):
        self.user_action[select_menu_num - 1]()

    def next_page(self):
        if self.page_num > 1:
            self.page_num -= 1

    def previous_page(self):
        if self.page_num * Board.posts_per_page < len(self.posts):
            self.page_num += 1

    def user_authorization(self, post):
        if self.user_data[self.user_index].id == post.user_name:
            return
        print("게시글 접근 권한이 없습니다.")
        return

    @autosave
    def write(self):
        context = input("작성 > ")
        self.posts.insert(0, Post(context, self.user_name))
        print(str(self.posts[len(self.posts) - 1].index) + "번째 글이 성공적으로 작성되었습니다.")

    @autosave
    def edit(self):
        try:
            revise_num = int(input("몇 번 글을 수정할까요? "))
            _, post = self.find(revise_num)
            self.user_authorization(post)
            revise_context = input("수정 > ")
            post.context = revise_context
        except:
            print("잘못된 게시글 번호를 입력하셨습니다.")

    @autosave
    def delete(self):
        try:
            delete_num = int(input("몇 번 글을 지울까요? "))
            index, post = self.find(delete_num)
            self.user_authorization(post)
            self.posts[index].removed = True
        except:
            print("잘못된 게시글 번호를 입력하셨습니다.")

    def find(self, num):
        for index, post in enumerate(self.posts):
            if post.index == num:
                return index, post

    def load(self):
        self.posts = pickle.load(open("posts.pickle", "rb"))

    def save(self):
        pickle.dump(self.posts, open("posts.pickle", "wb"))


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


if __name__ == "__main__":
    clear_screen()
    board = Board()

    select_menu_num = board.login_menu()
    board.login_act(select_menu_num)

    while True:
        clear_screen()
        board.show()
        select_menu_num = board.main_menu()
        board.user_act(select_menu_num)