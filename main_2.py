import operating

s_1 = """본 프로그램은 광일공방에서 중고거래 사이트를 기웃기웃 거리던 광일이가 
어느날 삘이 꽂혀 \'아! 여기가 돈 나오는 방석이다!\' 생각하자마자 아주 급하게 
만들어낸 불안정한 중고거래 사이트입니다. 물론 아직은 허접한 게시판이지만 1000만 
사용자를 꿈구는 광일이는 커다란 희망의 씨앗을 마음에 품고서 오늘도 밤을 지세우며
코드를 작성합니다."""

print(s_1)

s_2 = """프로그램을 시작하시려면 Enter 키를 눌러주세요... """

togoNotogo = input(s_2)

if togoNotogo != "":
    quit()

print("\n")

# 여기까지가 프로그램의 시작 아랫부분은 입력받고 출력하는 것 출력이 우선 그리고 입력 for는 iterble인 경우에 많이 쓴다
# enumerate 공부하기   for index, post in enumerate(posts)
# formatted string print('안녕하세요 {}님',format(arg1, arg2, arg3) >> print('{}, {}', index+1, post)

#if __name__=="__main__":

a = []

if a == []:
    file = open('list.txt', 'w')
    file.write('게시판에 아직 작성된 글이 없습니다. \n한 번 작성해보는 것은 어떨까요?')
    file.close()

while True:
    operating.showing()
    print('----------------------------------')
    print('1. 작성하기\n2. 수정하기\n3. 삭제하기')
    print('----------------------------------')
    num = int(input('> '))
    if num == 1:
        operating.writing(a)
    if num == 2:
        operating.correcting(a)
    if num == 3:
        operating.deleting(a)
    # 예외의 경우에서 어떻게 처리할지에 대해서도 넣어야겠다.
    # select를 만들고 return을 해서 다시 while문에서 돌아갈 수 있도록 한다.
    # 재귀를 피해야하는데 // 모든 재귀는 모든 반복으로 풀 수 있는데 stack overflow가 날 수 있다. 나는 제어할 수 없다. 코드가 복잡해질수록
    # 수정/삭제시 해당 번호가 없는 경우를 처리하는 코드를 넣어야한다.
    # try except 코드 공부하기

# 자료이름을 변수명으로 사용하지 않는다