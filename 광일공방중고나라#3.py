import csv
from datetime import datetime
import os
import sys

class Post():
    current_posting_num = 0

    def __init__(self, posting_title):
        self.posting_num = Post.current_posting_num + 1
        Post.current_posting_num += 1 
        self.posting_title = posting_title
        self.posting_time = datetime.now().strftime('%Y-%m-%d %H:%M')

class Auto_save_decorator():
    def __init__(self, function):
        self.function = function
    
    def __call__(self, *args, **kwargs):
        result = self.function(*args, **kwargs)
        ## 여기서 board 인스턴스의 save_post()를 호출하고 싶었는데 뜻대로 되질 않네요. 인스턴스를 이 클래스로 어떻게 끌고들어와야할지...
        ## save_post()를 @classmethod로 지정해야하나? 싶기도 했는데 내부에서 self.posts를 사용해서 그럴수도 없고ㅠ
        return result
        

class Board():
    current_page_num = 1

    def __init__(self):
        self.posts = list()
        self.actions = [self.create_post, self.update_post, self.delete_post, self.save_post, self.go_to_previous_page, self.go_to_next_page]
        # self.actions = {'1': self.createPost, '2': self.updatePost, '3': self.deletePost}

    @staticmethod
    def print_actions():
        print('------------------------------------------------------------------------------------------')
        print('1. 작성하기')
        print('2. 수정하기')
        print('3. 삭제하기')
        print('4. 저장하기')
        print('5. 이전 페이지로')
        print('6. 다음 페이지로')
        print('------------------------------------------------------------------------------------------')

    # iterate posts and print
    def show_posts(self):
        reversed_posts = list(reversed(self.posts))
        paging_reversed_posts = [post for idx, post in enumerate(reversed_posts) if 15 * (Board.current_page_num - 1) <= idx < 15 * Board.current_page_num]
        for post in paging_reversed_posts:
            print('{:^6}'.format(post.posting_num), '|', '{:60.60}'.format(post.posting_title), '|', post.posting_time)

    # check existence of post in posts and handle messages
    def check_existence_of_posts(self):
        if not self.posts:
            print('게시판에 아직 작성된 글이 없습니다.')
            print('한 번 작성해 보는 것은 어떨까요?')
            return
        self.show_posts()

    ## @Auto_save_decorator
    def create_post(self):
        post = Post(input('작성 > '))
        self.posts.append(post)
        print('{}번 글이 성공적으로 작성되었습니다.'.format(post.posting_num))

    ## @Auto_save_decorator
    def update_post(self):
        if not self.posts:
            raise Exception('현재 글이 없습니다.')
        update_idx = int(input('몇 번 글을 수정할까요? '))
        post_to_update = [post for post in self.posts if post.posting_num == update_idx]
        if not post_to_update:
            raise Exception('수정할 해당 번호 글이 없습니다.')
        post_to_update[0].posting_title = input('수정 > ')
        input('{}번 글이 성공적으로 수정되었습니다.'.format(update_idx))
        
    ## @Auto_save_decorator
    def delete_post(self):
        if not self.posts:
            raise Exception('현재 글이 없습니다.')
        delete_idx = int(input('몇 번 글을 지울까요? '))
        post_to_delete = [post for post in self.posts if post.posting_num == delete_idx]
        if not post_to_delete:
            raise Exception('삭제할 해당 번호 글이 없습니다.')
        self.posts.remove(post_to_delete[0])
        input('{}번 글이 성공적으로 삭제되었습니다.'.format(delete_idx))
        
    ## save_post()와 load_post()는 들여쓰기 1수준 제한을 어떻게 걸어야할지 모르겠군요...  
    def save_post(self):
        with open('./광일공방중고나라_게시판목록.csv', 'w', encoding='utf-8', newline='') as writer_csv:
            writer = csv.writer(writer_csv, delimiter=',')
            for post in self.posts:
                writer.writerow([post.posting_num] + [post.posting_title] + [post.posting_time])
        input('저장되었습니다.')
    
    def load_post(self):
        if not os.path.exists('./광일공방중고나라_게시판목록.csv'):
            return
        with open('./광일공방중고나라_게시판목록.csv', 'r', encoding='utf-8') as reader_csv:
            reader = csv.reader(reader_csv, delimiter=',')
            for row in reader:
                new_post = Post(row[1])
                new_post.posting_num = int(row[0])
                new_post.posting_time = row[2]
                self.posts.append(new_post)
                ## posting number에 대한 고찰 
                ## 처음엔 이 반복문 안에서 Post.current_posting_num += 1 식으로 다음 포스팅 번호를 잡아주려고 했습니다만.
                ## 1, 2, 3번 글이 있었는데 2번 글을 삭제하고 1, 3번 글이 남아있는 상태로 저장한다고 할 때
                ## load하고 글을 쓰면 당연하게도 3번글이 두개가 되어버리더군요ㅠ
                ## 그래서 아래와 같이 구현을 했습니다만, 가장 최근 글이 삭제되었다가 save_load되는 경우까지는 구현이 안되는 방법인 것 같습니다.
                Post.current_posting_num = max(Post.current_posting_num, int(row[0]))
        
    def go_to_previous_page(self):
        if Board.current_page_num == 1:
            input('이전 페이지가 없습니다.')
            return
        Board.current_page_num -= 1
    
    def go_to_next_page(self):
        if (Board.current_page_num - 1) * 15 < len(self.posts) <= Board.current_page_num * 15:
            input('다음 페이지가 없습니다.')
            return
        Board.current_page_num += 1

    # manage CRUD of posts
    def post_CRUD_handler(self):
        try:
            menuSel = int(input('> '))
            self.actions[menuSel - 1]()
            # self.actions(menuSel).get(menuSel)()
            return
        except TypeError:
            print('잘못 입력하셨습니다. 올바른 번호를 선택하세요.')
            input()
        except IndexError:
            print('잘못 입력하셨습니다. 현재 글 번호를 맞게 입력하세요.')
            input()
        except Exception as e:
            print('잘못 입력하셨습니다.', e)
            input()
        finally:
            print()


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
    input('프로그램을 시작하시려면 엔터키를 입력하세요...')


if __name__ == '__main__':
    greeting_messages()
    board = Board()
    board.load_post()

    while True:
        clear_screen()
        board.check_existence_of_posts()
        board.print_actions()
        board.post_CRUD_handler()
