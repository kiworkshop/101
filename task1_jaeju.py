import os

def intro():
    greeting = 
    '''본 프로그램은 광일공방에서 중고거래 사이트를 기웃기웃 거리던 광일이가 어느날 삘이 꽂혀'아! 여기가 돈 나오는 방석이다!'생각하자마자 아주 급하게 만들어낸 불안정한 중고거래 사이트입니다.
    물론 아직은 허접한 게시판이지만 1000만 사용자를 꿈꾸는 광일이는 커다란 희망의 씨앗을 마음에 품고서 오늘도 밤을 지새우며 코드를 작성합니다.'''

    print()
    print("프로그램을 시작하려면 엔터키를 입력하세요...", end='')
    input()
    os.system('cls' if os.name == 'nt' else 'clear')

def write_post(posts):
    post = input('>')
    posts.append(post)
    n = len(posts)
    print(str(n) + '번째 글이 성공적으로 작성되었습니다.')
    input('엔터를 입력하시면 글목록을 보여드립니다.')

def show_posts(posts):
    if posts == []:
        print('게시판에 아직 작성된 글이 없습니다.')
        print('한 번 작성해보는 것은 어떨까요?')

    for index, post in enumerate(posts):
        print('{글번호}. {글내용}'.format(글번호 = index + 1, 글내용 = post))

    print('-------------------------------------')

if __name__ == "__main__":
    intro()
    posts = list()
    while True:
        show_posts(posts)
        write_post(posts)
        os.system('cls' if os.name == 'nt' else 'clear')