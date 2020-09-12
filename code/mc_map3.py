import numpy as np
from Draw import Draw

map1 = np.array([[1,3,3],
                [-1,1,2],
                [-1,-1,0]])

states_list = []

M=1200 # 最大负重
init_money=10000
base_water_price=5
base_water_weight=3
base_food_price=10
base_food_weight=2

base_consume_water=[3,9,10]
base_consume_food=[4,9,10]

# 晴朗 高温 沙暴
weather=[np.random.choice(np.arange(0,2), p=[0.4,0.6]) for _ in range(10)] # 0为晴朗，1为高温

def cost(cur_time, cur_state, next_state, cur_water,cur_food,states):
    T = map1[cur_state][next_state]
    last_time = cur_time + T
    t = cur_time
    if(t>=10):
        cur_water = -10000000
        cur_food = -10000000
        states.append('die')
        return (last_time, cur_water,cur_food)
    isdig = False # 是否能够继续挖矿
    if cur_state == 1 and next_state == 1: # 挖矿
        if(weather[t] == 0):
            cur_water -= base_consume_water[0]*3
            cur_food -= base_consume_food[0]*3
        elif(weather[t] == 1):
            if(cur_water >= 3*2*base_consume_water[2] and cur_food >= 3*2*base_consume_food[2]):
                cur_water -= base_consume_water[1]
                cur_food -= base_consume_food[1]
                isdig = True
            else:
                cur_water -= base_consume_water[1]*2
                cur_food -= base_consume_food[1]*2
                isdig = False
            
    elif(cur_state == next_state): #原地停留
        if(weather[t] == 0):
            cur_water -= base_consume_water[0]
            cur_food -= base_consume_food[0]
        elif(weather[t] == 1):
                cur_water -= base_consume_water[1]
                cur_food -= base_consume_food[1]


    else:  # 行走
        while(t < last_time):
            if(t >= 10):
                break
            if(weather[t] == 0):
                cur_water -= base_consume_water[0]*2
                cur_food -= base_consume_food[0]*2
            elif(weather[t] == 1):
                if(np.random.uniform() < 0.4):
                    cur_water -= base_consume_water[1]
                    cur_food -= base_consume_food[1]
                else:
                    cur_water -= base_consume_water[1]*2
                    cur_food -= base_consume_food[1]*2
            t += 1
        if(t>=10):
            cur_water = -10000000
            cur_food = -10000000
            states.append('die')
            

    return (last_time, cur_water,cur_food, isdig)


def MC(cur_time, cur_state, cur_money, cur_water, cur_food,states):

    states.append((cur_time,cur_state,cur_money,cur_water,cur_food))
    if cur_water < 0 or cur_food < 0:
        states_list.append(states)
        return 0

    if cur_money < 0:
        states_list.append(states)
        return 0        

    if cur_time >= 10:
        #print(states)
        states_list.append(states)
        return 0
    

    if cur_state == 2: # 终点
        # print("curwater----:", cur_water)
        # print("curfood----:",cur_food)
        states_list.append(states)
        return cur_money+cur_food*base_food_price/2+cur_water*base_water_price/2

    next_state = np.random.choice(len(map1))
    while map1[cur_state][next_state] == -1:
        next_state = np.random.choice(len(map1))

    if(cur_state == 1): # 鼓励多挖矿
        if(np.random.uniform() < 0.5):
            next_state = 1

    (next_time,next_water,next_food,isdig) = cost(cur_time,cur_state,next_state,cur_water,cur_food,states)


    if cur_state == 0:
        return MC(next_time, 
                    next_state, 
                    cur_money, 
                    next_water, 
                    next_food,states)

    if cur_state == 1: # 矿场 
        if(cur_state == 1 and next_state == 1):
            if isdig == True:
                return MC(next_time, 
                        next_state, 
                        cur_money+200, 
                        next_water, 
                        next_food,states)
        return MC(next_time, 
                next_state, 
                cur_money, 
                next_water, 
                next_food,states)
           


def Game():
    print('Start')
    iteration = 100000
    money_list = []
    sum_money = 0
    for i in range(iteration):
        states=[]
        sum_money = MC(0,0,7400,240,240,states)
        money_list.append(sum_money)
 #   print(money_list)
  #  for i in states_list:
      #  print(i)
    assert len(money_list) == 100000
    index = np.argmax(money_list)
    print(index)
    print(max(money_list))
    print('--最优路径--', states_list[index])
    #print(states_list)
    #Draw([money_list],['测试'],range(len(money_list)),"MC")

# 25
# 10000.0
# --最优路径-- [(0, 0, 7400, 240, 240), (3, 1, 7400, 240, 240), (4, 1, 7600, 240, 240), (5, 1, 7800, 240, 240), (6, 1, 8000, 240, 240), (7, 1, 8200, 240, 240), (9, 2, 8200, 240, 240)]
Game()
print(weather)