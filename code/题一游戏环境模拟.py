Map=[]

class Node:
    def __init__(self,id,state,nodes):
        self.id=id
        self.state=state
        self.neibor=[]
        for i in nodes:
            self.neibor.append(i)

def build_map():
    fp = open("Map1.txt",'r')
    node_id=1
    for i in fp:
        if i !=None:
            i=i.split()
            temp_state=i[0]
            temp_list=[]
            for j in range(1,len(i)):
                temp_list.append(int(i[j]))
            temp_node=Node(node_id,temp_state,temp_list)
            Map.append(temp_node)
            node_id+=1



# 晴朗 高温 沙暴
weather=["高温","高温","晴朗","沙暴","晴朗",
         "高温","沙暴","晴朗","高温","高温",
         "沙暴","高温","晴朗","高温","高温",
         "高温","沙暴","沙暴","高温","高温",
         "晴朗","晴朗","高温","晴朗","沙暴",
         "高温","晴朗","晴朗","高温","高温"
         ]

TotalTake=1200
init_money=10000
base_water_price=5
base_water_weight=3
base_food_price=10
base_food_weight=2

base_consume_water=[5,8,10]
base_consume_food=[7,6,10]

import random

def check(id):
    if id>1000:
        print("Hit !!!!!",id)
        exit()

def MonteCarloRobot(cur_time,cur_money,cur_water,cur_food,cur_node):
    check(cur_node)
    cur_state=Map[cur_node-1].state
    if cur_water<0 or cur_food <0 :
        #print("No food or water And Dead")
        return 0
    if cur_time>30:
        #print("Out of Time Dead")
        return 0
    if cur_state == 'z':
        #print("get End point with Money",cur_money+cur_food*base_food_price/2+cur_water*base_water_price/2)
        return cur_money+cur_food*base_food_price/2+cur_water*base_water_price/2

    if cur_state == 'p' or 's':
        check(cur_node-1)
        neigh=Map[cur_node-1].neibor
        ret = random.randint(0, len(neigh)-1)
        return MonteCarloRobot(cur_time+1,cur_money,cur_water-base_consume_water[0]*2,cur_food-base_consume_food[0]*2,neigh[ret])
    if cur_state == 'k':
        ret = random.randint(0, 1)
        if ret == 0:# 不挖矿 直接离开
            check(cur_node-1)
            neigh = Map[cur_node-1].neibor
            ret = random.randint(0, len(neigh) - 1)
            return MonteCarloRobot(cur_time+1,cur_money,cur_water-base_consume_water[0]*2,cur_food-base_consume_food[0]*2,neigh[ret])
        else:
            print("挖到矿了！！！！！！！！！！！！！！！！！！！！！！！")
            return MonteCarloRobot(cur_time + 2, cur_money+1000, cur_water-base_consume_water[0]*3,cur_food-base_consume_food[0]*3,cur_node)
    if cur_state == 'c':
        cur_take=cur_water*base_water_weight+cur_food*base_food_weight
        can_take= TotalTake-cur_take
        water_can_afford = cur_money/(base_water_price*2)
        food_can_afford = cur_money/(base_food_price * 2)
        water_can_take = can_take / (base_water_price)
        food_can_take = can_take / (base_food_price )

        water_can_buy=min(water_can_afford,water_can_take)
        food_can_buy=min(food_can_afford,food_can_take)
        random_water=random.randint(0, water_can_buy)
        random_food = random.randint(0, food_can_buy)

        use_money= (random_water*2*base_water_price+random_food*2*base_food_price)
        use_weight=(random_water*base_water_weight+random_food*base_food_weight)

        if use_money>cur_money or use_weight>can_take:
            check(cur_node)
            neigh = Map[cur_node-1].neibor
            ret = random.randint(0, len(neigh) - 1)
            return MonteCarloRobot(cur_time+1,cur_money,cur_water-base_consume_water[0]*2,cur_food-base_consume_food[0]*2,neigh[ret])
        else:
            check(cur_node)
            neigh = Map[cur_node-1].neibor
            ret = random.randint(0, len(neigh) - 1)
            return MonteCarloRobot(cur_time + 1, cur_money-use_money, cur_water+random_water-base_consume_water[0]*2, cur_food+random_food-base_consume_food[0]*2, neigh[ret])



from Draw import Draw
def RunGame():
    T=len(weather)
    print("Start")
    Money_sum=0
    try_time=100000
    money_list=[]
    for i in range(try_time):
        Money_sum+=MonteCarloRobot(0,2000,800,400,1)
        money_list.append(Money_sum/(i+1))
    Draw([money_list], ["测试"], range(len(money_list)), "蒙特卡罗模拟沙漠穿越")
    print("Average Money",Money_sum/try_time)

build_map()

RunGame()