import tkinter
from tkinter import StringVar
from tkinter import Entry
from tkinter import Button
from tkinter import *
import tkinter .messagebox
import numpy 
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.pylab import mpl
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
#
win = tkinter.Tk()
nowMethod = StringVar()
nowMethod.set("待选择")
nowUnknow = StringVar()
nowUnknow.set("待确定")
premissibleError = StringVar()
premissibleError.set("待确定")
#
class Application(Frame):#这个类是专门用来搞第二个窗口，画图的，为啥叫Application呢？因为我不想起名啦
    """一个经典的GUI写法"""
 #
    def __init__(self, master=None):
        '''初始化方法'''
        super().__init__(master)  # 调用父类的初始化方法，网上都这么用，我也来
        self.master = master#self
        self.pack(side=TOP, fill=BOTH, expand=1)  # 此处填充父窗体
        global nowCalNum#nowCalNum是当前迭代次数，其实运行到这里迭代结果已经出来了
        #所谓迭代次数专指折线图的x坐标，这个可参照效果图来看
        nowCalNum = 0#最开始只画x=0
        self.label = Label(self)
        #
        frm = Frame(self.label,bg='yellow')
        #
        global bt_nextCal,bt_finishCal
        #搞俩按钮，一个是点一下折线往后走一步，另一个是点完折线自己慢慢走,直到迭代次数=最大值
        bt_nextCal =  Button(frm,text='迭代一次',command=lambda:self.nextCal(),state='normal')
        bt_nextCal.pack(side=RIGHT)
        bt_finishCal = Button(frm,text='自动迭代',command=lambda:self.finishCal(),state='normal')
        bt_finishCal.pack(side=LEFT)
        frm.pack(side=TOP)
        self.label.pack()
        self.create_matplotlib()#创建一个figure，具体的在讲到它时再说
        colors = ['red','blue','green','purple','pink','dark red','dark blue','dark yellow','light purple']#封装一些颜色，便于后续区分不同x
        x_axis_data = [i for i in range(len(Xs))]#这个装的是迭代次数，也就是折线图的横坐标，从0开始，一直到Xs的长度
        y_axis_data = []#初始化折线图的y值们
        num = int(nowUnknow.get())
        for i in range(num):#用于把Xs中的值按次装入y_axis_data，运行结束后y_axis_data便是折线的纵坐标
            temp = []
            for j in Xs:
                temp.append(j[i])
            y_axis_data.append(temp)
        for i in range(num):#因为此时nowCalNum是0，所以相当于每个未知数只画了一个点
            plt.plot(x_axis_data[:nowCalNum+1],y_axis_data[i][:nowCalNum+1], 'ro-', color=colors[i%9], alpha=0.8, linewidth=1, label='x%-2d'%i)#用于在右上角标出哪条对应哪个x
        plt.legend(loc="upper right")#这个得写，不写的话右上角的标注都不显示
        #
        xTicks = [i for i in range(len(Xs)+2)]#x的刻度范围，我这里设置的是迭代次数+2，看着舒服一点
        plt.xticks(xTicks)#导入到这个图里
        yTicks = []#y的范围，我这里用的是迭代过程中x们的最小值-最大值与最小值的差的三分之一为下界（读着有点恶心),具体读代码吧
        for i in range(int(minX - (maxX - minX)/3)-1,int (maxX + (maxX - minX)/3)+1 ):
            yTicks.append(i)
        plt.yticks(yTicks)#导入图中
        plt.xlabel('迭代次数')
        plt.ylabel('未知数取值')
        ###目前已知plf可用
        #
        # 创建画布
        self.canvas = FigureCanvasTkAgg(self.figure, self)
        self.canvas.draw()#画起来
        self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)#放到第二个窗口里
#######
       ########### 
    def create_matplotlib(self):
        """创建绘图对象"""
        # 设置中文显示字体
        ##
        mpl.rcParams['font.sans-serif'] = ['SimHei']  # 中文显示，不写这行，图里的中文全是乱码
        mpl.rcParams['axes.unicode_minus'] = False  # 负号显示，不写没负号
        # 创建绘图对象f figsize的单位是英寸 像素 = 英寸*分辨率
        #创一个figure
        self.figure = plt.figure(num=2, figsize=(7, 4), dpi=80, facecolor="gold", edgecolor='green', frameon=True)
        ##
    def plotXs(self):#画图的主力！！！ 也是我卡的最久的函数
        plt.clf()#重点！ 每次画图的时候，把前边的图先清掉，不然会很恶心
        colors = ['red','blue','green','purple','pink','dark red','dark blue','dark yellow','light purple']
        #封装一些颜色
        #接下来的部分和主体"__init__"中几乎相同（或者说完全相同),唯一的变化就是nowCalNum值加一了，所以视觉上折线向前画了一步
        #下面的代码不再注释，有不懂的地方请回到__init__看注释
        x_axis_data = [i for i in range(len(Xs))]
        y_axis_data = []
        num = int(nowUnknow.get())
        for i in range(num):
            temp = []
            for j in Xs:
                temp.append(j[i])
            y_axis_data.append(temp)
        for i in range(num):    
            plt.plot(x_axis_data[:nowCalNum+1],y_axis_data[i][:nowCalNum+1], 'ro-', color=colors[i%9], alpha=0.8, linewidth=1, label='x%-2d'%i)
        plt.legend(loc="upper right")
        xTicks = [i for i in range(len(Xs)+2)]
        plt.xticks(xTicks)
        yTicks = []
        for i in range(int(minX - (maxX - minX)/3)-1,int (maxX + (maxX - minX)/3)+1 ):
            yTicks.append(i)
        plt.yticks(yTicks)
        plt.xlabel('迭代次数')
        plt.ylabel('未知数取值')
        self.canvas.draw()#最后再次调用一下draw！大功告成！
####
    def nextCal(self):#对应坐标图上“迭代一次”的功能
        global nowCalNum#得到当前迭代次数
        if nowCalNum + 1 == len(Xs):#如果当前是最大次数，就来个提示，然后返回False（一会会讲这里返回值的用处）
            tkinter .messagebox .showinfo("提示","迭代结束，共迭代%d次。"%(len(Xs)-1))
            bt_nextCal['state'] = DISABLED#迭代结束后，把“自动迭代”和“迭代一次”俩按钮禁用
            bt_finishCal['state'] = DISABLED
            return False
        nowCalNum += 1#如果不是最大次数，就+1然后进入画图的主力函数plotXs中
        self.plotXs()
        return True#画完了就return True
#
    def finishCal(self):#对应坐标图上“自动迭代”的功能
        bt_nextCal['state'] = DISABLED#点了这个按钮，就直接禁用俩迭代按钮，防止用户瞎点点出问题
        bt_finishCal['state'] = DISABLED
        if self.nextCal() == True: #调用一下迭代一次的功能，然后看看返回值，如果是True说明还没到最大次数
            self.master.after(1000,self.finishCal)#那就在1秒后，重新自我调用，直到nextCa的返回值是True
#
#
#
#
#
def startCal():
    num = int(nowUnknow.get())#老办法，获取未知数数量（我为什么不直接搞个全局变量呢？》
    Xold = numpy.array([i for i in range(num)])#初始化旧迭代矩阵（即为公式中的Xk），同时也是X0，所以给了不同的初值，有利于可视化分辨
    Xnew = numpy.array([0 for i in range(num)])#初始化新迭代矩阵（Xk+1）
    global Xs#用于记录X的迭代过程，便于可视化,未来有大用处，所以设置为全局变量
    Xs = [Xold]#将k=0时X放入Xs
    nowError = 0x3f3f3f3f#每迭代一次的max（Xk+1-Xk),用于和允许误差对比，判断何时迭代结束
    global minX,maxX#用于记录迭代过程中最大的X和最小的X，便于画图展示所有X时计算刻度范围
    minX = 0x3f3f3f3f
    maxX = -0x3f3f3f3f
    nowArr = None#迭代矩阵
    if nowMethod.get() == '雅各比迭代法':
        nowArr = arrM
    elif nowMethod.get() == '赛德尔迭代法':
        nowArr = arrG
    #print(nowArr)
    while(nowError >= float(premissibleError.get())):#premissibleError是用户输入的允许误差,已经做过合法性检验，所以直接用
        Temp = numpy.matmul(nowArr,Xold)#先把Xk和MorG的积算出来
        Xnew = Temp + arrN#Xk+1 = MorG * Xk + N，这步是计算加法
        maxError = 0 #计算Xnew中所有x和Xold中所有x之间最大的误差值
        for i in range(num):
            for j in Xnew:
                if minX > j :#记录所有x的最小值
                    minX = j
                if maxX < j :#记录所有x的最大值
                    maxX = j
            temp = numpy.abs(Xnew[i] - Xold[i])#当前xnew与xold的误差
            if maxError < temp:#记录最大误差
                maxError = temp
        nowError = maxError#nowError记录本次迭代的最大误差
        Xs.append(Xnew)#将本次迭代结果记入Xs
        Xold = Xnew#k+=1
    #print("迭代过程",Xs)
    #跳出循环则说明迭代成功，接下来就是在当前窗口展示迭代结果和新建一个窗口来放迭代过程折线图了
    initResult()    #展示结果
    initMap()#迭代过程折线图
#
 #   
#
#
'''def test():
    global A,B
    A=[[10,0,1,-5],[1,8,-3,0],[3,2,-8,1],[1,-2,2,7]]
    B=[-7,11,23,17]
    if checkRank() == True:
        if nowMethod.get() == '雅各比迭代法':
            getMandN()
        elif nowMethod.get() == '赛德尔迭代法':
            getGandN()
        elif nowMethod.get() == '松弛迭代法':
            pass
    else:
        tkinter .messagebox .showinfo("警告","矩阵未满秩，请重新输入！")'''
#
def getAandB():
    num = int(nowUnknow.get())#获取未知数数量存入num
    if nowMethod.get() == '待选择':#检测用户是否已经选择了迭代方法
        tkinter .messagebox .showinfo("警告","未选择迭代法！")
        return 0
    if premissibleError.get() == '待确定':#检测用户是否已经填写了误差
        tkinter .messagebox .showinfo("警告","未填写允许误差！")
        return 0
    for i in range(num):
        for j in range(num):
            if checkAorBLegality(unknowFrmsOfA[i][j].get()) == False:#检测A、B矩阵的合法性
                tkinter .messagebox .showinfo("警告","输入不合法！")
                return 0
            elif unknowFrmsOfA[i][j].get() == '':#遇到空白则默认系数为0
                unknowFrmsOfA[i][j].set('0')
            if i == j:#如果i==j即为主元
                if unknowFrmsOfA[i][j].get() == '0':#主元不可为0
                    tkinter .messagebox .showinfo("警告","输入不合法,请确保主元不为0!")
                    return 0
        if checkAorBLegality(unknowFrmsOfB[i].get()) == False:
            tkinter .messagebox .showinfo("警告","输入不合法！")
            return 0
        elif unknowFrmsOfB[i].get() == '':
                unknowFrmsOfB[i].set('0')
    #若A、B都合法，则创建全局变量，将二者储存起来 
    global A,B
    A = [[float(unknowFrmsOfA[i][j].get()) for j in range(num)] for i in range(num)]
    B = [float(unknowFrmsOfB[i].get()) for i in range(num)]
    #print(A,B)
    if checkRank() == True:#检查A/B矩阵是否满秩
        if nowMethod.get() == '雅各比迭代法':
            getMandN()
        elif nowMethod.get() == '赛德尔迭代法':
            getGandN()
#     
    else:
        tkinter .messagebox .showinfo("警告","矩阵未满秩，请重新输入！")
#    
def getMandN():#用于计算雅各比迭代法的迭代矩阵M和N
    num = int(nowUnknow.get())#获取未知数数量
    D = [[0 for i in range(num)] for j in range(num)]#初始化
    I = [[0 for i in range(num)] for j in range(num)]#初始化
    for i in range(num):
        for j in range(num):
            if i == j:
                D[i][j] = A[i][j]#D为A的对角线
                I[i][j] = 1#I矩阵
    arrD = numpy.array(D)#将D转为数组
    invD = numpy.linalg.inv(arrD)#获取D的逆矩阵
    arrA = numpy.array(A)#将A转为数组
    invDdotA = numpy.matmul(invD,arrA)#D-1与A的积
    N = [B[i]/D[i][i] for i in range(num)]#雅各比迭代法中N的公式
    global arrM,arrN#将迭代需要用的M和N设为全局变量
    arrM = I - invDdotA#得到M
    arrN = numpy.array(N)#
    if checkMorGlegality() == True:#检查M的收敛性
        unknowFrms['state']=DISABLED#程序运行到此证明A/B/M矩阵都合法且迭代法收敛，用户无需再输入任何数据，锁定全部按钮，然后开始迭代计算
        unknowButtonChange['state']=DISABLED
        unknowButtonOK['state']=DISABLED
        errorButtonChange['state']=DISABLED
        errorButtonOK['state']=DISABLED
        startCal()#迭代计算的函数
#
def getGandN():#用于计算赛德尔迭代法的迭代矩阵G和N
    num = int(nowUnknow.get())#获取未知数数量
    D = [[0 for i in range(num)] for j in range(num)]#初始化D L U
    L = [[0 for i in range(num)] for j in range(num)]
    U = [[0 for i in range(num)] for j in range(num)]
    for i in range(num):
        for j in range(num):
            if i == j:
                D[i][j] = A[i][j]#D为A的对角线
            if i > j :
                L[i][j] = A[i][j]#左下角
            if i < j :
                U[i][j] = A[i][j]#右上角
    arrD = numpy.array(D)#数组化
    arrL = numpy.array(L)
    arrU = numpy.array(U)
    arrDplusL = arrD + arrL#D和L相加
    invDplusL = numpy.linalg.inv(arrDplusL)#取逆
    invDplusL = -1 * invDplusL#取负
    invDplusLdotU = numpy.matmul(invDplusL,arrU)#得到积
    global arrG,arrN
    arrG = invDplusLdotU#得到G
    arrB = numpy.array(B)
    arrN = numpy.matmul(invDplusL,arrB)#得到N
    if checkMorGlegality() == True:
        unknowFrms['state']=DISABLED#程序运行到此证明A/B/G矩阵都合法且迭代法收敛，用户无需再输入任何数据，锁定全部按钮，然后开始迭代计算
        unknowButtonChange['state']=DISABLED
        unknowButtonOK['state']=DISABLED
        errorButtonChange['state']=DISABLED
        errorButtonOK['state']=DISABLED
        startCal()#开始迭代计算
   # 
def checkRank():#用于检测A是否满秩
    arr = numpy.array(A)#用array储存A
    if numpy.linalg.det(arr) != 0 :#如果A的行列式不等于0则满秩
        return True
    else:
        return False
#
def checkMorGlegality():#用于检测迭代矩阵是否收敛
    if nowMethod.get() == '雅各比迭代法':
        a,b=numpy.linalg.eig(arrM)
        rou = numpy.max(numpy.abs(a))
        if rou < 1:
            tkinter .messagebox .showinfo("提示","检测矩阵成功收敛，现在开始迭代！")
            return True
        else:
            tkinter .messagebox .showinfo("警告","检测矩阵未收敛！请确认输入或更换迭代方法！")
            return False
    elif nowMethod.get()=='赛德尔迭代法':
        a,b=numpy.linalg.eig(arrG)
        rou = numpy.max(numpy.abs(a))
        if rou < 1:
            tkinter .messagebox .showinfo("提示","检测矩阵成功收敛，现在开始迭代！")
            return True
        else:
            tkinter .messagebox .showinfo("警告","检测矩阵未收敛！请确认输入或更换迭代方法！")
            return False
#
    #
def checkAorBLegality(temp):#用于检测A或B是否输入合法
    if temp == '':
        return True
    try :
        num = float(temp)
        return True
    except:
        return False
    #
def checkUnknowLegality(TEMP):#用于检测未知数个数的输入是否合法
    try :
        num = int(TEMP)
        if num >= 1 and num <= 50:
            return True
        else:
            return False
    except:
        return False
    #
def checkErrorLegality(TEMP):
    try :#检查输入的误差的合法性
        num = float(TEMP)#首先检查是否为浮点数
        if num >= 0.00000001 and num <= 0.1 :#再检查是否符合误差合理范围
            return True
        else:
            return False
    except:
        return False
    #
def changeUnknow():
    unknowButtonOK['state']=ACTIVE
    unknowButtonChange['state']=DISABLED
    unknowEntry.config(state='normal')
    #
def changeError():
    errorButtonOK['state']=ACTIVE
    errorButtonChange['state']=DISABLED
    errorEntry.config(state='normal')
    #
def updateUnkown(TEMP):
    if checkUnknowLegality(TEMP) == True:
        unknowButtonOK['state']=DISABLED
        unknowButtonChange['state']=ACTIVE
        nowUnknow.set(TEMP)
        unknowEntry.config(state='readonly')
        initInputView()
    else:
        tkinter .messagebox .showinfo("警告","输入不合法！请输入[1,50]内正整数")
#
def updateError(TEMP):
    if checkErrorLegality(TEMP) == True:#用于异常情况排查的函数
        errorButtonOK['state']=DISABLED#如果合适，则将确认按钮设置为disabled，更改按钮设置为active
        errorButtonChange['state']=ACTIVE
        premissibleError.set(TEMP)#将设置的误差存入StringVar
        errorEntry.config(state='readonly')#更新Entry里的内容
    else:
        tkinter .messagebox .showinfo("警告","输入不合法！请输入[0.0000001,0.1]内小数")
#        
def Methods(type):
    nowMethod.set(type)
#
def initResult():#用于在win窗口展示迭代结果
    sep = tkinter.Frame(win,bg='black')
    sep.pack(side=tkinter.TOP,fill='both')
    frm = tkinter.Frame(win)
    title = Label(frm,text = '迭代结果',bg='yellow').pack(side=TOP)#新建Frame
    num = int(nowUnknow.get())#还是老办法哈哈哈哈 这行代码写了n次了
    now = 0
    while now != num :#这块写的有点混乱，大概介绍一下，最开始想着假如有很多未知数，我不能都在一行显示出来吧？
        #所以就套了两层循环，外层建新的Frame，内层建Label
        #但是做着做着做到展示迭代过程时（下面的initProcess）发现其实意义不大，要是未知数很多，
        #迭代次数相对就多，每一次迭代又分了好多行显示的话
        #最后看着就非常滴乱，所以我就都在一次迭代在同一行展示了
        #不过已经懒得改代码了QAQ，就把参数改了改，现在最外层的while循环应该是没用的
        tempFrm = tkinter.Frame(frm)
        for i in range(num):
            if now != num:
                Label(tempFrm,text='x%-3d='%now,bg='grey',fg='white').pack(side=LEFT)
                Label(tempFrm,text='%-3.6f'%Xs[-1][now],bg='black',fg='white').pack(side=LEFT)
            now+=1
        tempFrm.pack(side=TOP)
    frm.pack(side=tkinter.TOP,fill='both')            
    initProcess()#用于展示迭代过程
#    
def initProcess():#初始化查看迭代过程按钮
    sep = tkinter.Frame(win,bg='black')
    sep.pack(side=tkinter.TOP,fill='both')
    frm = tkinter.Frame(win)
    global btProcess#这里设计的是：玩家可以选择是否查看迭代过程，所以一开始不展出，而是只放了个按钮
    btProcess = Button(frm,text = '查看迭代过程',command = lambda:getProcess())#用户点了按钮再展示
    btProcess.pack(side=TOP)
    frm.pack(side=TOP)
#    
def getProcess():#初始化迭代过程
    btProcess['state']=DISABLED
    frm = tkinter.Frame(win)
    tkinter.Label(frm,text='下面是迭代过程',fg='dark blue',bg='orange').pack(side=TOP)#先来个标题
    num = int(nowUnknow.get())#??????我有这么离谱吗 用了这么多次还不……
    for i in range(len(Xs)):
        tempFrm = tkinter.Frame(frm)
        tkinter.Label(tempFrm,text='第%2d次迭代：'%i,bg='dark green',fg='white').pack(side=LEFT)#显示迭代次数
        for j in range(num):#显示xn和具体数
            Label(tempFrm,text='x%-2d='%j,fg='purple',bg='light grey').pack(side=LEFT)
            Label(tempFrm,width=10,text='%3.6f'%Xs[i][j],bg='black',fg='white').pack(side=LEFT)
        tempFrm.pack(side=TOP)
    frm.pack(side=TOP)
#        
def initMap():
    global root
    root = Tk()
    root.title('【'+nowMethod.get()+'】迭代过程折线图')
    root.geometry('560x400+600+200')
    app = Application(master=root)
    root.mainloop()
 #  
def initMenuMethod():
    menu1= tkinter.Menu(menubar,tearoff=False)
    #给菜单添加内容
    method1 = "雅各比迭代法"
    method2 = "赛德尔迭代法"
    
    menu1.add_command(label=method1,command=lambda: Methods(method1))
    menu1.add_command(label=method2,command=lambda: Methods(method2))
    
    menubar.add_cascade(label="迭代方法",menu=menu1)
    win.config(menu = menubar)
#
def initInputView():
    sep = tkinter.Frame(win,bg='black')
    sep.pack(side=tkinter.TOP,fill='both')
    frm = tkinter.Frame(win)
    frm.pack(side=tkinter.TOP,fill='both')
    num = int(nowUnknow.get())
    global unknowFrmsOfA,unknowFrmsOfB
    unknowFrmsOfA = [[StringVar() for i in range(num)] for j in range(num)]#用两个StringVar来储存用户输入的两个矩阵A、B
    unknowFrmsOfB = [StringVar() for i in range(num)]#
    for i in range(num):#利用循环创建多个Frame，每个Frame是一个方程
        frmLine = tkinter.Frame(frm,bg='green')
        for j in range(num+1):
            tempFrm  = tkinter.Frame(frmLine,bg='white')
            if j == num :
                Entry(tempFrm,textvariable=unknowFrmsOfB[i],width=2).pack(side=tkinter.LEFT)
                tkinter.Label(tempFrm,text="b"+str(i),fg='white',bg="grey").pack(side=tkinter.LEFT)  
            else:  
                Entry(tempFrm,textvariable=unknowFrmsOfA[i][j],width=2).pack(side=tkinter.LEFT)
                tkinter.Label(tempFrm,text="x"+str(j),fg='white',bg="grey").pack(side=tkinter.LEFT)
            tempFrm.pack(side=tkinter.LEFT)
        frmLine.pack(side=tkinter.TOP)
    tkinter.Label(win, text='空白格默认以0为系数,请确保主元不为0！',bg='light grey',fg="white").pack(side=TOP)
    global unknowFrms
    unknowFrms = Button(win, text='输入完成',command=lambda:getAandB())
    unknowFrms.pack(side=TOP)
    #Button(win, text='测试按钮',command=lambda:test()).pack(side=TOP)
#
def initErrorInput():#初始化输入和显示允许误差
    frm = tkinter.Frame(win)
    frm.pack(side=tkinter.TOP,fill='x')
    frm_1 = tkinter.Frame(frm)
    tkinter.Label(frm_1,text="当前误差范围   ",fg="white",bg="grey").pack(side=tkinter.LEFT)
    global errorEntry,errorButtonChange,errorButtonOK
    errorEntry = Entry(frm_1,state="normal",width=6)
    errorButtonOK = Button(frm_1, text='确定', command=lambda:updateError(errorEntry.get()))#利用Entry.get获取输入
    errorButtonChange = Button(frm_1, text='更改',command=lambda:changeError())#更改按钮
    errorEntry.pack(side=tkinter.LEFT)
    errorButtonOK.pack(side=tkinter.LEFT)
    errorButtonChange.pack(side=tkinter.LEFT)
    frm_1.pack(side=tkinter.LEFT)
#    
def initUnknowInput():#用于用户输入未知数的个数,整体逻辑和initErrorInput相同
    frm = tkinter.Frame(win)
    frm.pack(side=tkinter.TOP,fill='x')
    frm_1 = tkinter.Frame(frm)
    tkinter.Label(frm_1,text="当前未知数数量",fg="white",bg="grey").pack(side=tkinter.LEFT)
    global unknowEntry,unknowButtonOK,unknowButtonChange
    unknowEntry = Entry(frm_1,state="normal",width=6)
    unknowButtonOK = Button(frm_1, text='确定', command=lambda:updateUnkown(unknowEntry.get()))
    unknowButtonChange = Button(frm_1, text='更改',command=lambda:changeUnknow())
    unknowEntry.pack(side=tkinter.LEFT)
    unknowButtonOK.pack(side=tkinter.LEFT)
    unknowButtonChange.pack(side=tkinter.LEFT)
    frm_1.pack(side=tkinter.LEFT)
 #   
def initContentMethod():
    frm = tkinter.Frame(win)
    frm.pack(side=tkinter.TOP,fill='x')#设置父框
    frm_1 = tkinter.Frame(frm)
    tkinter.Label(frm_1,text="当前迭代方法   ",fg="white",bg="grey").pack(side=tkinter.LEFT)
    tkinter.Label(frm_1,textvariable=nowMethod,bg="white").pack(side=tkinter.LEFT)#利用StringVar和textvariable实现Label的动态刷新
    frm_1.pack(side=tkinter.LEFT)
#
#
win.title("小惠解方程组") #窗体标题
win.geometry("400x600+200+50") #设置窗体显示屏幕上的位置
menubar = tkinter.Menu(win)#顶部菜单栏
initMenuMethod()#初始化菜单栏
initContentMethod()#初始化显示迭代方法的Frame
initErrorInput()#初始化输入和显示允许误差的Frame
initUnknowInput()#初始化输入和显示未知数的Frame
#
#
win.mainloop()#将窗体显示出来