def checkItemList(itemList):
    if len(itemList) == 0:
        print("작성된 판매게시글이 없습니다. \n 회원님이 한 번 작성해보시는 것이 어떨까요?")
        addItem(itemList)


def printItemList(itemList):
    checkItemList(itemList)
    print('------------------목록-----------------')
    itemIndex = 2
    for item in itemList:
        print(str(itemIndex) + '. ' + item)
        itemIndex += 1
    print('---------------------------------------')
    

def addItem(itemList):
    newItem = input()
    itemList.append(newItem)
    print(str(len(itemList))+ '번째 글이 성공적으로 작성되었습니다.' )
    

def main():
    print("본 프로그램은 광일공방에서 중고거래 사이트를 기우거리던 광일이가 \n...\n중략\n...\n아나바다 철학이 담긴 프로그램을 밤을 지새우며 코드를 작성합니다.")
    input("프로그램을 시작하시려면 엔터키를 입력하세요...")

    itemList = []
    while True:
        printItemList(itemList)
        addItem(itemList)

if __name__ == "__main__":
    main()
    