import numpy as np
state_dict={}

M=1200 # 最大负重
init_money=10000
base_water_price=5
base_water_weight=3
base_food_price=10
base_food_weight=2

base_consume_water=[5,8,10]
base_consume_food=[7,6,10]
# state={day ,pos,water,food}
for i in range(180,185):
    for j in range(325,331):
        if base_water_weight*i+base_food_weight*j<=1200 and base_food_price*j+base_water_price*i<10000:
            state=(1,0,i,j)
            state_dict[state]=10000-(base_food_price*j+base_water_price*i)


map1 = np.array([[1,1,6,3],
                [-1,1,2,5],
                [-1,2,1,3],
                [-1,-1,-1,0]])
weather=["高温","高温","晴朗","沙暴","晴朗",
         "高温","沙暴","晴朗","高温","高温",
         "沙暴","高温","晴朗","高温","高温",
         "高温","沙暴","沙暴","高温","高温",
         "晴朗","晴朗","高温","晴朗","沙暴",
         "高温","晴朗","晴朗","高温","高温"
         ]

def cost(cur_time, cur_state, next_state, cur_water, cur_food, states):
    T = map1[cur_state][next_state]
    last_time = cur_time + T
    t = cur_time
    if (t >= 30):
        cur_water = -10000000
        cur_food = -10000000
        states.append('die')
        return (last_time, cur_water, cur_food)
    if cur_state == 1 and next_state == 1:  # 挖矿
        if (weather[t] == '晴朗'):
            cur_water -= base_consume_water[0] * 3
            cur_food -= base_consume_food[0] * 3
        elif (weather[t] == '高温'):
            cur_water -= base_consume_water[1] * 3
            cur_food -= base_consume_food[1] * 3
        elif (weather[t] == '沙暴'):
            cur_water -= base_consume_water[2] * 3
            cur_food -= base_consume_food[2] * 3


    elif (cur_state == next_state):  # 原地停留
        if (weather[t] == '晴朗'):
            cur_water -= base_consume_water[0]
            cur_food -= base_consume_food[0]
        elif (weather[t] == '高温'):
            cur_water -= base_consume_water[1]
            cur_food -= base_consume_food[1]
        elif (weather[t] == '沙暴'):
            cur_water -= base_consume_water[2]
            cur_food -= base_consume_food[2]

    else:  # 行走
        while (t < last_time):
            if (t >= 30):
                break
            if (weather[t] == '晴朗'):
                cur_water -= base_consume_water[0] * 2
                cur_food -= base_consume_food[0] * 2
            elif (weather[t] == '高温'):
                cur_water -= base_consume_water[1] * 2
                cur_food -= base_consume_food[1] * 2
            elif (weather[t] == '沙暴'):
                cur_water -= base_consume_water[2]
                cur_food -= base_consume_food[2]
                last_time += 1
            t += 1
        if (t >= 30):
            cur_water = -10000000
            cur_food = -10000000
            states.append('die')

    return (last_time, cur_water, cur_food)

success_dict={}
#for i in range(30):

for i in range(30):
    print("Start ",i)
    new_dict = {}
    print(len(state_dict))
    for j in list(state_dict.keys()):
        if j[1]==0:
            for l in range(1,4):
                # if l == 3:
                #     print(1,j[1],l,j[2],j[3],[])
                (time,cur_water,cur_food)=cost(i+1,j[1],l,j[2],j[3],[])
                if cur_food<0 or cur_water<0:
                    continue
                state=(time,l,cur_water,cur_food)
                if l==3:
                    if state not in success_dict or success_dict[state]<state_dict[j]:
                        success_dict[state]=state_dict[j]
                else:
                    if state not in new_dict or new_dict[state]<state_dict[j]:
                        new_dict[state]=state_dict[j]
        else:
            for l in range(0,4):
                # if l == 3:
                #     print(1,j[1],l,j[2],j[3],[])
                (time,cur_water,cur_food)=cost(i+1,j[1],l,j[2],j[3],[])
                if cur_food<0 or cur_water<0:
                    continue
                state=(time,l,cur_water,cur_food)
                if l==3:
                    if state not in success_dict or success_dict[state]<state_dict[j]:
                        success_dict[state]=state_dict[j]
                else:
                    temp = state_dict[j]
                    if j[1]==1 and l==1:
                        temp+=1000
                    if l==2:#达到商店，构造可能购买的状态转移
                        can_take=1200-3*state[2]-2*state[3]
                        can_afford=temp
                        for init_water in range(200):
                            for init_food in range(100):
                                if init_food*2+init_water*3<=can_take and init_water*10+init_food*20<=can_afford:
                                    temp_state=(state[0],state[1],state[2]+init_water,state[3]+init_food)
                                    temp_money=can_afford-(init_water*10+init_food*20)
                                    if state not in new_dict or new_dict[state] < temp_money:
                                        new_dict[state] = temp
                    if state not in new_dict or new_dict[state] <  temp:
                        new_dict[state] =  temp
    #print(len(success_dict))

    #print(list(state_dict.keys())[0:5])
    state_dict=new_dict
print(len(success_dict))
c=[ v for v in sorted(success_dict.values(),reverse=True)]
print(c[ : 5])
    #print(list(state_dict.keys())[0:5])