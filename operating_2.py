renumbering = []

def showing():
    with open('list.txt', 'r') as file:
        s = file.read()
        print(s)

def writing(list):
    num = len(list) + 1
    new = input('작성 > ') 
    list.append(new)
    renew = "\n" + str(num) + ". " + new
    renumbering.append(renew)
    with open('list.txt', 'w') as file:
        file.writelines(renumbering)
    print(len(list), "번째 글이 성공적으로 작성되었습니다.")

def correcting(list):
    num = int(input('몇 번째 글을 수정하실 건가요?'))
    buffer = input('수정 > ')
    list[num-1] = buffer
    renumbering[num-1] = "\n" + str(num) + ". " + buffer
    with open('list.txt', 'w') as file:
        file.writelines(renumbering)
    print(num, "번째 글이 성공적으로 작성되었습니다.")

def deleting(list):
    renumbering = []
    num = int(input('몇 번째 글을 지울까요?'))
    list.remove(list[num-1])
    for i in range(len(list)):
        new = "\n" + str(i) + ". " + list[i]
        renumbering.append(new)
    with open('list.txt', 'w') as file:
       file.writelines(renumbering)