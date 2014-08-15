import go_GPIO

go = go_GPIO.GPIO()
while True:
    print('left:0,right:1,forward:2,back:3,stop:4')
    i = int(input().split()[0])
    if i == 0:
        go.left(30)
    elif i== 1:
        go.right(30)
    elif i== 2:
        go.forward(30)
    elif i== 3:
        go.back(30)
    elif i==4:
        go.stop()
