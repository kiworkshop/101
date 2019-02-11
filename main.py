import os
from BOARD import Board
from POST import Post
from USER import UserManager, User

def intro():
    greeting = '''
    본 프로그램은 광일공방에서 중고거래 사이트를 기웃기웃 거리던 광일이가
    어느날 삘이 꽂혀 '아! 여기가 돈 나오는 방석이다!' 생각하자마자
    아주 급하게 만들어낸 불안정한 중고거래 사이트입니다. 물론 아직은
    허접한 게시판이지만 1000만 사용자를 꿈꾸는 광일이는 커다란 희망의 씨앗을
    마음에 품고서 오늘도 밤을 지새우며 코드를 작성합니다.

    프로그램을 시작하려면 로그인하세요...'''
    print(greeting, end = '')
    input()
    clear_screen()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == "__main__":
    user_manager = UserManager()
    while UserManager.LOGINNED_USER == None:
        user_manager.print_actions()
        user_manager.execute_action()
    board = Board()
    while True :
        board.show_posts()
        board.show_actions()
        board.execute_action()
        clear_screen()