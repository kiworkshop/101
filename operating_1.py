def showing():
    with open('list.txt', 'r') as file:
        s = file.read()
        print(s)

def writing(list):
    num = len(list) + 1
    new = str(num)+". " + input('작성 > ') +"\n"
    list.append(new)
    with open('list.txt', 'w') as file:
        file.writelines(list)
    print(len(list), "번째 글이 성공적으로 작성되었습니다.")