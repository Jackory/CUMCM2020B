import numpy as np
from Draw import Draw

map1 = np.array([[-1,5,-1,-1],
                [-1,1,2,3],
                [-1,2,1,3],
                [-1,-1,-1,0]])

states_list = []

M=1200 # 最大负重
init_money=10000
base_water_price=5
base_water_weight=3
base_food_price=10
base_food_weight=2

base_consume_water=[3,9,10]
base_consume_food=[4,9,10]




def cost(cur_time, cur_state, next_state, cur_water,cur_food,states,weather):
    T = map1[cur_state][next_state]
    last_time = cur_time + T
    t = cur_time
    if(t>=30):
        cur_water = -10000000
        cur_food = -10000000
        states.append('die')
        return (last_time, cur_water,cur_food)
    if cur_state == 1 and next_state == 1: # 挖矿
        if(weather[t] == 0):
            cur_water -= base_consume_water[0]*3
            cur_food -= base_consume_food[0]*3
        elif(weather[t] == 1):
            cur_water -= base_consume_water[1]*3
            cur_food -= base_consume_food[1]*3
        elif(weather[t] == 2):
            cur_water -= base_consume_water[2]*3
            cur_food -= base_consume_food[2]*3


    elif(cur_state == next_state): #原地停留
        if(weather[t] == 0):
            cur_water -= base_consume_water[0]
            cur_food -= base_consume_food[0]
        elif(weather[t] == 1):
            cur_water -= base_consume_water[1]
            cur_food -= base_consume_food[1]
        elif(weather[t] == 2):
            cur_water -= base_consume_water[2]
            cur_food -= base_consume_food[2]

    else:  # 行走
        while(t < last_time):
            if(t >30):
                break
            if(weather[t] == 0):
                cur_water -= base_consume_water[0]*2
                cur_food -= base_consume_food[0]*2
            elif(weather[t] == 1): # 高温天气0.4概率停止，0.6概率前行
                if(np.random.uniform() < 0.4):
                    cur_water -= base_consume_water[1]
                    cur_food -= base_consume_food[1]
                    last_time += 1
                else:
                    cur_water -= base_consume_water[1]*2
                    cur_food -= base_consume_food[1]*2
            elif(weather[t] == 2):
                cur_water -= base_consume_water[2]
                cur_food -= base_consume_food[2]
                last_time += 1
            t += 1
        if(t>30):
            cur_water = -10000000
            cur_food = -10000000
            states.append('die')
            
    return (last_time, cur_water,cur_food)


def MC(cur_time, cur_state, cur_money, cur_water, cur_food,states,weather):

    states.append((cur_time,cur_state,cur_money,cur_water,cur_food))
    if cur_water < 0 or cur_food < 0:
        states_list.append(states)
        return 0

    if cur_money < 0:
        states_list.append(states)
        return 0        

    if cur_time > 30:
        #print(states)
        states_list.append(states)
        return 0

    if cur_state == 3: # 终点

        states_list.append(states)
        return cur_money+cur_food*base_food_price/2+cur_water*base_water_price/2

    if cur_state == 2: # 商店 买到上限
        wmax = min(cur_money / (base_food_price*2 + base_water_price*2),
                    M / (base_food_weight + base_water_weight))
        wmax = int(wmax)
        fmax = wmax
        if(cur_water < wmax):
            cur_money -= (wmax-cur_water)* base_water_price*2
            cur_water = wmax
        if(cur_food < fmax):
            cur_money -= (fmax-cur_food) * base_food_price*2
            cur_food = fmax



    next_state = np.random.choice(len(map1))
    while map1[cur_state][next_state] == -1:
        next_state = np.random.choice(len(map1))

    (next_time,next_water,next_food) = cost(cur_time,cur_state,next_state,cur_water,cur_food,states,weather)


    if cur_state == 0:
        return MC(next_time, 
                    next_state, 
                    cur_money, 
                    next_water, 
                    next_food,states,weather)

    if cur_state == 2: # 村庄
        return MC(next_time, 
            next_state, 
            cur_money, 
            next_water, 
            next_food,states,weather)
                


    if cur_state == 1: # 矿场
        if(cur_state == 1 and next_state == 1):
            return MC(next_time, 
                    next_state, 
                    cur_money+1000, 
                    next_water, 
                    next_food,states,weather)
        else:
            return MC(next_time, 
                    next_state, 
                    cur_money, 
                    next_water, 
                    next_food,states,weather)
           


def Game():
    #0晴朗 1高温 2沙暴

    print('Start')
    iteration = 1000

    returns = []
    E = []
    sum_money = 0
    for k in range(1000):
        money_list = []
        for i in range(500):
            states=[]
            weather = [-1]
            weather.extend([np.random.choice(np.arange(0,3),p=[1/3,1/2,1/6]) for _ in range(30)])
            sum_money = MC(1,0,6400,240,240,states,weather)
            money_list.append(sum_money)
        returns.append(max(money_list))
        E.append(sum(returns)/(k+1))
    #print(E)


#     print('Start')
#     iteration = 10000
#     money_list = []
#  #  states_list = []
#     sum_money = 0
#     for i in range(iteration):
#         weather = [-1]
#         weather.extend([np.random.choice(np.arange(0,3), p=[1/3,1/2,1/6]) for _ in range(30)] )
#         states=[]
#         sum_money = MC(1,0,6400,240,240,states,weather)
#         money_list.append(sum_money)
#     index = np.argmax(money_list)
#     print(index)
#     print(max(money_list))
#     print('--最优路径--', states_list[index])
    #print(states_list)
    Draw([E],[''],range(len(E)),"")

#[(0, 0), (8, 2), (10, 1), (11, 1), (12, 1), (13, 1), (14, 1), (16, 2), (20, 1), (21, 1), (22, 1), (28, 3)]
Game()
