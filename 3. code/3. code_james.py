import os
import datetime
import math

class Board():
    def __init__(self):
          self.posts = list()
          self.count = 0
          self.page = 1
          self.post_per_pages = 15
   
    def list_posts(self):
        if self.posts == []:
            print('게시판에 아직 작성된 글이 없습니다.')
            print('한 번 작성해보는 것은 어떨까요?')
            return
        current_page = self.posts[self.post_per_pages*(self.page - 1):self.post_per_pages*(self.page)]
        for post in current_page:
            print('{:^8}| {:<60} | {}'.format(post[0], post[1], post[2]))
    def next_page(self):
        self.page += 1
        return           
    def previous_page(self):
        self.page -= 1
        return

    def create_post(self):
        print('----------------------------------------')
        title = input('>')
        self.count += 1
        now = datetime.datetime.now()
        nowDate = now.strftime('%Y-%m-%d %H:%M')
        self.posts.insert(0, [self.count, title, nowDate])
        print('{}번째 글이 성공적으로 작성되었습니다.'.format(len(self.posts)))
        input()

    def modify_post(self):
        print('----------------------------------------')
        for index, post in enumerate(self.posts):
            index = int(input('몇 번 글을 수정할까요 ? '))
            self.posts[index-1] = input('수정 >')
            return()
                      
    def delete_post(self):
        index = int(input('몇 번 글을 지울까요 ? '))
        del self.posts[index-1]

def print_greeting_message():
    greeting_message = '''
    본 프로그램은 광일공방에서 중고거래 사이트를 기웃기웃 거리던 광일이가
    어느날 삘이 꽂혀 '아! 여기가 돈 나오는 방석이다!' 생각하자마자 아주
    급하게 만들어낸 불안정한 중고거래 사이트입니다. 물론 아직은 허접한 
    게시판이지만 1000만 사용자를 꿈꾸는 광일이는 커다란 희망의 씨앗을 마음에
    품고서 오늘도 밤을 지새우며 코드를 작성합니다.
    '''
    print(greeting_message)
    input('프로그램을 시작하시려면 엔터키를 입력하세요...')


def feature_list():
    feature_list = '''
    1. 작성하기
    2. 수정하기
    3. 삭제하기
    4. 다음 페이지로
    5. 이전 페이지로
    '''
    print(feature_list)
    print('--------------------------------------------------------')

def clear():
    os.system("cls")

if __name__ == "__main__":
    print_greeting_message()
    board = Board()
    while True:
        clear()
        board.list_posts()
        feature_list()
        n = int(input(' >'))
        if n == 1 :
             board.create_post()
        elif n == 2:
             board.modify_post()
        elif n == 3:
             board.delete_post()
        elif n == 4:
             board.next_page()
        elif n == 5:
             board.previous_page()
