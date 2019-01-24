## main guard(line 21) 안 쪽에 위치하면 더 좋을 것 같습니다.
## 그리고 머릿말같은 문구이기에 함수로 만들어서 출력하면 어떨까요?
## 반복문 생성
## 글이 없을 경우 문자열 출력(index이 0인경우)
## 글작성 - X번째 글이 작성되었습니다.(index번째)
## 글번호. 글 내용 출력(index, contents)
## 변수명을 s와 같이 작성하면 이 변수가 언제 쓰이는지, 어떤 데이터를 담고 있는지
## 변수를 어떻게 사용해야하는지 등등 데이터의 특징이 담기지 않습니다.
## 이 경우 게시물(string)들을 담는 용도로 사용되니 posts라는 이름으로 작명하는 게 좋아보입니다.
## 이름을 짓는 행위는 어쩌면 프로그래밍의 처음이자 끝일 수도 있습니다.
## 가장 공들여서 작성해야하는 일 중에 하나이니 꼭 신경써서 지어주시기 바랍니다.
## 변수는 사용하는 지점 바로 앞에서 할당해주시기 바랍니다.
## 파이썬에서 반복문 for loop는 순회가능한(iterable) 자료구조를 받아서 순회합니다.

import os
import datetime

class Board():
     def __init__(self):
          self.posts = list()

     def list_posts(self):
          if len(self.posts) == 0:
               print
               ('''
               게시판에 아직 작성된 글이 없습니다.
               한 번 작성해보는 것은 어떨까요?
               ''')
               return
          
          ## for post in range posts: 와 같은 형식으로 활용하는 것이 일반적입니다.
          ##for i in range(0,index):
          ##   print('{}.'.format(i + 1),posts[i])
          for index, post in enumerate(reversed(self.posts)):
               post_no = index + 1
               now = datetime.datetime.now()
               nowDate = now.strftime('%Y-%m-%d %H:%M')
               print('{:^8}| {:<60} | {}'.format(post_no, post, nowDate))
                    
          
     def create_post(self):
          print('----------------------------------------')
          self.posts.append(input('> '))
          print('{}번째 글이 성공적으로 작성되었습니다.'.format(len(self.posts)))
          input()

## 안내문 출력
## 글번호 입력받아서 해당글 덮어쓰기
## self.posts[post_no] = input()
     def modify_post(self):
          print('----------------------------------------')
          for index, post in enumerate(self.posts):
               index = int(input('몇 번 글을 수정할까요 ? '))
               self.posts[index-1] = input('수정 >')
               return()


##          post_no = int(input('몇 번 글을 수정할까요 ? '))
##          self.posts(post_no) = input('수정 >')

                        
     def delete_post(self):
          index = int(input('몇 번 글을 지울까요 ? '))
          del self.posts[index-1]
## '=' 비교 연산자, '==' 대입연산자
## 파이썬 index는 0부터
          
##def clear_screen():
##    os.system('cls' if os.name == 'nt' else 'clear')

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


def print_supported_feature():
     feature_list = '''
     1. 작성하기
     2. 수정하기
     3. 삭제하기
     '''
     print(feature_list)
     print('--------------------------------------------------------')


if __name__ == "__main__":
##    clear_screen()
    print_greeting_message()
    board = Board()
    while True:
##        clear_screen()
        print_supported_feature()
        board.list_posts()
        n = int(input(' >'))
        if n == 1 :
             board.create_post()
        elif n == 2:
             board.modify_post()
        elif n == 3:
             board.delete_post()
