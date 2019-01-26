import csv
from time import localtime, strftime
# Post의 시간 정보를 기록하기 위한 것

# Board class
# 게시판에 해당하는 클래스
# 게시판에는 Post class 가 Board 클래스의 List 안에 저장됩니다.
# 다양한 operation
# 작성하기 : Input을 사용자로부터 받아 Post를 생성하고 그 Post를 Board 안의 List에 저장합니다.
# 수정하기 : Board 안의 List에 저장되어있는 Post 중 사용자가 지정한 번호의 Post에 대해 '글'만 수정합니다
# 삭제하기 : 사용자로부터 삭제하고 싶은 글의 번호를 받고 해당 Post를 List에서 지웁니다.
# 저장하기 : List 안에 저장되어 있는 Post들을 csv 파일로 저장합니다.
##################################### page_nation의 구현 > pagenumber를 이용하여 하나의 함수로 구현 // 초기페이지 넘버 0
# 페이지를 보여주기 : 가장 최신 글 15개를 최신순으로 보여주는 것
# 이전 페이지로 : 왼쪽 이동 페이지 넘버 1 감소
# 다음 페이지로 : 오른쪽 이동 페이지 넘버 1 증가

class Board: 
    def __init__(self):
        self.post_list = []
        self.call_num = 0
        self.pagenumber = 0

    # 이미 저장되어 있는 정보가 있을 경우에는 그것을 불러내야하므로 Board를 생성할 때 csv 파일의 내용을 Board의 list에 넣는 과정이 필요합니다.
    # 만약 data.csv 에 데이터가 없다면 아무런 일도 일어나지 않습니다.

    def page_showing(self, b):

        total_pagenumber = int((len(b.post_list) / 15)) + 1

        if b.pagenumber < 0:
            b.pagenumber = 0
        
        if b.pagenumber >= total_pagenumber:
            b.pagenumber = total_pagenumber - 1

        determinant = len(b.post_list) - b.pagenumber * 15

        print("----------------------------------------------------------------------")           
        if determinant > 14:
            for i in range(15):
                j = determinant - i - 1
                print("{0:>5} {1:33} {2:22} ".format(b.post_list[j].num, b.post_list[j].name, b.post_list[j].time))
        else:
            for i in range(determinant):
                j = determinant - i - 1
                print("{0:>5} {1:33} {2:22} ".format(b.post_list[j].num, b.post_list[j].name, b.post_list[j].time))
        print("----------------------------------------------------------------------")               

        # 최신글을 15개씩 잘라서 보여줍니다. 
        # 15개 미만시 오류 해결을 위해 list의 길이가 15
        # 이전 페이지는 pagenumber를 1 감소시키고 다음 페이지는 pagenumber를 1증가시킵니다.
        # 맨 처음에 pagenumber는 0으로 합니다.
        # 새 포스트를 작성할 경우 len(b.post_list)가 자동으로 증가합니다.

    def posting(self, b, call_num):
        
        b.call_num = call_num + 1
        
        new_post = Post() 
        # Post 객체 하나 생성
        new_post.name = input('내용을 입력하세요 > ')
        new_post.num = b.call_num
        new_post.time = strftime("%Y-%m-%D %H:%M", localtime())
        # Post 객체에 필요한 데이터를 다 넣고
        b.post_list.append(new_post)
        # Board의 Post 객체 리스트에 추가
        #posting이 호출된 횟수를 세서 넘버링


    def correcting(self, b):
        correct_num = input('고칠 글의 번호를 입력하세요! > ')
        correct_name = input('새로운 내용을 입력하세요! > ')
        j = len(b.post_list)
        for i in range(j):
            if str(b.post_list[i].num) == correct_num:
                b.post_list[i].name = correct_name


    def deleting(self, b):
        delete_num = input('지울 글의 번호를 입력하세요! > ')
        j = len(b.post_list)
        for i in range(j):
            if str(b.post_list[i].num) == delete_num:
                b.post_list.remove(b.post_list[i])
        # 반복문으로 num 과 일치하는 것을 지운다

    def saving(self, b):
        f = open('data.csv', 'w', encoding='utf-8', newline='')
        wr = csv.writer(f)
        for i in range(len(b.post_list)):
            wr.writerow([b.post_list[i].num, b.post_list[i].name, b.post_list[i].time])
        f.close


# Post class
# 게시판에 있는 글 하나하나를 Post라고 한다
# Post의 구성 : 글 번호 + 글 제목 + 연도-월-날짜 작성시간
# 글 번호는 Increasing // Posting 함수가 호출된 횟수를 call_num으로 카운트 함으로써 해결!

class Post:
    def __init__(self):
        self.name = ''
        self.num = 0
        self.time = ''

def initiating(b):
    f = open('data.csv', 'r', encoding = 'utf-8' )
    rdr = csv.reader(f)
    for line in rdr:
        buffer = Post()
        buffer.num = line[0]
        buffer.name = line[1]
        buffer.time = line[2]
        b.post_list.append(buffer)
    f.close()
    b.call_num = len(b.post_list)

def selecting(b, call_num):
    print("1. 작성하기")
    print("2. 수정하기")
    print("3. 삭제하기")
    print("4. 저장하기")
    print("5. 이전 페이지로")
    print("6. 다음 페이지로")
    print("----------------------------------------------------------------------")
    select_num = input('> ')
    if select_num == '1':
        b.posting(b, call_num)
    if select_num == '2':
        b.correcting(b)
    if select_num == '3':
        b.deleting(b)
    if select_num == '4':
        b.saving(b)
    if select_num == '5':
        b.pagenumber = b.pagenumber - 1
    if select_num == '6':
        b.pagenumber = b.pagenumber + 1

if __name__ == '__main__':
    
    b = Board()
    initiating(b)

    while True:
        b.page_showing(b)
        selecting(b, b.call_num)

    #페이지보여주기 출력
    #옵션들 표시 및 어느 옵션할지 받아오는 것
    #옵션 실행
    ########################################## 무한루프