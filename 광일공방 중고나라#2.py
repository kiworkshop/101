def program_start():
    print('kwangilcho:1. 데이터 수집하기 (1) kwangilcho$ python3 광일공방 \\ 중고나라 #1.py\n')
    print('    본 프로그램은 광일공방에서 중고거래 사이트를 기웃기웃 거리던 광일이가')
    print('    어느날 삘이 꽃혀 \'아! 여기가 돈 나오는 방석이다!\' 생각하자마자 아주')
    print('    급하게 만들어낸 불안정한 중고거래 사이트입니다. 물론 아직은 허접한')
    print('    게시판이지만 1000만 사용자를 꿈꾸는 광일이는 커다란 희망의 씨앗을 마음에')
    print('    품고서 오늘도 밤을 지새우며 코드를 작성합니다.\n')
    print('프로그램을 시작하시려면 엔터키를 입력하세요...')

    start = input() 
    if start == '':
        print(end='')

contents = []
def menu(choice=None):
    if contents == []: 
        print('게시판에 아직 작성된 글이 없습니다.\n한 번 작성해보는 것은 어떨까요?')
    
    print('-----------------------------------------------------')
    print('1. 작성하기\n2. 수정하기\n3. 삭제하기')
    print('-----------------------------------------------------')
    
    print('> ', end='')	
    try:
        choice = int(input())
        if choice == 1:
            post()
        if choice == 2:
            revise()
        if choice == 3:
            delete()
        if choice != 1 or 2 or 3: #1,2,3 이외의 숫자 입력시
            menu()
    except: #숫자 외의 문자 입력시(모든 함수에 해당)
        menu()            


def post():
    print('작성 > ', end='')	
    content = input()
    contents.append(content)
    
    print('{}번째 글이 성공적으로 작성되었습니다.'.format(len(contents)))
    print('-----------------------------------------------------')
    
    list()
   

def revise():
    print('몇 번 글을 수정할까요? ', end='') 
    index = int(input())-1
    print('수정 > ', end='') 
    contents[index] = input()  

    list()


def delete():
    print('몇 번 글을 지울까요? ', end='')
    index = int(input())-1 
    del contents[index]

    list()


def list():
    for i, content in enumerate(contents):
        print('{}. {}'.format(i+1, content))
    
    menu()


if __name__ == '__main__':
    program_start()
    menu()