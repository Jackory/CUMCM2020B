# 本代码模拟了多个玩家根据给定的策略进行运动
# Lines=[
#     [1, 4, 3, 9, 11, 13],
#     [1, 2, 3, 9, 11, 13],
#     [1, 4, 3, 9, 10, 13],
#     [1, 2, 3, 9, 10, 13],
#     [1,5,6,13],
#     [1,4,6,13]
# ]

# Lines=[
#     [1, 4, 3, 9, 11, 13],
#     [1,5,6,13]
# ]

Lines=[
    [1,4,6,13],
    [1,5,6,13],
    [1,4,6,13],
    [1,5,6,13]
]

# Times=[
#     [ 1,1,1,0,0,0,1,1,0,0],
#     [1,1,1]
# ]

Times=[
    [1,1,1],
    [1,0,1,1]
]
Mines=[0,0,0,1,1,1,0,0,0,0]

weather=[0,1,0,0,0,0,1,1,1,1]

cost=[
    [3,9,10],
    [4,9,10]
]
class Player:
    def __init__(self,lineid,cur_time,cur_water,cur_food,cur_money):
        self.lineid=lineid
        self.cur_time=cur_time
        self.cur_water=cur_water
        self.cur_food=cur_food
        self.cur_money=cur_money
        self.point=0
        self.cur_pos = Lines[self.lineid][self.point]
        self.dig=False
        self.go=False

    def Policy(self):
        self.cur_pos = Lines[self.lineid][self.point]
        self.dig=False
        self.go=False
        if self.lineid<2:
            if self.cur_time < len(Times[0]):
                if Times[0][self.cur_time]==1:
                    self.point+=1
                    self.go= True
                # else:
                #     if Mines[self.cur_time]==1:
                #         self.dig=True
                #         self.cur_money+=200
                self.cur_time+=1
        else:
            if self.cur_time < len(Times[1]):
                if Times[1][self.cur_time]==1:
                    self.point+=1
                    self.go = True
                self.cur_time += 1
    def display(self):
        print(self.lineid," ",self.cur_time," ",self.cur_water," ",self.cur_food," ",self.cur_money," ",self.point," ",self.cur_pos)

def count_loss(pos1,pos2,dig1,dig2,go1,go2,gametime):
    loss1=0
    loss2=0
    if pos1==pos2:
        if dig1==1:
            loss1+=100 #挖矿收益减半
            loss1+=(cost[0][weather[gametime]]*5+cost[1][weather[gametime]]*10)*3
        if dig2==1:
            loss2+=100 #挖矿收益减半
            loss2+=(cost[0][weather[gametime]]*5+cost[1][weather[gametime]]*10)*3
        if go1==1:
            loss1+=(cost[0][weather[gametime]]*5+cost[1][weather[gametime]]*10)*4
        if go2==1:
            loss2+=(cost[0][weather[gametime]]*5+cost[1][weather[gametime]]*10)*4
        if go1==0 and dig1==0:
            loss1+=(cost[0][weather[gametime]] * 5 + cost[1][weather[gametime]] * 10) * 2
        if go2 == 0 and dig2 == 0:
            loss2 += (cost[0][weather[gametime]] * 5 + cost[1][weather[gametime]] * 10) * 2
    else:
        if dig1==1:
            loss1+=(cost[0][weather[gametime]]*5+cost[1][weather[gametime]]*10)*3
        if dig2==1:
            loss2+=(cost[0][weather[gametime]]*5+cost[1][weather[gametime]]*10)*3
        if go1==1:
            loss1+=(cost[0][weather[gametime]]*5+cost[1][weather[gametime]]*10)*2
        if go2==1:
            loss2+=(cost[0][weather[gametime]]*5+cost[1][weather[gametime]]*10)*2
        if go1==0 and dig1==0:
            loss1+=(cost[0][weather[gametime]] * 5 + cost[1][weather[gametime]] * 10)
        if go2 == 0 and dig2 == 0:
            loss2 += (cost[0][weather[gametime]] * 5 + cost[1][weather[gametime]] * 10)
    return loss1,loss2

import random

def Game():
    Score={}
    M=[]
    for i in range(2):
        N=[]
        for j in range(2):
           N.append([0,0])
        M.append(N)
    iter=100000
    for i in range(iter):
        for l in range(2):
            for j in range(2):
                if l==0:
                    pp1=(random.randint(0, 1))
                else:
                    pp1=(random.randint(2, 3))
                if j==0:
                    pp2=(random.randint(0,1))
                else:
                    pp2=(random.randint(2, 3))
                p1 = Player(pp1, 0, 42, 47, 9320)
                p2 = Player(pp2, 0, 42, 47, 9320)
                loss11=0
                loss22=0
                for i in range(5):
                    p1.Policy()
                    p2.Policy()
                    pos1=p1.cur_pos
                    pos2=p2.cur_pos
                    loss1,loss2=count_loss(pos1, pos2, p1.dig, p2.dig, p1.go, p2.go, i)
                    #print("Pos1",pos1,p1.go,loss1," ","Pos2",pos2,p2.go,loss2)
                    loss11+=loss1
                    loss22+=loss2
                #print(loss11,loss22)
                #print("\n\n")
                M[l][j][0]+=(p1.cur_money-loss11)
                M[l][j][1]+=(p2.cur_money-loss22)


    for i  in range(2):
        for j in range(2):
            M[i][j][1]=M[i][j][1] / iter
            M[i][j][0] = M[i][j][0] / iter
            print(M[i][j][0],",",M[i][j][1],"      ",end="")
        print("\n")

    # for i  in range(5):
    #     for j in range(6):
    #         #print(j[0],",",j[1],"     ",end="")
    #         M[i][j][1]-=M[i+1][j][1]
    #         print(M[i][j][1], end=" ")
    #     print("\n")
Game()
