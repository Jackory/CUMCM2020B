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
    for i in range(20000):
        states = []
        sum_money = MC(0,0,rest,para[0],para[1],states)
        if sum_money>max_money:
            max_money=sum_money
    return max_money



def aimFunction(para):
    return realFuction(para)



T0 = 180  # initiate temperature\
T=T0
Tmin = 15  # minimum value of terperature

para=[240,240]

k = 100  # times of internal circulation
temp_y = 0  # initiate result
t = 0  # time
best=[]
best_fit=0
while T >= Tmin:
    for i in range(k):
        # calculate y
        temp_y = aimFunction(para)
        # generate a new x in the neighboorhood of x by transform function
        paraNew = [i+np.random.uniform(low=-10,high=10) for i in para]
        rest=count_restMoney(paraNew[0],paraNew[1])
        rest2=count_take(paraNew[0],paraNew[1])
        if rest<0 or rest2<0:
            continue
        yNew = aimFunction(paraNew)
        if len(best)==0:
            best_fit=yNew
            best=paraNew
        else:
            if yNew>best_fit:
                best=paraNew
                best_fit=yNew
        if yNew - temp_y > 0:
            para = paraNew
        else:
            # metropolis principle
            p = math.exp(-(yNew - temp_y) / T)
            r = np.random.uniform(low=0, high=1)
            if r > p:
                para = paraNew
        print(para,best_fit,yNew)
    t += 1
    T = T0 / math.log2(1 + t)
    print("cur T: ",T)