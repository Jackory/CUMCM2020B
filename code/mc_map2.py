import numpy as np
from Draw import Draw

map1 = np.array([[-1,7,9,8,9,-1],
                [-1,1,-1,1,-1,-1],
                [-1,-1,1,-1,1,2],
                [-1,-1,2,-1,-1,-1],
                [-1,-1,1,-1,-1,2],
                [-1,-1,-1,-1,-1,0]])

states_list = []

M=1200 # 最大负重
init_money=10000
base_water_price=5
base_water_weight=3
base_food_price=10
base_food_weight=2

base_consume_water=[5,8,10]
base_consume_food=[7,6,10]

# 晴朗 高温 沙暴
weather=["0","高温","高温","晴朗","沙暴","晴朗",
         "高温","沙暴","晴朗","高温","高温",
         "沙暴","高温","晴朗","高温","高温",
         "高温","沙暴","沙暴","高温","高温",
         "晴朗","晴朗","高温","晴朗","沙暴",
         "高温","晴朗","晴朗","高温","高温"
         ]

def cost(cur_time, cur_state, next_state, cur_water,cur_food,states):
    T = map1[cur_state][next_state]
    last_time = cur_time + T
    t = cur_time
    if(t>30):
        cur_water = -10000000
        cur_food = -10000000
        states.append('die')
        return (last_time, cur_water,cur_food)
    if (cur_state == 1 and next_state == 1) or (cur_state == 2 and next_state == 2): # 挖矿
        if(weather[t] == '晴朗'):
            cur_water -= base_consume_water[0]*3
            cur_food -= base_consume_food[0]*3
        elif(weather[t] == '高温'):
            cur_water -= base_consume_water[1]*3
            cur_food -= base_consume_food[1]*3
        elif(weather[t] == '沙暴'):
            cur_water -= base_consume_water[2]*3
            cur_food -= base_consume_food[2]*3


    elif(cur_state == next_state): #原地停留
        if(weather[t] == '晴朗'):
            cur_water -= base_consume_water[0]
            cur_food -= base_consume_food[0]
        elif(weather[t] == '高温'):
            cur_water -= base_consume_water[1]
            cur_food -= base_consume_food[1]
        elif(weather[t] == '沙暴'):
            cur_water -= base_consume_water[2]
            cur_food -= base_consume_food[2]

    else:  # 行走
        while(t < last_time):
            if(t >30):
                break
            if(weather[t] == '晴朗'):
                cur_water -= base_consume_water[0]*2
                cur_food -= base_consume_food[0]*2
            elif(weather[t] == '高温'):
                cur_water -= base_consume_water[1]*2
                cur_food -= base_consume_food[1]*2
            elif(weather[t] == '沙暴'):
                cur_water -= base_consume_water[2]
                cur_food -= base_consume_food[2]
                last_time += 1
            t += 1
        if(t>30):
            cur_water = -10000000
            cur_food = -10000000
            states.append('die')
            
    return (last_time, cur_water,cur_food)


def MC(cur_time, cur_state, cur_money, cur_water, cur_food,states):

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
    

    if cur_state == 5: # 终点
        states_list.append(states)
        return cur_money+cur_food*base_food_price/2+cur_water*base_water_price/2
    
    if cur_state == 4 : # 村庄  买东西
        wmax=240
        fmax=240
        if(cur_water < wmax):
            cur_money -= (wmax-cur_water)* base_water_price*2
            cur_water = wmax
        if(cur_food < fmax):
            cur_money -= (fmax-cur_food) * base_food_price*2
            cur_food = fmax
        states.append((cur_time, cur_state, cur_money, cur_water, cur_food))


    if cur_state == 3: # 买到上限

        wmax=238
        fmax=226
        if(cur_water < wmax):
            cur_money -= (wmax-cur_water)* base_water_price*2
            cur_water = wmax
        if(cur_food < fmax):
            cur_money -= (fmax-cur_food) * base_food_price*2
            cur_food = fmax
        states.append((cur_time, cur_state, cur_money, cur_water, cur_food))



    next_state = np.random.choice(len(map1))
    while map1[cur_state][next_state] == -1:
        next_state = np.random.choice(len(map1))


    (next_time,next_water,next_food) = cost(cur_time,cur_state,next_state,cur_water,cur_food,states)


    if cur_state == 0:
        return MC(next_time, 
                    next_state, 
                    cur_money, 
                    next_water, 
                    next_food,states)
    if cur_state == 3 or cur_state == 4: # 村庄
        return MC(next_time, 
            next_state, 
            cur_money, 
            next_water, 
            next_food,states)
                
    if cur_state == 1 or cur_state == 2: # 矿场
        if((cur_state == 1 and next_state == 1) or (cur_state == 2 and next_state == 2)):
            return MC(next_time, 
                    next_state, 
                    cur_money+1000, 
                    next_water, 
                    next_food,states)
        else:
            return MC(next_time, 
                    next_state, 
                    cur_money, 
                    next_water, 
                    next_food,states)
           


def Game():
    print('Start')
    iteration = 1000000
    money_list = []
    sum_money = 0
    for i in range(iteration):
        states=[]
        sum_money = MC(1,0,5840,184,324,states)
        money_list.append(sum_money)
    index = np.argmax(money_list)
    print('---index----',index)
    print(max(money_list))
    print('--最优路径--', states_list[index])

Game()
