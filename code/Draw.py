import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator
import seaborn as sns
from matplotlib.font_manager import FontProperties

#{darkgrid, whitegrid, dark, white, ticks}
#{deep, muted, bright, pastel, dark, colorblind}
sns.set(context='notebook', style='whitegrid', palette='colorblind', font='sans-serif', font_scale=1, color_codes=False, rc=None)

plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号
#families=[ 'fantasy','Tahoma', 'monospace','Times New Roman']

def Draw(Lines,Names,index,Title,Colors=None):
    if Colors==None:
        Colors=['lightseagreen','orange','red','darkblue','green' ]
    plt.rcParams['figure.figsize'] = (12.0, 7.0)
    for i in range(len(Lines)):
        plt.plot(index,Lines[i],Colors[i],label=Names[i],linewidth=0.8)

    English=0
    if English:
        Title_font = {'family': 'fantasy', 'size': 20}
    else:
        Title_font = {'family': "STXinwei", 'size': 20}
    plt.title(Title, Title_font)

    if English:
        font1 = {'family': 'Tahoma','size': 14}
    else:
        font1 = {'family': "FangSong", 'size': 14}
    plt.xlabel('决策概率/‰', font1)
    plt.ylabel('期望收益/元', font1,rotation=90)
    plt.legend()

    show_num=20
    x_len=len(index)/show_num
    x_major_locator = MultipleLocator(x_len)
    ax = plt.gca()
    ax.xaxis.set_major_locator(x_major_locator)
    plt.show()

def test():
    X = np.linspace(-np.pi, np.pi, 256, endpoint=True)
    C,S = np.cos(X), np.sin(X)
    Draw([C,S],['Cos','Sin'],X,"Test")
    DrawLineWithSeaBorn([C,S],['Cos','Sin'],X,"Sin And Cos")

import pandas as pd
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
def DrawLineWithSeaBorn(Lines,Names,index,Title):
    #index = pd.date_range("1 1 2000", periods=100,freq="m", name="date")
    Lines=np.array(Lines)
    Lines=np.transpose(Lines)
    print(Lines[:,1])
    wide_df = pd.DataFrame(Lines, index, Names)
    print(wide_df)
    f, ax = plt.subplots(figsize=(12.0, 7.0))
    ax.set_title(Title, fontsize=22, position=(0.5, 1.05))
    #ax.invert_yaxis()
    ax.set_xlabel('X Label', fontsize=18)
    ax.set_ylabel('Y Label', fontsize=18)
    sns.lineplot(data=wide_df)
    plt.show()

def DrawBarWithSeaBorn(datas,names,title):
    data={}
    for i in range(len(datas)):
        data[names[i]]=datas[i]
    wide_df = pd.DataFrame(data)
    print(wide_df)
    #sns.barplot(x="color",y="age",data=wide_df,hue="gender")
    sns.barplot(x="color", y="age", palette="Set3",data=wide_df)
    plt.show()


def test2():
    color = ['green', 'red', 'green', 'blue', 'blue']
    gender = ['男', '女', '女', '男', '男']
    age = [55, 35, 35, 81, 45]
    DrawBarWithSeaBorn([age,color,gender],['age','color','gender'],"Test")


'''
import pandas as pd
import seaborn as sns

df = pd.DataFrame({'a' : ['a', 'b' , 'b', 'a'], 'b' : [5, 6, 4, 3] })

# horizontal boxplots
sns.boxplot(x="b", y="a", data=df, orient='h')
plt.show()
# vertical boxplots
sns.boxplot(x="a", y="b", data=df, orient='v')
plt.show()
'''