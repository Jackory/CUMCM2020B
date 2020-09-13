from mc_map3 import *


# 值
def analysis1():
    E1 = []
    E2 = []
    E3 = []
    E4 = []
    E5 = []
    # ---------------求稳态收敛值
    print('Start')
    iter1 = 1000
    iter2 = 100
    returns = []
    sum_money = 0
    for k in range(iter1):
        money_list = []
        for i in range(iter2):
            states=[]
            weather = [-1]
            weather.extend([np.random.choice(np.arange(0,2),p=[0.4,0.6]) for _ in range(10)])
            sum_money = MC(1,0,9190,54,54,states,map1,weather)
            money_list.append(sum_money)
        returns.append(max(money_list))
        E1.append(sum(returns)/(k+1))
    
    returns = []
    sum_money = 0
    for k in range(iter1):
        money_list = []
        for i in range(iter2):
            states=[]
            weather = [-1]
            weather.extend([np.random.choice(np.arange(0,2),p=[0.45,0.55]) for _ in range(10)])
            sum_money = MC(1,0,9190,54,54,states,map1,weather)
            money_list.append(sum_money)
        returns.append(max(money_list))
        E2.append(sum(returns)/(k+1))

    returns = []
    sum_money = 0
    for k in range(iter1):
        money_list = []
        for i in range(iter2):
            states=[]
            weather = [-1]
            weather.extend([np.random.choice(np.arange(0,2),p=[0.5,0.5]) for _ in range(10)])
            sum_money = MC(1,0,9190,54,54,states,map1,weather)
            money_list.append(sum_money)
        returns.append(max(money_list))
        E3.append(sum(returns)/(k+1))

    returns = []
    sum_money = 0
    for k in range(iter1):
        money_list = []
        for i in range(iter2):
            states=[]
            weather = [-1]
            weather.extend([np.random.choice(np.arange(0,2),p=[0.35,0.65]) for _ in range(10)])
            sum_money = MC(1,0,9190,54,54,states,map1,weather)
            money_list.append(sum_money)
        returns.append(max(money_list))
        E4.append(sum(returns)/(k+1))
    returns = []
    sum_money = 0
    for k in range(iter1):
        money_list = []
        for i in range(iter2):
            states=[]
            weather = [-1]
            weather.extend([np.random.choice(np.arange(0,2),p=[0.3,0.7]) for _ in range(10)])
            sum_money = MC(1,0,9190,54,54,states,map1,weather)
            money_list.append(sum_money)
        returns.append(max(money_list))
        E5.append(sum(returns)/(k+1))

    Draw([E1,E2,E3,E4,E5],['E1','E2','E3','E4','E5'],range(len(E1)),"")

def analysis2():
    E1 = []
    E2 = []
    E3 = []
    E4 = []
    E5 = []
    # ---------------求稳态收敛值
    print('Start')
    iter1 = 1000
    iter2 = 100
    returns = []
    sum_money = 0
    for k in range(iter1):
        money_list = []
        for i in range(iter2):
            states=[]
            weather = [-1]
            weather.extend([np.random.choice(np.arange(0,2),p=[0.4,0.6]) for _ in range(10)])
            sum_money = MC(1,0,6400,240,240,states,map2,weather)
            money_list.append(sum_money)
        returns.append(max(money_list))
        E1.append(sum(returns)/(k+1))
    
    returns = []
    sum_money = 0
    for k in range(iter1):
        money_list = []
        for i in range(iter2):
            states=[]
            weather = [-1]
            weather.extend([np.random.choice(np.arange(0,2),p=[0.45,0.55]) for _ in range(10)])
            sum_money = MC(1,0,6400,240,240,states,map2,weather)
            money_list.append(sum_money)
        returns.append(max(money_list))
        E2.append(sum(returns)/(k+1))

    returns = []
    sum_money = 0
    for k in range(iter1):
        money_list = []
        for i in range(iter2):
            states=[]
            weather = [-1]
            weather.extend([np.random.choice(np.arange(0,2),p=[0.5,0.5]) for _ in range(10)])
            sum_money = MC(1,0,6400,240,240,states,map2,weather)
            money_list.append(sum_money)
        returns.append(max(money_list))
        E3.append(sum(returns)/(k+1))

    returns = []
    sum_money = 0
    for k in range(iter1):
        money_list = []
        for i in range(iter2):
            states=[]
            weather = [-1]
            weather.extend([np.random.choice(np.arange(0,2),p=[0.35,0.65]) for _ in range(10)])
            sum_money = MC(1,0,6400,240,240,states,map2,weather)
            money_list.append(sum_money)
        returns.append(max(money_list))
        E4.append(sum(returns)/(k+1))
    returns = []
    sum_money = 0
    for k in range(iter1):
        money_list = []
        for i in range(iter2):
            states=[]
            weather = [-1]
            weather.extend([np.random.choice(np.arange(0,2),p=[0.3,0.7]) for _ in range(10)])
            sum_money = MC(1,0,6400,240,240,states,map2,weather)
            money_list.append(sum_money)
        returns.append(max(money_list))
        E5.append(sum(returns)/(k+1))

    Draw([E1,E2,E3,E4,E5],['E1','E2','E3','E4','E5'],range(len(E1)),"")

if __name__ == "__main__":
    # 直奔终点
    analysis1()
    # 先到矿山
    analysis2()
