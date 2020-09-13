import numpy as np
from Draw import Draw

# 直接到达终点
map1 = np.array([[1,-1,3],
                [-1,1,2],
                [-1,-1,0]])

# 先到矿山
map2 = np.array([[1,3,-1],
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




def cost(cur_time, cur_state, next_state, cur_water,cur_food,states,map_,weather):
    T = map_[cur_state][next_state]
    last_time = cur_time + T
    t = cur_time
    if(t>10):
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


    elif(cur_state == next_state): #原地停留
        if(weather[t] == 0):
            cur_water -= base_consume_water[0]
            cur_food -= base_consume_food[0]
        elif(weather[t] == 1):
            cur_water -= base_consume_water[1]
            cur_food -= base_consume_food[1]

    else:  # 行走
        while(t < last_time):
            if(t >10):
                break
            if(weather[t] == 0):
                cur_water -= base_consume_water[0]*2
                cur_food -= base_consume_food[0]*2
            elif(weather[t] == 1):
                if(np.random.uniform() < 0.4):
                    cur_water -= base_consume_water[1]
                    cur_food -= base_consume_food[1]
                    last_time += 1
                else:
                    cur_water -= base_consume_water[1]*2
                    cur_food -= base_consume_food[1]*2
            t += 1
        if(t>10):
            cur_water = -10000000
            cur_food = -10000000
            states.append('die')
            
    return (last_time, cur_water,cur_food)


def MC(cur_time, cur_state, cur_money, cur_water, cur_food,states, map_,weather):

    states.append((cur_time,cur_state,cur_money,cur_water,cur_food))
    if cur_water < 0 or cur_food < 0:
        states_list.append(states)
        return 0

    if cur_money < 0:
        states_list.append(states)
        return 0        

    if cur_time > 10:
        states_list.append(states)
        return 0
    

    if cur_state == 2: # 终点
        states_list.append(states)
        return cur_money+cur_food*base_food_price/2+cur_water*base_water_price/2
    
    next_state = np.random.choice(len(map_))
    while map_[cur_state][next_state] == -1:
        next_state = np.random.choice(len(map_))

    (next_time,next_water,next_food) = cost(cur_time,cur_state,next_state,cur_water,cur_food,states,map_,weather)


    if cur_state == 0:
        return MC(next_time, 
                    next_state, 
                    cur_money, 
                    next_water, 
                    next_food,states,map_,weather)
                
    if cur_state == 1: # 矿场
        if(cur_state == 1 and next_state == 1):
            return MC(next_time, 
                    next_state, 
                    cur_money+200, 
                    next_water, 
                    next_food,states,map_,weather)
        else:
            return MC(next_time, 
                    next_state, 
                    cur_money, 
                    next_water, 
                    next_food,states,map_,weather)
           


def Game():
    print('Start')
    iteration = 1000
    money_list = []
    returns = []
    E1 = []
    E2 = []
    print('------先到终点-------')
    for k in range(iteration):
        for i in range(100):
            # 0晴朗 1高温 2沙暴
            weather = [-1]
            weather.extend([np.random.choice(np.arange(0,2), p=[0.4,0.6]) for _ in range(10)] )
            states=[]
            sum_money = MC(1,0,9190,54,54,states,map1,weather)
            money_list.append(sum_money)
        returns.append(max(money_list))
        E1.append(sum(returns)/(k+1))

    index = np.argmax(money_list)
    print(index)
    print(max(money_list))
    print('--最优路径--', states_list[index])

    money_list.clear()
    states_list.clear()
    returns.clear()
    print('------先到矿山-----')
    for k in range(iteration):
        for i in range(100):
            # 0晴朗 1高温 2沙暴
            weather = [-1]
            weather.extend([np.random.choice(np.arange(0,2), p=[0.4,0.6]) for _ in range(10)] )
            states=[]
            sum_money = MC(1,0,6400,240,240,states,map2,weather)
            money_list.append(sum_money)
        returns.append(max(money_list))
        E2.append(sum(returns)/(k+1))
    index = np.argmax(money_list)
    print(max(money_list))
    print('--最优路径--', states_list[index])
    # 先到矿山
    #print(E)
    Draw([E1,E2],['直接到终点','先到矿山再到终点'],range(len(E1)),"")
    #Draw([E1],['直接到终点'],range(len(E1)),"MC")

if __name__ == "__main__":
    Game()
