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
-------------------------------------------------------"""

CRUDMessage = """
1. 작성하기 
2. 수정하기 
3. 삭제하기
-------------------------------------------------------
> """

postList = []


# iterate postList and print
def showPosts():
    for idx, post in enumerate(postList):
        print(idx + 1, ". ", post, sep="")
    print("-------------------------------------------------------", end="")


# check existence of post in postList and handle messages
def checkExistenceOfPostList():
    if not postList:
        return print(noPostMessage, end="")
    showPosts()


def createPost():
    postList.append(input("작성 > "))
    print(len(postList), "번째 글이 성공적으로 작성되었습니다.", sep="")


def updatePost():
    if not postList:
        raise Exception("현재 글이 없습니다.")
    updateIdx = int(input("몇 번 글을 수정할까요? ")) - 1
    postList.pop(updateIdx)
    postList.insert(updateIdx, input("수정 > "))


def deletePost():
    if not postList:
        raise Exception("현재 글이 없습니다.")
    deleteIdx = int(input("몇 번 글을 지울까요? ")) - 1
    postList.pop(deleteIdx)


def CRUDMenu(menuSel):
    return {'1': createPost, '2': updatePost, '3': deletePost}


# manage CRUD of posts
def postCRUDHandler():
    checkExistenceOfPostList()

    menuSel = input(CRUDMessage)
    try:
        CRUDMenu(menuSel).get(menuSel)()
    except TypeError:
        print("잘못 입력하셨습니다. 올바른 번호를 선택하세요.")
    except IndexError:
        print("잘못 입력하셨습니다. 현재 글 번호를 맞게 입력하세요.")
    except Exception as e:
        print("잘못 입력하셨습니다.", e)
    finally:
        print()


def main():
    print(startingMessage, end="")
    input() # To wait user

    while True:
        postCRUDHandler() 


if __name__ == '__main__':
    main()