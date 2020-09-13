Map = []
Set_strategy=[1,2,7,8,13,14,15,20,25]
Set_strategy2=[1,2,7,12,13,14,19,24,25]
class Node:
    def __init__(self, id, state, nodes):
        self.id = id
        self.state = state
        self.neibor = []
        for i in nodes:
            self.neibor.append(i)


class Log:
    def __init__(self, time, pos, action, money, water, food):
        self.time = time
        self.pos = pos
        self.action = action
        self.money = money
        self.water = water
        self.food = food

    def display(self):
        print("Day: " + str(self.time) + " At: " + str(self.pos) + " Money: " + str(self.money) + " water " + str(
            self.water) + " food " + str(self.food) + " " + self.action)


def build_map():
    fp = open("Map6.txt", 'r')
    node_id = 1
    for i in fp:
        if i != None:
            i = i.split()
            temp_state = i[0]
            temp_list = []
            for j in range(1, len(i)):
                temp_list.append(int(i[j]))
            temp_node = Node(node_id, temp_state, temp_list)
            Map.append(temp_node)
            node_id += 1


# 晴朗 高温 沙暴
import random

weather = ["高温", "高温", "晴朗", "晴朗", "晴朗",
           "高温", "沙暴", "晴朗", "高温", "高温",
           "高温", "高温", "晴朗", "高温", "高温",
           "高温", "晴朗", "晴朗", "高温", "高温",
           "晴朗", "晴朗", "高温", "晴朗", "晴朗",
           "高温", "晴朗", "晴朗", "高温", "高温"
           ]

TotalTake = 1200
init_money = 10000
base_water_price = 5
base_water_weight = 3
base_food_price = 10
base_food_weight = 2

base_consume_water = [3, 9, 10]
base_consume_food = [4, 9, 10]

import random


def check(i, j, can_take, canafford):
    use_money = (i * 2 * base_water_price + j * 2 * base_food_price)
    use_weight = (i * base_water_weight + j * base_food_weight)
    if use_money > canafford or use_weight > can_take:
        return False
    else:
        return True


# 这个函数作为一个机器人已经决定要从当前位置移动到下一个位置的决策过程
def Just_Go(cur_time, cur_money, cur_water, cur_food, cur_node,meet):
    if cur_time >= 30:
        return 0
    if weather[cur_time] == "沙暴":
        return MonteCarloRobot(cur_time + 1, cur_money, cur_water - base_consume_water[2],
                               cur_food - base_consume_food[2], cur_node)
    if weather[cur_time] == "高温":
        neigh = Map[cur_node - 1].neibor
        ret = random.randint(0, len(neigh) - 1)
        return MonteCarloRobot(cur_time + 1, cur_money, cur_water - base_consume_water[1] * 2 * meet,
                               cur_food - base_consume_food[1] * 2 * meet, neigh[ret])
    if weather[cur_time] == "晴朗":
        neigh = Map[cur_node - 1].neibor
        ret = random.randint(0, len(neigh) - 1)
        return MonteCarloRobot(cur_time + 1, cur_money, cur_water - base_consume_water[0] * 2* meet,
                               cur_food - base_consume_food[0] * 2* meet, neigh[ret])
    else:
        print("Hit Error !!!!!!!!!!!!!!!!!!")
        exit()
        return


def MonteCarloRobot(cur_time, cur_money, cur_water, cur_food, cur_node, last_state=0):
    cur_state = Map[cur_node - 1].state
    if cur_time>=len(Set_strategy):
        Player2_pos=25
        Player3_pos=25
    else:
        Player2_pos=Set_strategy[cur_time]
        Player3_pos=Set_strategy2[cur_time]
    meet=1
    if Player2_pos==cur_node:
        meet+=1
    else:
        if Player3_pos==cur_node:
            meet+=1
    if cur_water < 0 or cur_food < 0:
        # print("No food or water And Dead")
        return 0
    if cur_time > 30:
        # print("Out of Time Dead")
        return 0
    if cur_state == 'z':
        # print("get End point with Money",cur_money+cur_food*base_food_price/2+cur_water*base_water_price/2)
        # return cur_money+cur_food*base_food_price/2+cur_water*base_water_price/2
        return cur_money
    if cur_state == 'p' or cur_state == 's':
        return Just_Go(cur_time, cur_money, cur_water, cur_food, cur_node,meet)

    if cur_state == 'k':
        ret = random.randint(0, 2)
        if ret == 0:  # 不挖矿 直接离开
            return Just_Go(cur_time, cur_money, cur_water, cur_food, cur_node,meet)
        else:
            if last_state == 1:
                temp = MonteCarloRobot(cur_time + 1, cur_money + (1000/meet), cur_water - base_consume_water[0] * 3,
                                       cur_food - base_consume_food[0] * 3, cur_node, 1)
            else:
                temp = MonteCarloRobot(cur_time + 1, cur_money, cur_water - base_consume_water[0],
                                       cur_food - base_consume_food[0], cur_node, 1)
            # if temp!=0:
            # print("Hit herre")
            # print(temp)
            return temp

    if cur_state == 'c':
        cur_take = cur_water * base_water_weight + cur_food * base_food_weight
        can_take = TotalTake - cur_take
        water_can_afford = cur_money / (base_water_price * 2)
        food_can_afford = cur_money / (base_food_price * 2)
        water_can_take = can_take / (base_water_price)
        food_can_take = can_take / (base_food_price)

        water_can_buy = int(min(water_can_afford, water_can_take))
        food_can_buy = int(min(food_can_afford, food_can_take))
        if water_can_buy <= 0:
            random_water = 0
        else:
            random_water = random.randint(0, water_can_buy)
        if food_can_buy <= 0:
            random_food = 0
        else:
            random_food = random.randint(0, food_can_buy)

        use_money = (random_water * 2 * base_water_price + random_food * 2 * base_food_price)
        use_weight = (random_water * base_water_weight + random_food * base_food_weight)

        if use_money > cur_money or use_weight > can_take:
            return Just_Go(cur_time, cur_money, cur_water, cur_food, cur_node,meet)
        else:
            # 带着新买的物资走
            return Just_Go(cur_time, cur_money - use_money, cur_water + random_water, cur_food + random_food, cur_node,meet)


from Draw import Draw

Decide_List = []


def monte_move(cur_time, cur_money, cur_water, cur_food, cur_node, try_time):
    neigh = Map[cur_node - 1].neibor
    best_score = -1
    best_choice = neigh[0]

    for i in neigh:
        Money_sum = 0
        real = 1
        for _ in range(try_time):
            tempmoney = MonteCarloRobot(cur_time + 1, cur_money, cur_water - base_consume_water[0] * 2,
                                        cur_food - base_consume_food[0] * 2, i)
            Money_sum += tempmoney
            if tempmoney != 0:
                real += 1
        #print(Money_sum)
        Money_sum /= real

        if Money_sum > best_score:
            best_choice = i
            best_score = Money_sum
        print("At ", cur_node, " to ", i, " ", Money_sum)
    return best_choice, best_score


def monte_dig(cur_time, cur_money, cur_water, cur_food, cur_node, try_time):
    Money_sum = 0
    real = 1
    for _ in range(try_time):
        temp = MonteCarloRobot(cur_time + 1, cur_money + 1000, cur_water - base_consume_water[0] * 3,
                               cur_food - base_consume_food[0] * 3, cur_node)
        if temp != 0:
            real += 1
        Money_sum += temp
    Money_sum /= real
    return -1, Money_sum


def Try_Decide(cur_time, cur_money, cur_water, cur_food, cur_node, Log_list):
    #print("I am in site " + str(cur_node))
    Try_time = 2000
    cur_state = Map[cur_node - 1].state
    if cur_water < 0 or cur_food < 0:
        temp = Log(cur_time, cur_node, "Dead", cur_money, cur_water, cur_food)
        Log_list.append(temp)
        return
    if cur_time >= 30:
        temp = Log(cur_time, cur_node, "Timeout", cur_money, cur_water, cur_food)
        Log_list.append(temp)
        return

    if cur_state == 'z':
        temp = Log(cur_time, cur_node, "Reach",
                   cur_money + cur_food * base_food_price / 2 + cur_water * base_water_price / 2, cur_water, cur_food)
        Log_list.append(temp)
        return (cur_time,cur_money + cur_food * base_food_price / 2 + cur_water * base_water_price / 2,0,0,cur_node)

    if cur_state == 'p' or cur_state == 's':
        best_choice, best_score = monte_move(cur_time, cur_money, cur_water, cur_food, cur_node, Try_time)
        temp = Log(cur_time, cur_node, "Move" + str(best_choice), cur_money, cur_water, cur_food)
        Log_list.append(temp)
        return (cur_time + 1,cur_money, cur_water - base_consume_water[0] * 2,cur_food - base_consume_food[0] * 2,best_choice)
        # Try_Decide(cur_time + 1, cur_money, cur_water - base_consume_water[0] * 2,
        #                   cur_food - base_consume_food[0] * 2, best_choice, Log_list)

    if cur_state == 'k':
        best_choice, best_score = monte_move(cur_time, cur_money, cur_water, cur_food, cur_node, Try_time)
        _, dig_score = monte_dig(cur_time, cur_money, cur_water, cur_food, cur_node, Try_time)
        print("Stay And Dig", dig_score)
        if dig_score > best_score:
            best_choice = -1
            best_score = dig_score

        if best_choice == -1:
            temp = Log(cur_time, cur_node, "Dig", cur_money, cur_water, cur_food)
            Log_list.append(temp)
            if len(Log_list) > 2 and Log_list[-2].action == "Dig":
                return (cur_time + 1, cur_money + 1000, cur_water - base_consume_water[0] * 4,cur_food - base_consume_food[0] * 4, cur_node)
                # Try_Decide(cur_time + 1, cur_money + 1000, cur_water - base_consume_water[0] * 4,
                #                   cur_food - base_consume_food[0] * 4, cur_node, Log_list)
            else:
                return (cur_time + 2, cur_money + 1000, cur_water - base_consume_water[0] * 4,cur_food - base_consume_food[0] * 4, cur_node)
                # Try_Decide(cur_time + 2, cur_money + 1000, cur_water - base_consume_water[0] * 4,
                #                   cur_food - base_consume_food[0] * 4, cur_node, Log_list)
        else:
            temp = Log(cur_time, cur_node, "Move" + str(best_choice), cur_money, cur_water, cur_food)
            Log_list.append(temp)
            return (cur_time + 1, cur_money, cur_water - base_consume_water[0] * 2, cur_food - base_consume_food[0] * 2, best_choice)
            # Try_Decide(cur_time + 1, cur_money, cur_water - base_consume_water[0] * 2,
            #                   cur_food - base_consume_food[0] * 2, best_choice, Log_list)

    if cur_state == 'c':
        cur_take = cur_water * base_water_weight + cur_food * base_food_weight
        can_take = TotalTake - cur_take
        water_can_afford = cur_money / (base_water_price * 2)
        food_can_afford = cur_money / (base_food_price * 2)
        water_can_take = can_take / (base_water_price)
        food_can_take = can_take / (base_food_price)

        water_can_buy = min(water_can_afford, water_can_take)
        food_can_buy = min(food_can_afford, food_can_take)
        best_choice = [0, 0]
        best_score = 0
        for i in range(int(water_can_buy)):
            for j in range(int(food_can_buy)):
                Money_sum = 0
                if check(i, j, can_take, cur_money):
                    use_money = (i * 2 * base_water_price + j * 2 * base_food_price)
                    temp_try=int(Try_time/1000)
                    for l in range( temp_try):
                        Money_sum += MonteCarloRobot(cur_time, cur_money - use_money, cur_water, cur_food, cur_node)
                    Money_sum /= Try_time
                    if Money_sum > best_score:
                        best_score = Money_sum
                        best_choice[0] = i
                        best_choice[1] = j

        use_money = (best_choice[0] * 2 * base_water_price + best_choice[1] * 2 * base_food_price)
        cur_money -= use_money
        cur_water += best_choice[0]
        cur_food += best_choice[1]
        temp = Log(cur_time, cur_node, "Buy", cur_money, cur_water, cur_food)
        Log_list.append(temp)

        best_choice, best_score = monte_move(cur_time, cur_money, cur_water, cur_food, cur_node, Try_time)
        temp = Log(cur_time, cur_node, "Move" + str(best_choice), cur_money, cur_water, cur_food)
        Log_list.append(temp)
        return (cur_time + 1, cur_money, cur_water - base_consume_water[0] * 2, cur_food - base_consume_food[0] * 2, best_choice)
        #Try_Decide(cur_time + 1, cur_money, cur_water - base_consume_water[0] * 2, cur_food - base_consume_food[0] * 2, best_choice, Log_list)


def Player(cur_time , cur_money, cur_water, cur_food , cur_node):
    Log_List=[]
    old_state=(cur_time , cur_money, cur_water, cur_food , cur_node)
    while 1:
        # if old_state[4]==25:
        #     break
        new_state=Try_Decide(old_state[0],old_state[1], old_state[2], old_state[3] , old_state[4],Log_List)
        #print(old_state," ",new_state)
        if new_state == None:
            return 0
        if old_state[4]==25:
            break
        old_state=new_state
    for i in Log_List:
        i.display()
    return old_state[1]


choose=[ "晴朗", "高温", "沙暴",]
def init_weather(i,j):
    Sunny=i
    Hot=i+j
    Storm=i+j
    temp_weather=[]
    for i in range(30):
        p=(random.randint(0, 1000))
        choice=0
        if p<Sunny:
            choice=0
        if p>Sunny and p <=Hot:
            choice=1
        if p>Hot:
            choice=2
        temp_weather.append(choose[choice])
    global weather
    weather=temp_weather

def RunGame():
    # T=len(weather)
    # print("Start")
    # Money_sum=0
    # try_time=100000
    # money_list=[]
    # for i in range(try_time):
    #     Money_sum+=MonteCarloRobot(0,2000800,400,1)
    #     money_list.append(Money_sum/(i+1))
    # Draw([money_list], ["测试"], range(len(money_list)), "蒙特卡罗模拟沙漠穿越")
    # print("Average Money",Money_sum/try_time)
    # results=[]
    # result=[]
    # total=0
    # i=0
    # while len(result)!=10:
    #     i+=1
    #     f = 200
    #     w = 200
    #     init_weather(700,250)
    #     rest_money = init_money - (base_food_price * f + base_water_price * w)
    #     temp=Player(0, rest_money, w, f, 1)
    #     if temp==0:
    #         continue
    #     else:
    #         total+=temp
    #         result.append(total/(i))
    #
    # results.append(result)
    #
    # result=[]
    # total=0
    # i=0
    # while len(result)!=10:
    #     i+=1
    #     f = 200
    #     w = 200
    #     init_weather(500,450)
    #     rest_money = init_money - (base_food_price * f + base_water_price * w)
    #     temp = Player(0, rest_money, w, f, 1)
    #     if temp == 0:
    #         continue
    #     else:
    #         total += temp
    #         result.append(total / (i))
    # results.append(result)
    # Draw(results,["0.7+0.25+0.05","0.5+0.45+0.05"],range(len(result)),"不同天气下的决策收益")
    # # for i in best_decide:
    # #     i.display()
    f = 200
    w = 200
    init_weather(700,250)
    rest_money = init_money - (base_food_price * f + base_water_price * w)
    Player(0, rest_money, w, f, 1)
build_map()
RunGame()