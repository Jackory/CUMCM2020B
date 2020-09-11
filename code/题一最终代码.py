init_water=108
init_food=438
money=5080

weather=["高温","高温","晴朗","沙暴","晴朗",
         "高温","沙暴","晴朗","高温","高温",
         "沙暴","高温","晴朗","高温","高温",
         "高温","沙暴","沙暴","高温","高温",
         "晴朗","晴朗","高温","晴朗","沙暴",
         "高温","晴朗","晴朗","高温","高温"
         ]

base_consume_water=[5,8,10]
base_consume_food=[7,6,10]

def get_weather(i):
    if i=="高温":
        return 1
    if i=="晴朗":
        return 0
    else:
        return 2

def go(hhday,road):

    already_go=0
    consume_water=0
    consume_food=0
    while already_go<road:
        if hhday>30:
            return -1,-1,-1
        if get_weather(weather[hhday-1])!=2:
            #print(hhday,"Day go",weather[hhday])
            consume_food+=base_consume_food[get_weather(weather[hhday-1])]*2
            consume_water+=base_consume_water[get_weather(weather[hhday-1])]*2
            hhday+=1
            already_go+=1
        else:
            #print(hhday, "Day dont go")
            consume_food += base_consume_food[get_weather(weather[hhday-1])]
            consume_water += base_consume_water[get_weather(weather[hhday-1])]
            hhday += 1
    return consume_water,consume_food,hhday

base_water_price=5
base_water_weight=3
base_food_price=10
base_food_weight=2

def possess_c(cur_water,cur_food,cur_money,cur_day,log):
    can_take=1200-cur_water*3-cur_food*2
    while can_take>0 and cur_money>0:
        can_take-=2*base_water_weight
        can_take-=base_food_weight
        cur_money-=2*base_water_price
        cur_money-=base_food_weight
        cur_food+=1
        cur_water+=2

    can_take += 2 * base_water_weight
    can_take += base_food_weight
    cur_money += 2 * base_water_price
    cur_money += base_food_weight
    cur_food -= 1
    cur_water -= 2

    # water_can_afford = cur_money / (base_water_price * 2 )
    #     # food_can_afford = cur_money / (base_food_price * 2)
    #     # water_can_take = can_take / (base_water_price)
    #     # food_can_take = can_take / (base_food_price)
    #     # buy=min(water_can_take,water_can_afford,food_can_take,food_can_afford)
    #     # cur_money-=(base_water_price * 2)*buy+(base_food_price * 2)*buy
    #     # cur_food+=buy
    #     # cur_water+=buy
    newlog=log+str(cur_day)+" "+"Go end\n"
    q,w,e=go(cur_day,3)
    temp_water=cur_water-q
    temp_food=cur_food-w
    possess_z(temp_water,temp_food,cur_money,e,newlog)

    newlog = log+str(cur_day)+" " + "Go Mine\n"
    q, w, e = go(cur_day, 2)
    temp_water = cur_water - q
    temp_food = cur_food - w
    posseess_k(temp_water, temp_food, cur_money, e,newlog)


log_list={}
def possess_z(cur_water,cur_food,cur_money,cur_day,log):
    print("END ",cur_water*5/2+cur_food*10/2+cur_money,cur_day)
    log+="End "+str(cur_water*5/2+cur_food*10/2+cur_money)
    log_list[log]=cur_water*5/2+cur_food*10/2+cur_money
    return cur_water*5/2+cur_food*10/2+cur_money

def posseess_k(cur_water,cur_food,cur_money,cur_day,log):
    water_limit=cur_water/(base_consume_water[get_weather(weather[cur_day-1])]*3)
    food_limit=cur_food/(base_consume_food[get_weather(weather[cur_day-1])]*3)
    total_limit=int(min(water_limit,food_limit))
    total_limit=min(total_limit,30-cur_day)
    #print(total_limit)
    for i in range(total_limit):
        temp_food=cur_food
        temp_water=cur_water
        temp_day=cur_day
        for j in range(i+1):
            temp_water=temp_water-base_consume_water[get_weather(weather[cur_day+j-1])]*3
            temp_food=temp_food-base_consume_food[get_weather(weather[cur_day+j-1])]*3
            temp_day+=1
        newlog=log+str(temp_day)+" "+"Dig "+str(i+1)+" Day\n"
        q,w,e=go(temp_day,5)
        if q<0:
            continue
        temp_water-=q
        temp_food-=w
        temp_money=1000* (i+1) +cur_money
        newlog+="Go end "
        possess_z(temp_water,temp_food,temp_money,e,newlog)

        newlog = log+str(temp_day)+" " + "Dig " + str(i + 1) + " Day\n"
        q, w, e = go(temp_day, 2)
        if q < 0:
            continue
        temp_water -= q
        temp_food -= w
        temp_money = 1000 * (i+1) + cur_money
        newlog += "Go village\n"
        possess_c(temp_water, temp_food, temp_money, e,newlog)


q,w,e=go(1,6)
log=""

possess_c(init_water-q,init_food-w,money,e,log)

max=-1
max_index=0
for i in log_list:
    if log_list[i]>max:
        max=log_list[i]
        max_index=i
print(max_index)

import matplotlib.pyplot as plt

index=0
x=[]
y=[]
for i in log_list:
    x.append(index)
    index+=1
    y.append(log_list[i])

plt.scatter(x, y, alpha=0.6)
plt.show()
