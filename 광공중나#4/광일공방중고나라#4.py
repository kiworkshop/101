import os
import sys
from board import Board  
from membership_manager import Membership_manager

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear') 

def greeting_messages():
    clear_screen()
    print("""
    본 프로그램은 광일공방에서 중고거래 사이트를 기웃기웃 거리던 광일이가 
    어느 날 삘이 꽃혀 '아! 여기가 돈 나오는 방석이다!' 생각하자마자 아주 
    급하게 만들어낸 불안정한 중고거래 사이트입니다. 물론 아직은 허접한 
    게시판이지만 1000만 사용자를 꿈꾸는 광일이는 커다란 희망의 씨앗을 마음에 
    품고서 오늘도 밤을 지새우며 코드를 작성합니다.""")
    print()
    input('프로그램을 시작하시려면 로그인하세요...')


if __name__ == '__main__':
    greeting_messages()
    membership_manager = Membership_manager()
    while True:
        clear_screen()
        membership_manager.menu()
        log_in_user_id = membership_manager.action_handler() # 로그인 성공한 유저가 없으면 None, 있으면 id 반환

        if log_in_user_id is not None:
            break

    board = Board(log_in_user_id)
    while True:
        clear_screen()
        board.check_existence_of_posts()
        board.print_actions()
        board.post_CRUD_handler()
