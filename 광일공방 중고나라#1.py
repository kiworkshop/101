def program_start():
    print('kwangilcho:1. 데이터 수집하기 (1) kwangilcho$ python3 광일공방 \\ 중고나라 #1.py\n')
    print('''	본 프로그램은 광일공방에서 중고거래 사이트를 기웃기웃 거리던 광일이가
        어느날 삘이 꽃혀 '아! 여기가 돈 나오는 방석이다!' 생각하자마자 아주
        급하게 만들어낸 불안정한 중고거래 사이트입니다. 물론 아직은 허접한
        게시판이지만 1000만 사용자를 꿈꾸는 광일이는 커다란 희망의 씨앗을 마음에 
        품고서 오늘도 밤을 지새우며 코드를 작성합니다.\n''')
    print('프로그램을 시작하시려면 엔터키를 입력하세요...')

    program_start = input()
    if program_start == '': 
        print(end='')

contents = []
def post():
    if contents == []: 
        print('게시판에 아직 작성된 글이 없습니다.\n한 번 작성해보는 것은 어떨까요?\n-----------------------------------------------------\n> ', end='')
    
    content = input()
    contents.append(content)
    
    print('{}번째 글이 성공적으로 작성되었습니다.'.format(len(contents)))
    print('-----------------------------------------------------')
    
    list()
    print('-----------------------------------------------------')
    print('> ', end='')	
   
    post()

def list():
    for i, content in enumerate(contents):
        print('{}. {}'.format(i+1, content))
	
if __name__ == '__main__':
    program_start()
    post()
