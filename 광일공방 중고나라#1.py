import os 
WANT_TO_POST = True

class Bulletin_Board():
    def __init__(self):
        self.article = list()

    @staticmethod
    def display_intro():
        print('본 프로그램은 중고거래 사이트를 만들기 위한 게시판 프로그램입니다.')
        input('프로그램을 시작하시려면 엔터키를 입력하세요...')
        os.system('cls')
    
    def display_article(self):
        if len(self.article) == 0:    
            print('게시판에 아직 작성된 글이 없습니다.')
            print('한 번 작성해보는 것은 어떨까요?')
            return

        for index, article in enumerate(self.article):
            print('{}. {}'.format(index + 1, article), end='')
        print('-----------------------------------')

    def add_article(self):
        self.article.append(input('작성해주세요:') + '\n')
        print('{}번째 글을 작성하였습니다.'.format(len(self.article)))
        input()
        os.system('cls')

if __name__ == "__main__":
    Bulletin_Board.display_intro()
    bulletin_board = Bulletin_Board()
    bulletin_board.display_intro()
    while WANT_TO_POST:
        bulletin_board.display_article()
        bulletin_board.add_article()