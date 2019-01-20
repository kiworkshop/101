startingMessage = """
    본 프로그램은 광일공방에서 중고거래 사이트를 기웃기웃 거리던 광일이가 
    어느 날 삘이 꽃혀 '아! 여기가 돈 나오는 방석이다!' 생각하자마자 아주 
    급하게 만들어낸 불안정한 중고거래 사이트입니다. 물론 아직은 허접한 
    게시판이지만 1000만 사용자를 꿈꾸는 광일이는 커다란 희망의 씨앗을 마음에 
    품고서 오늘도 밤을 지새우며 코드를 작성합니다.

프로그램을 시작하시려면 엔터키를 입력하세요..."""

noPostMessage = """
게시판에 아직 작성된 글이 없습니다. 
한 번 작성해 보는 것은 어떨까요?
-------------------------------------------------------
> """
postList = []   # TODO: name에 list가 굳이 들어갈 필요가 없다! 자료구조는 보통 네이밍에 들어가지 않는다.

def startingMenu():
    print(startingMessage, end="")
    input() # To wait user


# iterate postList and print
def showPosts():
    for idx, post in enumerate(postList):
        print(idx + 1, ". ", post, sep="")  # TODO: format 적용해보기
    print('-------------------------------------------------------')
    print('> ', end="")


# append post to postList
def managePostList():   # TODO: 게시판을 class 형태로 묶어보기
    if not postList:
        print(noPostMessage, end="")
    else:
        showPosts()
    postList.append(input())
    print(len(postList), "번째 글이 성공적으로 작성되었습니다.", sep="")
    print()


# TODO
# def clear_screen():
#     os.system('cls' if os.name == 'nt' else 'clear')


def main():
    startingMenu()
    while True:
        managePostList() 


if __name__ == '__main__':
    main()