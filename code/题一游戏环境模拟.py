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
print(len(weather))
TotalTake=1200
init_money=10000
base_water_price=5
base_water_weight=3
base_food_price=10
base_food_weight=2

base_consume_water=[5,8,10]
base_consume_food=[7,6,10]

import random

def check(i,j,can_take,canafford):
    use_money = (i * 2 * base_water_price + j * 2 * base_food_price)
    use_weight = (i * base_water_weight + j * base_food_weight)
    if use_money > cur_money or use_weight > can_take:
        return False
    else:
        return True

# 这个函数作为一个机器人已经决定要从当前位置移动到下一个位置的决策过程
def Just_Go(cur_time,cur_money,cur_water,cur_food,cur_node):
    if cur_time>=30:
        return 0
    if weather[cur_time] == "沙暴":
        return MonteCarloRobot(cur_time + 1, cur_money, cur_water - base_consume_water[2],cur_food - base_consume_food[2], cur_node)
    if weather[cur_time] == "高温":
        neigh = Map[cur_node - 1].neibor
        ret = random.randint(0, len(neigh) - 1)
        return MonteCarloRobot(cur_time + 1, cur_money, cur_water - base_consume_water[1] * 2,cur_food - base_consume_food[1] * 2, neigh[ret])
    if weather[cur_time] == "晴朗":
        neigh = Map[cur_node - 1].neibor
        ret = random.randint(0, len(neigh) - 1)
        return MonteCarloRobot(cur_time + 1, cur_money, cur_water - base_consume_water[0] * 2, cur_food - base_consume_food[0] * 2, neigh[ret])
    else:
        print("Hit Error !!!!!!!!!!!!!!!!!!")
        return

def MonteCarloRobot(cur_time,cur_money,cur_water,cur_food,cur_node):
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
        return Just_Go(cur_time,cur_money,cur_water,cur_food,cur_node)

    if cur_state == 'k':
        ret = random.randint(0, 1)
        if ret == 0:# 不挖矿 直接离开
            return Just_Go(cur_time,cur_money,cur_water,cur_food,cur_node)
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
            return Just_Go(cur_time, cur_money, cur_water, cur_food, cur_node)
        else:
            # 带着新买的物资走
            return Just_Go(cur_time,cur_money-use_money,cur_water+random_water,cur_food+random_food,cur_node)




from Draw import Draw

Decide_List=[]

def Try_Decide(cur_time,cur_money,cur_water,cur_food,cur_node):
    print("I am in site "+str(cur_node))
    Try_time=10000
    cur_state = Map[cur_node - 1].state
    if cur_water < 0 or cur_food < 0:
        Decide_List.append("No food or water And Dead")
        return 0
    if cur_time >= 30:
        Decide_List.append("Out of Time Dead")
        return 0
    if cur_state == 'z':
        Decide_List.append("get End point with All money "+str(cur_money + cur_food * base_food_price / 2 + cur_water * base_water_price / 2))
        return cur_money + cur_food * base_food_price / 2 + cur_water * base_water_price / 2

    if cur_state == 'p' or 's':
        neigh = Map[cur_node - 1].neibor
        best_score=-1
        best_choice=neigh[0]
        for i in neigh:
            Money_sum = 0
            for _ in range(Try_time):
                Money_sum+=MonteCarloRobot(cur_time + 1, cur_money, cur_water - base_consume_water[0] * 2,cur_food - base_consume_food[0] * 2, i)
            Money_sum/=Try_time
            if Money_sum>best_score:
                best_choice=i
                best_score=Money_sum
            print("i am in "+str(cur_node)+"money  "+str(Money_sum)+"  to "+str(i)+" money "+str(cur_money))
        Decide_List.append("from"+str(cur_node)+"to"+str(best_choice))
        return Try_Decide(cur_time + 1, cur_money, cur_water - base_consume_water[0] * 2,cur_food - base_consume_food[0] * 2, best_choice)
    if cur_state == 'k':
        neigh = Map[cur_node - 1].neibor
        best_score = -1
        best_choice = neigh[0]
        for i in neigh:
            Money_sum = 0
            for _ in range(Try_time):
                Money_sum += MonteCarloRobot(cur_time + 1, cur_money, cur_water - base_consume_water[0] * 2,
                                             cur_food - base_consume_food[0] * 2, i)
            Money_sum /= Try_time
            if Money_sum > best_score:
                best_choice = i
                best_score = Money_sum

        Money_sum = 0
        for _ in range(Try_time):
            Money_sum += MonteCarloRobot(cur_time + 2, cur_money+1000, cur_water-base_consume_water[0]*3,cur_food-base_consume_food[0]*3,cur_node)
        Money_sum /= Try_time
        if Money_sum > best_score:
            best_choice = -1
            best_score = Money_sum

        if best_choice==-1:
            Decide_List.append("Dig Mine at Day " + str(cur_time)+" money "+str(cur_money))
            return Try_Decide(cur_time + 2, cur_money+1000, cur_water-base_consume_water[0]*4,cur_food-base_consume_food[0]*4,cur_node)
        else:
            Decide_List.append("from" + str(cur_node) + "to" + str(best_choice)+" money "+str(cur_money))
            return Try_Decide(cur_time + 1, cur_money, cur_water - base_consume_water[0] * 2,
                              cur_food - base_consume_food[0] * 2, best_choice)

    if cur_state == 'c':
        cur_take = cur_water * base_water_weight + cur_food * base_food_weight
        can_take = TotalTake - cur_take
        water_can_afford = cur_money / (base_water_price * 2)
        food_can_afford = cur_money / (base_food_price * 2)
        water_can_take = can_take / (base_water_price)
        food_can_take = can_take / (base_food_price)

        water_can_buy = min(water_can_afford, water_can_take)
        food_can_buy = min(food_can_afford, food_can_take)

        best_choice=[0,0]
        best_score=0
        for i in range(water_can_buy):
            for j in range(food_can_buy):
                Money_sum=0
                if check(i,j,can_take,cur_money):
                    use_money=(i * 2 * base_water_price + j * 2 * base_food_price)
                    for l in range(Try_time):
                        Money_sum += MonteCarloRobot(cur_time , cur_money-use_money , cur_water ,cur_food , cur_node)
                    Money_sum /= Try_time
                    if Money_sum>best_score:
                        best_score=Money_sum
                        best_choice[0]=i
                        best_choice[1]=j
        Decide_List.append("Buy water and food"+str(best_choice[0])+"  "+str(best_choice[1])+" money "+str(cur_money))
        use_money = (best_choice[0] * 2 * base_water_price + best_choice[1] * 2 * base_food_price)
        neigh = Map[cur_node - 1].neibor
        best_score = -1
        best_choice = neigh[0]
        for i in neigh:
            Money_sum = 0
            for _ in range(Try_time):
                Money_sum += MonteCarloRobot(ccur_time + 1, cur_money-use_money, cur_water - base_consume_water[0] * 2 + best_choice[0],cur_food - base_consume_food[0] * 2+best_choice[1], i)
            Money_sum /= Try_time
            if Money_sum > best_score:
                best_choice = i
                best_score = Money_sum
        Decide_List.append("from" + str(cur_node) + "to" + str(best_choice)+" money "+str(cur_money))
        return Try_Decide(cur_time + 1, cur_money-use_money, cur_water - base_consume_water[0] * 2 + best_choice[0],cur_food - base_consume_food[0] * 2+best_choice[1], best_choice)


def RunGame():
    # T=len(weather)
    # print("Start")
    # Money_sum=0
    # try_time=100000
    # money_list=[]
    # for i in range(try_time):
    #     Money_sum+=MonteCarloRobot(0,2000,800,400,1)
    #     money_list.append(Money_sum/(i+1))
    # Draw([money_list], ["测试"], range(len(money_list)), "蒙特卡罗模拟沙漠穿越")
    # print("Average Money",Money_sum/try_time)
    Try_Decide(0,2000,800,400,1)
    print(Decide_List)

build_map()
RunGame()