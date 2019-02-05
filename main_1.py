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

a = []

if a == []:
    file = open('list.txt', 'w')
    file.write('게시판에 아직 작성된 글이 없습니다. \n한 번 작성해보는 것은 어떨까요?')
    file.close()

while True:
    operating.showing()
    operating.writing(a)
