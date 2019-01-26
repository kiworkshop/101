import datetime
import csv
import os

class Board():
    def __init__(self):
        self.posts = []
        self.actions = [self.add_post, self.update_post, self.delete_post, self.go_to_previous_page, self.go_to_next_page]
        self.page_index = 1
        self.posts_per_page = 15
        

    @staticmethod 
    def print_actions(): 
        print('---------------------------------------')
        print('1. 작성하기')
        print('2. 수정하기')
        print('3. 삭제하기')
        # print('4. 저장하기')
        print('4. 이전 페이지로')
        print('5. 다음 페이지로')
        print('---------------------------------------')

    def print_post_list(self):
        if self.posts == []:
            print("작성된 판매게시글이 없습니다.")
            print("회원님이 한 번 작성해보시는 것이 어떨까요?")
            return

        self.posts.sort(key=lambda list:list[0], reverse=True)

        paged_posts = self.posts[self.posts_per_page*(self.page_index-1):self.posts_per_page*self.page_index]

        for post in paged_posts: # [FIX] 포맷 padding 제대로 출력안됨. 들쑥날쑥
            print('{:^8} | {:<60} | {}'.format(post[0], post[1], post[2]))

        page_length = self.get_page_length()
        print('Page: {}'.format(str(self.page_index) + '/' + str(page_length)))

    def get_user_action(self):
        try:
            user_action_no = int(input('> '))
        except:
            print('잘못된 입력입니다.')
            input()    
            return  
        if user_action_no >0 and user_action_no <= len(self.actions):
            self.actions[user_action_no - 1]()
            return  
        print('잘못된 입력입니다.')

    def save_posts_decorator(func):
        def wrapper(self):
            func(self)
            with open ('중고나라 데이터.csv', 'w', encoding='utf8', newline='') as save_data:
                posts_write = csv.writer(save_data)
                posts_write.writerows(self.posts)
                input('저장이 완료되었습니다')
        return wrapper

    @save_posts_decorator
    def add_post(self):
        if self.posts == []:
            post_no = 1
        if self.posts != []:
            post_no = self.posts[0][0] + 1
        
        post_title = input('내용> ')
        
        post_insert_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.posts.append(list([post_no, post_title, post_insert_time]))
    
    @save_posts_decorator
    def update_post(self):
        try:
            target_post_no = int(input('몇 번 글을 수정할까요? '))
        except:
            input('잘못된 입력입니다')
            return
        
        try:
            target_post_index = [index for index, post in enumerate(self.posts) if post[0] == target_post_no][0]
        except:
            input('잘못된 입력입니다')
            return
        self.posts[target_post_index][1] = input('수정할 내용을 입력해주세요 >')
        print(str(target_post_no) +'번 글이 수정되었습니다')
    
    @save_posts_decorator
    def delete_post(self):
        try:
            target_post_no = int(input('몇 번 글을 삭제할까요? '))
        except:
            input('잘못된 입력입니다')
            return     
        try:
            target_post_index = [index for index, post in enumerate(self.posts) if post[0] == target_post_no][0]
        except:
            input('잘못된 입력입니다')
            return
        del(self.posts[target_post_index])
        print(str(target_post_no) +'번 글이 삭제되었습니다')

    # def save_posts(self):
    #     with open ('중고나라 데이터.csv', 'w', encoding='utf8', newline='') as save_data:
    #         posts_write = csv.writer(save_data)
    #         posts_write.writerows(self.posts)
    #     input('저장이 완료되었습니다')
    
    def load_posts(self):
        with open ('중고나라 데이터.csv', 'r', encoding='utf8') as load_data:
            posts_read = csv.reader(load_data)
            posts_read = [[int(post[0]), post[1], post[2]] for post in posts_read]
            self.posts = list(posts_read)

    def go_to_next_page(self):
        page_length = self.get_page_length()
        page_index_to_go = self.page_index + 1
        if page_index_to_go > page_length:
            input("가장 끝 페이지입니다.")
            return
        self.page_index = page_index_to_go

    def go_to_previous_page(self):
        page_index_to_go = self.page_index - 1
        if page_index_to_go < 1:
            input("가장 앞 페이지입니다.")
            return
        self.page_index = page_index_to_go
    
    def get_page_length(self):
        return len(self.posts)//(self.posts_per_page) + 1
    
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == "__main__":
    print("본 프로그램은 광일공방에서 중고거래 사이트를 기웃거리던 광일이가 \n...\n중략\n...\n아나바다 철학이 담긴 프로그램을 밤을 지새우며 코드를 작성합니다.")
    input("프로그램을 시작하시려면 엔터키를 입력하세요...")
    board = Board()
    try:
        board.load_posts()
    except:
        print("파일을 불러오지 못했습니다.")

    while True:
        clear_screen()
        board.print_post_list()
        board.print_actions()
        board.get_user_action()
                