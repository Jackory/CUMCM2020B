def Test(vec,result,v0):
    visit=[]
    last_visit=0
    for i in range(len(vec)):
        visit.append(0)
    visit[v0]=1
    result[0]=0

    for i in range(len(vec)):
        for j in range(len(vec)):

            if visit[j]==0:
                dist=vec[v0][j]+last_visit
                if dist<result[j]:
                    result[j]=dist
        minIndex=0
        while visit[minIndex]==1:
            if minIndex==len(visit)-1:
                break
            minIndex+=1
        for j in range(minIndex,len(vec)):
            if visit[j]==0 and result[j]<result[minIndex]:
                minIndex=j
        last_visit=result[minIndex]
        visit[minIndex]=1
        v0=minIndex

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


def startwith(start: int, mgraph: list) -> list:
    passed = [start]
    nopass = [x for x in range(len(mgraph)) if x != start]
    dis = mgraph[start]

    while len(nopass):
        idx = nopass[0]
        for i in nopass:
            if dis[i] < dis[idx]: idx = i

        nopass.remove(idx)
        passed.append(idx)

        for i in nopass:
            if dis[idx] + mgraph[idx][i] < dis[i]: dis[i] = dis[idx] + mgraph[idx][i]
    return dis

def run():
    n=27
    vec=[]

    result=[]
    for i in range(27):
        result.append(100000000)
    for i in range(27):
        temp=[]
        for j in range(27):
            temp.append(100000000000)
        vec.append(temp)

    build_map()
    for i in Map:
        for j in i.neibor:
            vec[i.id-1][j-1]=1

    print(vec)
    print(startwith(0,vec))

run()