import pickle
from time import gmtime, strftime
import os

class OldNara() :
    def __init__(self):
        try :
            f = open("posts.pickle", "rb")
            self.posts = pickle.load(f)
        except :
            self.posts = list()

        self.name = self.create_user()
        self.intro(self.name)
        self.user_action = [self.write, self.edit, self.delete]

    def create_user(self):
        return input("사용자 이름을 입력하세요: ")

    def intro(self, name):
        print("""본 프로그램은 광일공방에서 중고거래 사이트를 기웃기웃 거리던
              진영이가 어느날 삘이 꽂혀 '아! 여기가 돈 나오는 방석이다!' 
              생각하자마자 아주 급하게 만들어낸 불안정한 중고거래 사이트입니다.
              물론 아직은 허접한 게시판이지만 1000만 사용자를 꿈꾸는 {}이는 
              커다란 희망의 씨앗을 마음에 품고서 오늘도 밤을 지새우며 코드를 작성합니다.""".format(name, name))

        n = input('프로그램을 시작하시려면 엔터키를 입력하세요....')
        if n != '':
            print("프로그램을 종료합니다")
            exit()

    def main_menu(self):
        print("--------------------------------------------------")
        print("1. 작성하기")
        print("2. 수정하기")
        print("3. 삭제하기")
        print("--------------------------------------------------")
        select_menu_num = int(input("> "))
        return select_menu_num


    def show(self) :
        if len(self.posts) == 0 :
            print("게시판에 아직 작성된 글이 없습니다.")
            print("한번 작성해보는것은 어떨까요?")
            print("--------------------------------------------------")
            return

        for index, post in enumerate(self.posts) :
            print("{}. {}  | 작성자 : {} | 작성시간 : {} |".format(index+1, post["post"], post["user_name"], post["time"]))
        print("--------------------------------------------------")


    def write(self) :
        post_data = {}
        post_data["post"] = input("작성 > ")
        post_data["user_name"] = self.name
        post_data["time"] = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        self.posts.append(post_data)
        print(str(len(self.posts)) + "번째 글이 성공적으로 작성되었습니다.")
        pickle.dump(self.posts, open("posts.pickle", "wb"))


    def edit(self) :
        try :
            revise_num = int(input("몇 번 글을 수정할까요? "))
            revise_post = input("수정 > ")
            self.posts[revise_num-1]["post"] = revise_post
            pickle.dump(self.posts, open("posts.pickle", "wb"))
        except :
            print("잘못된 게시글 번호를 입력하셨습니다.")


    def delete(self):
        try :
            delete_num = int(input("몇 번 글을 지울까요? "))
            del self.posts[delete_num-1]
            pickle.dump(self.posts, open("posts.pickle", "wb"))
        except :
            print("잘못된 게시글 번호를 입력하셨습니다.")


    def action(self, select_menu_num):
        try :
            self.user_action[select_menu_num-1]()
        except :
            print("올바른 메뉴번호를 입력해주세요")

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == "__main__" :
    old = OldNara()
    while True :
        old.show()
        select_menu_num = old.main_menu()
        old.action(select_menu_num)
