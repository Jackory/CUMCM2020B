
class Node:
    def __init__(self,id,state,nodes):
        self.id=id
        self.state=state
        self.neibor=nodes

temp=[
    [2,9],
    [1,3,9,10],
    [2,10,11,4],
    [3,11,12,5],
    [4,12,13,6],
    [5,13,14,7],
    [6,14,15,8],
    [7,15,16],
    [1,2,17,18],
    [2,3,9,11,18,19],
    [3,4,10,12,19,20],
    [4,5,11,13,20,21],
    [5,6,12,14,21,22],
    [6,7,13,15,22,23],
    [7,8,14,16,23,24],
    [8,15,24]
]


node=[]

temp2=[]
for i in temp:
    temptemp=[]
    for j in i:
        temptemp.append(j+16)
    temp2.append(temptemp)

for i in temp2:
    temp.append(i)
print(temp)

temp2=[]
for i in temp:
    temptemp=[]
    for j in i:
        temptemp.append(j+32)
    temp2.append(temptemp)
print(len(temp2))
for i in temp2:
    temp.append(i)

print(temp)
for i in range(len(temp)):
    node.append(Node((i+1),'p',temp[i]))
node[0].state='s'
node[29].state='k'
node[38].state='c'
node[54].state='k'
node[61].state='c'
node[63].state='z'


file_write_obj = open("Map2.txt", 'w')
for var in node:
    file_write_obj.writelines(var.state)
    for i in var.neibor:
        file_write_obj.writelines( " "+str(i))
    file_write_obj.write('\n')
file_write_obj.close()
