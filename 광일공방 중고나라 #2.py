
def printActionList():
        print('---------------------------------------\n1. 작성하기\n2. 수정하기\n3. 삭제하기\n---------------------------------------')

def printItemList(itemList):    
    print('------------------목록-----------------')
    itemIndex = 1
    for item in itemList:
        print(str(itemIndex) + '. ' + item)
        itemIndex += 1
    print('---------------------------------------')

def checkAndPrintItemList(itemList):
    if len(itemList) == 0: #등록된 게시글이 없을 시 
        print("작성된 판매게시글이 없습니다. \n 회원님이 한 번 작성해보시는 것이 어떨까요?")
        addItem(itemList)
        #printItemList(itemList)
    if len(itemList) != 0:
        printItemList(itemList)

def selectAction(itemList):
    inputValue = input()
    
    if inputValue == '1':
        addItem(itemList)
    if inputValue == '2':
        editItem(itemList)
    if inputValue == '3':
        deleteItem(itemList)
    if inputValue != '1' and inputValue != '2' and inputValue != '3':
        print('수행하고 싶은 동작의 번호를 정수로 입력해주세요')    
        printActionList()    
        selectAction(itemList)    

def addItem(itemList):
    newItem = input('추가할 내용을 입력해주세요 >')
    itemList.append(newItem)
    print(str(len(itemList))+ '번째 글이 성공적으로 작성되었습니다.' )

def editItem(itemList):
    try:
        selectedItem = input('몇 번 글을 수정할까요?')
        selectedIndex = int(selectedItem)-1
        editedContent = input('수정할 내용을 입력해주세요 >')
        itemList[selectedIndex] = editedContent
    except:
        print('목록에 있는 글번호를 입력해주세요')
        editItem(itemList)

def deleteItem(itemList):
    try:
        selectedItem = input('몇 번 글을 삭제할까요?')
        selectedIndex = int(selectedItem)-1
        del(itemList[selectedIndex])
    except:
        print('목록에 있는 글번호를 입력해주세요')

def main():
    print("본 프로그램은 광일공방에서 중고거래 사이트를 기우거리던 광일이가 \n...\n중략\n...\n아나바다 철학이 담긴 프로그램을 밤을 지새우며 코드를 작성합니다.")
    input("프로그램을 시작하시려면 엔터키를 입력하세요...")

    itemList = []
    while True:
        checkAndPrintItemList(itemList)
        printActionList()
        selectAction(itemList)

if __name__ == "__main__":
    main()
    