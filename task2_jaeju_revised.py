import os

class Board():

    def __init__(self):
        self.posts = list()
        self.actions = [self.write_post, self.update_post, self.delete_post]

    def show_posts(self):
        if self.posts == []:
            print('게시판에 아직 작성된 글이 없습니다.')
            print('한번 작성해보는 것은 어떨까요?')
            return

        for index, post in enumerate(self.posts):
            print('{글번호}. {글내용}'.format(글번호 = str(index + 1), 글내용 = post))
        print('-------------------------------------')

    def write_post(self):
        post = input('작성 >')
        self.posts.append(post)

    def update_post(self):
        try:
            post_no = int(input('몇 번 글을 수정할까요?'))
            if post_no < 1 or post_no > len(self.posts):
                raise IndexError
            updated_post = input('수정 >')
            self.posts[post_no - 1] = updated_post
        except ValueError:
            print('숫자를 입력해주세요')
        except IndexError:
            print('범위 밖의 숫자를 입력하셨습니다.')

    def delete_post(self):
        try:
            post_no = int(input('몇 번 글을 지울까요?'))
            if post_no < 1 or post_no > len(self.posts):
                raise IndexError
            del self.posts[post_no -1]
        except ValueError:
            print('숫자를 입력해주세요')
        except IndexError:
            print('범위 밖의 숫자를 입력하셨습니다.')

    def list_actions(self):
        print('1. 작성하기')
        print('2. 수정하기')
        print('3. 삭제하기')
        print('-------------------------------------')

    def execute_action(self):
        try:
            action_no = int(input('>'))
            if  action_no < 1 or action_no > len(self.actions):
                raise IndexError
            self.actions[action_no - 1]()
            print('-------------------------------------')
        except ValueError:
            print('숫자를 입력하세요')
        except IndexError:
            print('범위 밖의 숫자를 입력하셨습니다.')

        input('엔터를 누르세요.')

    def write_file(self):
        with open('list.txt', 'w') as f:
            f.writelines(self.posts + '\n')

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

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

if __name__ == "__main__":
    intro()
    board = Board()
    while True :
        board.show_posts()
        board.list_actions()
        board.execute_action()
        clear_screen()
