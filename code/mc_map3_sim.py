import numpy as np

weather=[np.random.choice(np.arange(0,2), p=[0.4,0.6]) for _ in range(10)] # 0为晴朗，1为高温

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

def walk(cur_time, cur_state, next_state, cur_water,cur_food,states):
    T = map1[cur_state][next_state]
    last_time = cur_time + T
    t = cur_time
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
                last_time += 1
            else:
                cur_water -= base_consume_water[1]*2
                cur_food -= base_consume_food[1]*2
        t += 1
    return (last_time, cur_water,cur_food)

def mine(cur_time, cur_water,cur_food,states):
    last_time = cur_time + 1
    cur_water -= base_consume_water[0]*3
    cur_food -= base_consume_food[0]*3
    return (last_time,cur_water,cur_food)

def stop(cur_time,cur_water,cur_food,states):
    last_time = cur_time + 1
    cur_water -= base_consume_water[1]
    cur_food -= base_consume_food[1]
    return (last_time,cur_water,cur_food)

# 去矿山
def MC(cur_time, cur_state, cur_money, cur_water, cur_food,states):

    # 存储状态转移
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
        states_list.append(states)
        return cur_money+cur_food*base_food_price/2+cur_water*base_water_price/2
    
    # if(cur_time>=7):
    #     next_state = 2
    #     last_time, cur_water,cur_food= walk(cur_time,cur_state,next_state,cur_water,cur_food,states)
    #     return MC(last_time,next_state,cur_money,cur_water,cur_food,states)
    elif(cur_state == 0):
        next_state = 1
        last_time, cur_water,cur_food= walk(cur_time,cur_state,next_state,cur_water,cur_food,states)
        return MC(last_time,next_state,cur_money,cur_water,cur_food,states)
    
    elif(cur_state == 1): # 在矿山
        if(weather[cur_time] == 0):
            if(cur_water >= (4*base_consume_water[1]+3*base_consume_water[1]) and cur_water >= (4*base_consume_food[1]+3*base_consume_food[1])):# 食物足够
                (last_time,cur_water,cur_food) = mine(cur_time,cur_water,cur_food,states)
                cur_money += 200
                next_state = 1
            else:
                next_state = 2
                (last_time,cur_water,cur_food) = walk(cur_time,cur_state,next_state,cur_water,cur_food,states)
            

        elif(weather[cur_time] == 1): # 高温
            if(cur_water >= 3*2*base_consume_water[2] and cur_food >= 3*2*base_consume_food[2]): # 食物足够
                next_state = 1
                (last_time,cur_water,cur_food) = stop(cur_time,cur_water,cur_food,states)
        
            else: # 食物不够
                next_state = 2
                (last_time,cur_water,cur_food) = walk(cur_time,cur_state,next_state,cur_water,cur_food,states)
        return MC(last_time,next_state,cur_money,cur_water,cur_food,states)

# 不去矿山
def MC2(cur_time, cur_state, cur_money, cur_water, cur_food,states):
    # 存储状态转移
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
        states_list.append(states)
        return cur_money+cur_food*base_food_price/2+cur_water*base_water_price/2
    if(cur_state == 0):
        next_state = 2
        (last_time,cur_water,cur_food) = walk(cur_time,0,2,cur_water,cur_food,states)
        return MC2(last_time,2,cur_money,cur_water,cur_food,states)
    



def Game():
    print('Start')
    iteration = 100000
    money_list = []
    print(weather)
    for i in range(iteration):
        states=[]
        sum_money = MC(0,0,8200,120,120,states)
        money_list.append(sum_money)


    #assert len(money_list) == 100
    index = np.argmax(money_list)
    print("index",index)
    print(max(money_list))
    print('去矿山--最优路径--', states_list[index])

    money_list.clear()
    states_list.clear()

    for i in range(iteration):
        states=[]
        sum_money = MC2(0,0,8380,54,54,states)
        money_list.append(sum_money)
    #assert len(money_list) == 100
    index = np.argmax(money_list)
    print("index",index)
    print(max(money_list))
    print('直奔终点--最优路径--', states_list[index])

    #print(states_list)
    #Draw([money_list],['测试'],range(len(money_list)),"MC")

Game()