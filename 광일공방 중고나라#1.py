
from time import gmtime, strftime

class OldNara() :
    def __init__(self):
        self.posts = list()
        self.intro()

    def intro(self):
        print("""본 프로그램은 광일공방에서 중고거래 사이트를 기웃기웃 거리던
              진영이가 어느날 삘이 꽂혀 '아! 여기가 돈 나오는 방석이다!' 
              생각하자마자 아주 급하게 만들어낸 불안정한 중고거래 사이트입니다.
              물론 아직은 허접한 게시판이지만 1000만 사용자를 꿈꾸는
              진영이는 커다란 희망의 씨앗을 마음에 품고서 오늘도 밤을 지새우며 코드를 작성합니다.""")

        n = input('프로그램을 시작하시려면 엔터키를 입력하세요....')
        if n != '':
            print("프로그램을 종료합니다")
            exit()


    def show(self) :
        if len(self.posts) == 0 :
            print("게시판에 아직 작성된 글이 없습니다.")
            print("한번 작성해보는것은 어떨까요?")
            print("--------------------------------------------------")
            return

        for index, post in enumerate(self.posts) :
            print("{}. {}  | 작성시간 : {} |".format(index+1, post["post"], post["time"]))
        print("--------------------------------------------------")


    def write(self) :
        post_data = {}
        post_data["post"] = input("작성 > ")
        post_data["time"] = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        self.posts.append(post_data)
        print(str(len(self.posts)) + "번째 글이 성공적으로 작성되었습니다.")
        input()

if __name__ == "__main__" :
    old = OldNara()
    while True :
        old.show()
        old.write()
