from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
import math
from Draw import Draw
from mc2 import MC
from mc2 import count_restMoney
from mc2 import count_take
def realFuction(para):
    rest=count_restMoney(para[0],para[1])
    max_money=-1
    for i in range(1000):
        states = []
        sum_money = MC(0,0,rest,para[0],para[1],states)
        if sum_money>max_money:
            max_money=sum_money
    return max_money



def aimFunction(para):
    return realFuction(para)

Need=[240,240]
cur_best=aimFunction(Need)
update_time=0
for i in range(10000):
    para=[np.random.uniform(low=0, high=300) for _ in range(2)]
    rest = count_restMoney(para[0], para[1])
    rest2 = count_take(para[0], para[1])
    if rest < 0 or rest2 < 0:
        continue
    temp_y = aimFunction(para)
    if temp_y - cur_best  > 0:
        Need=para
        cur_best=temp_y
        update_time+=1
        print("update!!",update_time,i,Need,cur_best)
    if i%10000==0:
        print(i/10000,"%")