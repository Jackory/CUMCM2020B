import numpy as np

cost = np.array([[1,16,12,6],
    [16,3,4,10],
    [12,4,1,6],
    [6,10,6,0]])

reward = np.array([[0,0,0,0],
         [0,1000,0,0],
         [0,0,0,0],
         [0,0,0,0]])

Qtable = np.array([[0,1,0,0],
         [0,0,0,0],
         [0,0,0,0],
         [0,0,0,0]])

eps = 0.8
gamma = 1
iteration = 100

# 0表示水，1表示食物
m = np.array([3,2]) # 物品质量
p = np.array([5,10]) # 物品价格
c = np.array([[5,8,10],[7,6,10]]) #
W = 1200 # 质量上限




def policy(s):
    if(np.random.uniform(0,1) < eps):
        return np.random.choice(len(cost))
    else:
        return np.argmax(Qtable[s,:])

returns = {}
def init():
    Qtable = np.array([[0,1,0,0],
         [0,0,0,0],
         [0,0,0,0],
         [0,0,0,0]])
    for s in range(4):
        for a in range(4):
            returns[(s,a)] = []

def train(init_s, ww,wf, M):
    states = []
    acts = []
    rs = []
    die = False
    s = init_s

    for t in range(30):
        states.append(s)
        a = policy(s)
        acts.append(a)
        r = reward[s][a]
        rs.append(r)

        ww = ww - cost[s][a] * c[0][0]
        wf = wf - cost[s][a] * c[1][0]
        #print(ww,wf)
        if ww <= 0 or wf <= 0 :
            die = True

        if (s == 1 and a == 1): # 挖矿
            M += 1000
        s = a # 状态转移

        # if(s == 2): # 村庄
        #     if(np.random.uniform(0,1) < 0.5):
        #         if(ww <= c[0][2]*cost[2][3]):
        #             ww = c[0][2]*cost[2][3]
        #             M -= (c[0][2]*cost[2][3]) * p[0]
        #         if(wf <= c[0][2]*cost[2][3]):
        #             wf = c[0][2]*cost[2][3]
        #             M -= (c[0][2]*cost[2][3] * p[1])
        #     else:
        #         wwmax = min(W/(sum(m)), M/sum(p))# 水上限
        #         wfmax = wwmax
        #         if( ww < wwmax):
        #             ww = wwmax
        #             M -= (wwmax-ww)*p[0]
        #         if(wf < wfmax):
        #             wf = wwmax
        #             M -= (wfmax-wf)*p[1]

        if s == 3:
            break
    
    length = len(states)
    value = 0
    #print(returns)
    for i in reversed(range(length)):
        s = states[i]
        a = acts[i]
        r = rs[i]
        value += gamma*value + r
        if die == False:
            print("Hit")
            #exit()
            returns[(s,a)].append(value)
        else:
            returns[(s,a)].append(0)
        Qtable[s,a] = np.mean(returns[(s,a)])
    # print(returns)
    # print("returns字典", returns[(0,1)])
    # print(Qtable)

def mc_control(init_s,ww,wf,M):
    init()
    for i in range(iteration):
        train(init_s,ww,wf,M)
    print(Qtable)
    #print("returns字典", returns[(0, 1)])

def decision():
    s = 0
    ww = 240
    wf = 240
    M = 7400
    while(s != 3):
        mc_control(s,ww,wf,M)
        #print(Qtable)
        a = np.argmax(Qtable[s,:])
 
        ww = ww - cost[s][a] * c[0][0]
        wf = wf - cost[s][a] * c[1][0]
        s = a
        print(s)
        if ww <= 0 or wf <= 0 :
            die = True
            break
    
if __name__ == "__main__":
    decision()



