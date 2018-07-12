# -*- encoding=UTF-8 -*-
__author__ = 'fyby'
from tkinter import *
from tkinter import ttk
import win32api, win32con
import time
import datetime
from dateutil.relativedelta import relativedelta

import register
import uuid


class App:
    def __init__(self, master):
        # 功能列表模块
        # functionframe = Frame(master)
        # functionframe.place(x=80, y=30, relwidth=1, height=80)
        # self.initFunctionModule(functionframe)

        # 有效期模块
        validity = Frame(master)
        validity.place(x=80, y=40, relwidth=.8, height=80)
        self.initValidity(validity)

        # 用户码模块
        usercodeframe = Frame(master)
        usercodeframe.place(x=80, y=120, relwidth=.8, height=200)
        self.initUserCode(usercodeframe)

        # 保存为注册文件按钮
        saveframe = Frame(master)
        saveframe.place(x=80, y=400, relwidth=.8, height=100)
        self.initSaveFrame(saveframe)

        self.myRegister = register.ZyylRegister()

    def numberChosenEnabled(self):
        self.monthChosen.configure(state='disabled')
        self.numberChosen.configure(state='readonly')

    def monthChosenEnabled(self):
        self.monthChosen["state"] = 'readonly'
        self.numberChosen.configure(state='disabled')

    def initValidity(self, master):

        self.validitySelect = IntVar()
        self.validitySelect.set(1)
        Radiobutton(master, variable=self.validitySelect, value=1, text='有效次数:', font='18',
                    command=self.numberChosenEnabled).grid(row=0, column=0, pady=5, sticky=NW)
        Radiobutton(master, variable=self.validitySelect, value=2, text='有效时间段:', font='18',
                    command=self.monthChosenEnabled).grid(row=1, column=0, pady=5, sticky=NW)

        # 创建一个下拉列表
        self.validityTimes = StringVar()
        self.numberChosen = ttk.Combobox(master, width=12, textvariable=self.validityTimes, state='readonly')
        self.numberChosen['values'] = (500, 1000, 2500, 5000, 10000, 25000, 50000)  # 设置下拉列表的值
        self.numberChosen.grid(column=1, row=0, padx=2, pady=5, sticky=NW)  # 设置其在界面中出现的位置  column代表列   row 代表行
        self.numberChosen.current(0)  # 设置下拉列表默认显示的值，0为 numberChosen['values'] 的下标值

        usercodelb = Label(master, text='次', font='18')
        usercodelb.grid(row=0, column=2, padx=2, pady=5, sticky=NW)

        # 创建一个下拉列表
        self.validityMonths = StringVar()
        self.monthChosen = ttk.Combobox(master, width=12, textvariable=self.validityMonths, state='readonly')
        self.monthChosen.configure(state='disable')
        self.monthChosen['values'] = (1, 3, 6, 9, 12, 18, 24, 36)  # 设置下拉列表的值
        self.monthChosen.grid(column=1, row=1, padx=2, pady=5, sticky=NW)  # 设置其在界面中出现的位置  column代表列   row 代表行
        self.monthChosen.current(0)  # 设置下拉列表默认显示的值，0为 monthChosen['values'] 的下标值

        usercodelb = Label(master, text='月', font='18')
        usercodelb.grid(row=1, column=2, padx=2, pady=5, sticky=NW)

    def SaveRegisterToFile(self):
        if self.registerValue:
            self.myRegister.SaveRegisterCode()
            win32api.MessageBox(0, "保存成功，请在文件registerLicence中查看", "保存文件", win32con.MB_OK)

    def GenerateRegister(self):
        userCodeStr = self.usercodeentry.get()
        # userCodeStr = self.myRegister.GetUserCode()
        if userCodeStr == '':
            win32api.MessageBox(0, "请您输入用户码", "用户码提示", win32con.MB_OK)
            return

        print("用户码:" + userCodeStr)

        funcCheckSelectStr = ""
        i = 0

        '''
            功能区暂时屏蔽
        '''
        # funcIsSelect = False
        # for icheckboxValue in self.checkBoxSelect:
        #     if icheckboxValue.get() == 1:
        #         funcIsSelect = True
        #         funcCheckSelectStr += self.checkBoxFuncName[i] + '@'
        #     i += 1

        # if not funcIsSelect:
        #     win32api.MessageBox(0, "请您至少选择一个功能项", "未选择功能提示", win32con.MB_OK)
        #     return

        # print("选择的功能:" + funcCheckSelectStr)

        validitySelectStr = ""
        if self.validitySelect.get() == 1:
            validitySelectStr = "counts@" + self.numberChosen.get()
            print("选择了次数验证")
        else:
            datetime_now = datetime.datetime.now()
            datetime_three_month_after = datetime_now + relativedelta(months=int(self.monthChosen.get()))
            print(datetime_three_month_after)
            validitySelectStr = "months:" + datetime.datetime.now().strftime(
                '%Y-%m-%d') + "@" + datetime_three_month_after.strftime('%Y-%m-%d')
            print("选择了有效期验证")

        print("有效期:" + validitySelectStr)

        # myRegister = register.ZyylRegister()
        codeValue = userCodeStr + "|" + funcCheckSelectStr + "|" + validitySelectStr + "|" + str(uuid.uuid1())
        print(codeValue)
        self.registerValue = self.myRegister.GetRegistCode(codeValue)
        # self.registerValue = userCodeStr + "|" + funcCheckSelectStr + "|" + validitySelectStr
        self.registerText.delete(0.0, END)
        self.registerText.insert(INSERT, self.registerValue)


    def initFunctionModule(self, master):
        # lb.place(relx = 1,rely = 0.5,anchor = CENTER)
        # 使用相对坐标(0.5,0.5)将Label放置到(0.5*sx,0.5.sy)位置上
        functionlb = Label(master, text='功能列表', font='18')
        functionlb.place(x=0, y=20)
        # 这个地方的功能名称不能使用中文，在进行DES加密时候中文转换ASCII有问题
        self.checkBoxFuncName = ['Function1', 'Function2', 'Function3', 'Function4', 'Function5']
        self.FunctionNameDict = {'Function1': '功能1', 'Function2': '功能2', 'Function3': '功能3', 'Function4': '功能4',
                                 'Function5': '功能5'}
        self.checkBoxSelect = [IntVar(), IntVar(), IntVar(), IntVar(), IntVar()]
        self.checkboxlist = []
        pos = 0
        for i in self.FunctionNameDict:
            self.checkboxlist.append(Checkbutton(
                master,
                text=self.FunctionNameDict[i],
                variable=self.checkBoxSelect[pos]
            ).place(x=80 * pos + 40, y=70, anchor=W))
            pos = pos + 1

    def initSaveFrame(self, master):
        savebutton = Button(master, width=20, text="保存注册码为文件", command=self.SaveRegisterToFile)
        savebutton.grid(row=0, column=0, padx=150, pady=10)

    def initUserCode(self, master):
        usercodelb = Label(master, text='用户码:', font='18')
        # usercodelb.place(x=10, y=0)
        usercodelb.grid(row=0, column=0, padx=2, pady=5)
        name = StringVar()
        self.usercodeentry = Entry(master, width=40, textvariable=name)
        self.usercodeentry.grid(row=0, column=1, padx=2, pady=5)
        # usercodeentry.place(x=72, y=0)

        usercodebutton = Button(master, width=10, text="生成注册码", command=self.GenerateRegister)
        usercodebutton.grid(row=0, column=2, padx=2, pady=5)

        usercodelb = Label(master, text='注册码:', font='18')
        usercodelb.grid(row=1, column=0, padx=2, pady=5)
        # usercodelb.place(x=10, y=30)

        self.registerText = Text(master, height=100, width=55)
        self.registerText.grid(row=2, column=0, columnspan=3)


win = Tk(className='智影医疗CDKEY注册程序')
win.geometry('600x400')
win.resizable(0, 0)
app = App(win)
win.mainloop()
