from time import gmtime, strftime
import os
import pandas as pd
import pickle

class Post() :
    def __init__(self):
        try:
            self.load()
        except:
            self.posts = []
            self.index = 0

    def load(self):
        self.posts = []
        load_data = pd.read_csv("posts.csv", index_col= 0).to_dict()
        for i in range(len(load_data["post_number"])) :
            post_data = {}
            post_data["post_number"] = load_data["post_number"][i]
            post_data["post"] = load_data["post"][i]
            post_data["user_name"] = load_data["user_name"][i]
            post_data["time"] = load_data["time"][i]
            self.posts.append(post_data)

        f = open("index.pickle", "rb")
        self.index = pickle.load(f)

class Board():
    def __init__(self, posts, index):
        self.posts = posts
        self.index = index

        self.name = self.create_user()
        self.intro(self.name)
        self.user_action = [self.write, self.edit, self.delete, self.save, self.previous_page, self.next_page]
        self.page_num = 1

    def create_user(self):
        return input("사용자 이름을 입력하세요: ")

    def intro(self, name):
        print("""본 프로그램은 광일공방에서 중고거래 사이트를 기웃기웃 거리던
              {}이가 어느날 삘이 꽂혀 '아! 여기가 돈 나오는 방석이다!' 
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
        print("4. 저장하기")
        print("5. 이전 페이지로")
        print("6. 다음 페이지로")
        print("--------------------------------------------------")
        select_menu_num = int(input("> "))
        return select_menu_num

    def show(self) :
        if len(self.posts) == 0 :
            print("게시판에 아직 작성된 글이 없습니다.")
            print("한번 작성해보는것은 어떨까요?")
            print("--------------------------------------------------")
            return

        self.sort()

        i = 15*(self.page_num-1)
        while (len(self.posts) > i+1) and ((self.page_num * 15 -1) >= i):
            i += 1
            print("{:^8}| {:60}  | 작성자 : {} | 작성시간 : {} |".format(self.posts[i]["post_number"], self.posts[i]["post"], self.posts[i]["user_name"], self.posts[i]["time"]))
        print("--------------------------------------------------")

    def next_page(self):
        if (self.page_num*15-1) < len(self.posts) :
            self.page_num += 1


    def previous_page(self):
        if self.page_num > 1 :
            self.page_num -=1

    def sort(self):
        sorted_posts = pd.DataFrame(self.posts)
        sorted_posts.index = sorted_posts["post_number"]
        sorted_posts = sorted_posts.sort_index(ascending=False)
        sorted_index = sorted_posts.index
        sorted_posts = sorted_posts.to_dict()
        self.posts = []
        for i in sorted_index :
            post_data = {}
            post_data["post_number"] = sorted_posts["post_number"][i]
            post_data["post"] = sorted_posts["post"][i]
            post_data["user_name"] = sorted_posts["user_name"][i]
            post_data["time"] = sorted_posts["time"][i]
            self.posts.append(post_data)

    def write(self) :
        self.index += 1
        post_data = {}
        post_data["post_number"] = self.index
        post_data["post"] = input("작성 > ")
        post_data["user_name"] = self.name
        post_data["time"] = strftime("%Y-%m-%d %H:%M", gmtime())
        self.posts.append(post_data)
        print(str(self.index) + "번째 글이 성공적으로 작성되었습니다.")
        self.save()

    def edit(self) :
        try :
            revise_num = int(input("몇 번 글을 수정할까요? "))
            revise_post = input("수정 > ")
            self.posts[self.find(revise_num)]["post"] = revise_post
            self.save()
        except :
            print("잘못된 게시글 번호를 입력하셨습니다.")

    def delete(self):
        try :
            delete_num = int(input("몇 번 글을 지울까요? "))
            del self.posts[self.find(delete_num)]
            self.save()
        except :
            print("잘못된 게시글 번호를 입력하셨습니다.")

    def find(self, num):
        post_number_list = []
        for i in range(len(self.posts)):
            post_number_list = post_number_list + [(self.posts[i]["post_number"])]
        return(post_number_list.index(num))

    def action(self, select_menu_num):
        try :
            self.user_action[select_menu_num-1]()
        except :
            print("올바른 메뉴번호를 입력해주세요")

    def save(self):
        pd.DataFrame(self.posts).to_csv("posts.csv")
        pickle.dump(self.index, open("index.pickle", "wb"))


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == "__main__" :
    clear_screen()
    post = Post()
    board = Board(post.posts, post.index)
    while True :
        clear_screen()
        board.show()
        select_menu_num = board.main_menu()
        board.action(select_menu_num)
