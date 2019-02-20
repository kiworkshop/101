import os
from board import Board  
from post import Post
from user_management import User_management

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == "__main__":
    print("본 프로그램은 광일공방에서 중고거래 사이트를 기웃거리던 광일이가 \n...\n중략\n...\n아나바다 철학이 담긴 프로그램을 밤을 지새우며 코드를 작성합니다.")
    input("프로그램을 시작하시려면 로그인하세요")
    user_management = User_management()
    try:
        user_management.load_users()
    except:
        pass
    signed_in_user_id = None    
    while signed_in_user_id == None:
        user_management.print_actions()
        signed_in_user_id = user_management.get_user_action()

    
    board = Board(signed_in_user_id)
    try:
        board.load_posts()
    except:
        input("파일을 불러오지 못했습니다.")

    while True:
        clear_screen()
        board.print_post_list()
        board.print_actions()
        board.get_user_action()