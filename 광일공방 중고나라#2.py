import os 

class Data_Store():
    def __init__(self, data_store_location):
        self.data_store_location = data_store_location

    def give_data(self):
        with open(self.data_store_location, 'r') as file:
            self.data = file.readlines() 

    def take_data(self, data):
        with open(self.data_store_location, 'w') as file:
            file.writelines(data)

class Bulletin_Board():
    def __init__(self):
        pass

    @staticmethod
    def display_intro():
        print('본 프로그램은 중고거래 사이트를 만들기 위한 게시판 프로그램입니다.')
        input('프로그램을 시작하시려면 엔터키를 입력하세요...')
        os.system('cls')
        ArticleStore.give_data()
        if not ArticleStore.data:    
            print('게시판에 아직 작성된 글이 없습니다.')
            print('한 번 작성해보는 것은 어떨까요?')
            return
    
    def add_article(self):
        ArticleStore.give_data()
        ArticleStore.data.append(input('작성해주세요:') + '\n')
        print('{}번째 글을 작성하였습니다.'.format(len(ArticleStore.data)), sep='')
        ArticleStore.take_data(ArticleStore.data)
        input()
        os.system('cls')
        self.display_main_page()

    def correct_article(self):
        ArticleStore.give_data()   
        correct_index = int(input('몇 번 글을 수정 할까요?')) - 1
        ArticleStore.data[correct_index] = input('수정>') + '\n'
        ArticleStore.take_data(ArticleStore.data)
        input()
        os.system('cls')
        self.display_main_page()
           
    def delete_article(self):
        ArticleStore.give_data()
        del ArticleStore.data[int(input('몇 번 글을 삭제 할까요?')) - 1]
        ArticleStore.take_data(ArticleStore.data)
        input()
        os.system('cls')
        self.display_main_page()

    def display_main_page_choice(self):
        print('----------------페이지 목록----------------')
        print('1. 작성하기')
        print('2. 수정하기')
        print('3. 삭제하기')
        print('------------------------------------------')

    def move_each_page(self):
        self.action = int(input('이동하고 싶은 번호를 선택하세요:'))
        if self.action == 1:
            self.add_article()
            return
        if self.action == 2:
            self.correct_article()
            return    
        if self.action ==3:
            self.delete_article()
            return        

    def display_article(self):
        ArticleStore.give_data()
        if ArticleStore.data:
            print('------------------글 목록------------------')
        for index, article in enumerate(ArticleStore.data):
            print('{}. {}'.format(index + 1, article), end='')
        return

    def display_main_page(self):
        self.display_article()
        self.display_main_page_choice()
        self.move_each_page()

if __name__ == "__main__":
    ArticleStore = Data_Store('ArticleList2.txt')
    Bulletin_Board.display_intro()
    bulletin_board = Bulletin_Board()
    bulletin_board.display_main_page()