#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk
import register

win = tk.Tk()
win.title("Python GUI")    # 添加标题

#ttk.Label(win, text="Chooes a number").grid(column=1, row=0)    # 添加一个标签，并将其列设置为1，行设置为0
ttk.Label(win, text="点击按钮获取用户码").grid(column=0, row=0)      # 设置其在界面中出现的位置  column代表列   row 代表行

# button被点击之后会被执行
def clickMe():   # 当acction被点击时,该函数则生效
  myRegister = register.ZyylRegister()
  nameEntered.delete('0', 'end')
  nameEntered.insert(0,myRegister.GetUserCode())

# 按钮
action = ttk.Button(win, text="获取用户码", command=clickMe)     # 创建一个按钮, text：显示按钮上面显示的文字, command：当这个按钮被点击之后会调用command函数
action.grid(column=2, row=1)    # 设置其在界面中出现的位置  column代表列   row 代表行

# 文本框
name = tk.StringVar()     # StringVar是Tk库内部定义的字符串变量类型，在这里用于管理部件上面的字符；不过一般用在按钮button上。改变StringVar，按钮上的文字也随之改变。
nameEntered = ttk.Entry(win, width=30, textvariable=name)   # 创建一个文本框，定义长度为12个字符长度，并且将文本框中的内容绑定到上一句定义的name变量上，方便clickMe调用
nameEntered.grid(column=0, row=1)       # 设置其在界面中出现的位置  column代表列   row 代表行
nameEntered.focus()     # 当程序运行时,光标默认会出现在该文本框中


win.mainloop()      # 当调用mainloop()时,窗口才会显示出来
