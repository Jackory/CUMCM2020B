from mc_map4 import *

E1 = []
E2 = []
E3 = []
E4 = []
E5 = []
# ---------------求稳态收敛值
print('Start')
iter1 = 500
iter2 = 500
returns = []
sum_money = 0
for k in range(iter1):
    money_list = []
    for i in range(iter2):
        states=[]
        weather = [-1]
        weather.extend([np.random.choice(np.arange(0,3),p=[1/3,1/2,1/6]) for _ in range(30)])
        sum_money = MC(1,0,6400,240,240,states,weather)
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
        weather.extend([np.random.choice(np.arange(0,3),p=[8/30,17/30,5/30]) for _ in range(30)])
        sum_money = MC(1,0,6400,240,240,states,weather)
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
        weather.extend([np.random.choice(np.arange(0,3),p=[12/30,13/30,5/30]) for _ in range(30)])
        sum_money = MC(1,0,6400,240,240,states,weather)
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
        weather.extend([np.random.choice(np.arange(0,3),p=[11/30,15/30,4/30]) for _ in range(30)])
        sum_money = MC(1,0,6400,240,240,states,weather)
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
        weather.extend([np.random.choice(np.arange(0,3),p=[11/30,16/30,3/30]) for _ in range(30)])
        sum_money = MC(1,0,6400,240,240,states,weather)
        money_list.append(sum_money)
    returns.append(max(money_list))
    E5.append(sum(returns)/(k+1))

Draw([E1,E2,E3,E4,E5],['E1','E2','E3','E4','E5'],range(len(E1)),"")