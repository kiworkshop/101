import os

class openList_appending:
    def __enter__(self):
        self.file = open('list.txt', 'a+')
        return self.file

    def __exit__(self, exc_type, exc_value, traceback):
        self.file.close()

class openList_writing:
    def __enter__(self):
        self.file = open('list.txt', 'w')
        return self.file

    def __exit__(self, exc_type, exc_value, traceback):
        self.file.close()

class openList_editing:
    def __enter__(self):
        self.file = open('list.txt', 'r')
        return self.file

    def __exit__(self, exc_type, exc_value, traceback):
        self.file.close()

def print_sep(func):
    def wrapper():
        func()
        print('-------------------------------------')
    return wrapper

def is_existing(func):
    def wrapper():
        if func() == []:
            print('게시판에 아직 작성된 글이 없습니다.')
            print('한번 작성해보는 것은 어떨까요?')
    return wrapper

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
    os.system('cls' if os.name == 'nt' else 'clear')

@print_sep
def what_do_you_want():
    print('1. 작성하기')
    print('2. 수정하기')
    print('3. 삭제하기')

def make_list():
    with openList_editing() as reading:
        readings = reading.readlines()
    return readings

@print_sep
@is_existing
def show_List():
    r = make_list()
    for i in range(len(r)):
        print('{글번호}. {글제목}'.format(글번호 = i + 1, 글제목 = r[i].rstrip('\n')))
    return r

def writing_article():
    n = len(make_list())
    n += 1
    article = input('작성 >')
    with openList_appending() as writing:
        writing.write(article + '\n')
    print(str(n) + '번째 글이 성공적으로 저장되었습니다.')

def update_article(what_article):
    article_number = int(what_article) - 1
    r = make_list()
    updated_article = input('수정 >')
    r[article_number] = updated_article +'\n'
    with openList_writing() as update:
        update.writelines(r)

def delete_article(what_article):
    article_number = int(what_article)-1
    r = make_list()
    del r[article_number]
    with openList_writing() as delete:
        delete.writelines(r)

def writing_updating_deleting(i_want_this):
    if i_want_this == '1':
        writing_article()
    elif i_want_this == '2':
        what_article = input('몇 번 글을 수정할까요?')
        update_article(what_article)
    elif i_want_this == '3':
        what_article = input('몇번 글을 지울까요?')
        delete_article(what_article)

    input()
    os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == '__main__':
    intro()
    while True:
        show_List()
        what_do_you_want()
        i_want_this = input('>')
        writing_updating_deleting(i_want_this)
