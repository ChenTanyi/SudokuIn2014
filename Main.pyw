#!/usr/bin/env python
# -*- coding: utf-8- -*-
#===============================================================================
#This is a GUI of sudoku game made by Chen Tanyi.
#===============================================================================
import os
from Tkinter import *
from tkMessageBox import *
from tkFileDialog import *
from sudoku import *

class MyGUI(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.initGraphics()
        self.initSudoku()
        self.sudoku=Sudoku()
        showinfo("提示","这是一个数独游戏&求解器，使用方法详见README文档")
        answer=askokcancel("确认","是否打开README文档")
        if answer:
            os.popen("README.txt")
        #-----------------------------------------------------------------------
    def initGraphics(self):
        self.ModeFrame=Frame(self,bd=2,relief="groove")
        self.ModeVar=StringVar()
        self.ModeVar.set("solve")
        self.SolveMode=Radiobutton(self.ModeFrame,text="电脑帮我解数独",
                                   variable=self.ModeVar,value="solve")
        self.PlayMode=Radiobutton(self.ModeFrame,text="我要解数独",
                                  variable=self.ModeVar,value="playing")
        self.ModeFrame.grid(row=0,rowspan=2,column=20,sticky=N+E+S+W)
        self.SolveMode.grid(row=0,column=20,sticky=W)
        self.PlayMode.grid(row=1,column=20,sticky=W)
        #-----------------------------------------------------------------------
        self.ShowFrame=Frame(self,bd=2,relief="groove")
        self.ShowVar=StringVar()
        self.ShowVar.set("black")
        self.RedMode=Radiobutton(self.ShowFrame,text="显示错误",
                                 variable=self.ShowVar,value="red")
        self.BlackMode=Radiobutton(self.ShowFrame,text="不显示错误",
                                   variable=self.ShowVar,value="black")
        self.ShowFrame.grid(row=2,rowspan=2,column=20,sticky=N+E+S+W)
        self.RedMode.grid(row=3,column=20,sticky=W)
        self.BlackMode.grid(row=2,column=20,sticky=W)
        #-----------------------------------------------------------------------
        self.DifficultyFrame=Frame(self,bd=2,relief="groove")
        self.DifficultyVar=IntVar()
        self.DifficultyVar.set(3)
        self.EasyMode=Radiobutton(self.DifficultyFrame,text="简单",state="disabled",
                                  variable=self.DifficultyVar,value=3)
        self.MediumMode=Radiobutton(self.DifficultyFrame,text="中等",state="disabled",
                                    variable=self.DifficultyVar,value=2)
        self.HardMode=Radiobutton(self.DifficultyFrame,text="困难",state="disabled",
                                  variable=self.DifficultyVar,value=1)
        self.ExtremeMode=Radiobutton(self.DifficultyFrame,text="骨灰",state="disabled",
                                     variable=self.DifficultyVar,value=0)
        self.DifficultyFrame.grid(row=4,rowspan=4,column=20,sticky=N+E+S+W)
        self.EasyMode.grid(row=4,column=20,sticky=W)
        self.MediumMode.grid(row=5,column=20,sticky=W)
        self.HardMode.grid(row=6,column=20,sticky=W)
        self.ExtremeMode.grid(row=7,column=20,sticky=W)
        #-----------------------------------------------------------------------
        self.SelfDifineButton=Button(self,text="自定义",font=("Times New Roman",20),
                                     anchor=N,command=self.selfDifine)
        self.SelfDifineButton.grid(row=8,rowspan=2,column=20,sticky=N+E+S+W)
        self.InitButton=Button(self,text="初始化",font=("Times New Roman",15),
                               command=self.reInitSudoku)
        self.InitButton.grid(row=9,column=20)
        self.UndoButton=Button(self,text="撤销",font=("Times New Roman",15),
                               command=self.lineCancel)
        self.UndoButton.grid(row=10,column=20,sticky=E)
        self.OKButton=Button(self,text="确定",font=("Times New Roman",15),
                             command=self.selfDifineCheck)
        self.OKButton.grid(row=10,column=20,sticky=W)
        self.StartButton=Button(self,text="开始",font=("Times New Roman",20),
                                state="disabled",command=self.start)
        self.StartButton.grid(row=11,rowspan=2,column=20,sticky=N+E+S+W)
        self.SolveButton=Button(self,text="求解",font=("Times New Roman",20),
                                command=self.solve)
        self.SolveButton.grid(row=13,rowspan=2,column=20,sticky=N+E+S+W)
        self.AllClearButton=Button(self,text="清除",font=("Times New Roman",20),
                                command=self.allClear)
        self.AllClearButton.grid(row=15,rowspan=2,column=20,sticky=N+E+S+W)
        self.OpenButton=Button(self,text="打开",font=("Times New Roman",15),
                                 command=self.openFile)
        self.OpenButton.grid(row=17,column=20,sticky=W)
        self.SaveButton=Button(self,text="保存",font=("Times New Roman",15),
                               command=self.saveFile)
        self.SaveButton.grid(row=17,column=20,sticky=E)
        self.SubmitButton=Button(self,text="提交",font=("Times New Roman",15),
                                 command=self.submit)
        self.SubmitButton.grid(row=18,column=20,sticky=W)
        self.QuitButton=Button(self,text="离开",font=("Times New Roman",15),
                               command=lambda:self.destroy())
        self.QuitButton.grid(row=18,column=20,sticky=E)
        #-----------------------------------------------------------------------
        self.SolveMode.bind("<1>",self.disAbled)
        self.PlayMode.bind("<1>",self.abled)
        self.RedMode.bind("<1>",lambda event:self.showColor("red"))
        self.BlackMode.bind("<1>",lambda event:self.showColor("black"))
        #-----------------------------------------------------------------------
    def initSudoku(self):
        self.SudokuFrame=Frame(self)
        self.SudokuFrame.grid(row=0,column=0,rowspan=19,columnspan=19)
        self.SudokuLabel=[[0 for i in xrange(19)]for j in xrange(19)]
        self.normallinev=PhotoImage(file="images/normallinev.ppm")
        self.normallineh=PhotoImage(file="images/normallineh.ppm")
        self.seperatelinev=PhotoImage(file="images/seperatelinev.ppm")
        self.seperatelineh=PhotoImage(file="images/seperatelineh.ppm")
        self.seperatorb=PhotoImage(file="images/seperatorb.ppm")
        for i in xrange(19):
          for j in xrange(0,19,2):
            if i & 1 != 0:
              if j in [0,6,12,18]:
                self.SudokuLabel[j][i]=Label(self.SudokuFrame,image=self.seperatelineh)
                self.SudokuLabel[j][i].grid(row=j,column=i)
                self.SudokuLabel[i][j]=Label(self.SudokuFrame,image=self.seperatelinev)
                self.SudokuLabel[i][j].grid(row=i,column=j)
                self.SudokuLabel[i][j].bind("<1>",self.seperatev)
                self.SudokuLabel[j][i].bind("<1>",self.seperateh)
              else:
                self.SudokuLabel[j][i]=Label(self.SudokuFrame,image=self.normallineh)
                self.SudokuLabel[j][i].grid(row=j,column=i)
                self.SudokuLabel[i][j]=Label(self.SudokuFrame,image=self.normallinev)
                self.SudokuLabel[i][j].grid(row=i,column=j)
                self.SudokuLabel[i][j].bind("<1>",self.seperatev)
                self.SudokuLabel[j][i].bind("<1>",self.seperateh)
            else:
                self.SudokuLabel[i][j]=Label(self.SudokuFrame,image=self.seperatorb)
                self.SudokuLabel[i][j].grid(row=i,column=j)
        for row in xrange(1,18,2):
            for col in xrange(1,18,2):
                self.SudokuLabel[row][col]=Label(self.SudokuFrame,bg="white",takefocus=True,
                                                 bd=3,width=2,font=("Helvetica",30),cursor="hand2",
                                                 justify=CENTER, highlightcolor="#ffff00", highlightthickness="3")
                self.SudokuLabel[row][col].grid(row=row,column=col)
                self.SudokuLabel[row][col].bind("<1>",self.focusWidget)
                self.SudokuLabel[row][col].bind("<Key>",self.addKey)
        #-----------------------------------------------------------------------
        self.difine=False
        self.focus=None
        self.Box=[[0,0,0,1,1,1,2,2,2],
                  [0,0,0,1,1,1,2,2,2],
                  [0,0,0,1,1,1,2,2,2],
                  [3,3,3,4,4,4,5,5,5],
                  [3,3,3,4,4,4,5,5,5],
                  [3,3,3,4,4,4,5,5,5],
                  [6,6,6,7,7,7,8,8,8],
                  [6,6,6,7,7,7,8,8,8],
                  [6,6,6,7,7,7,8,8,8]]
        self.check=[[False for i in xrange(9)]for j in xrange(9)]
        #-----------------------------------------------------------------------
    def openFile(self):
        filename = askopenfilename(defaultextension = 'txt',
                                filetypes = [('Text Files','.txt'), ('All Files','.*')])
        if filename != '':
          try:
            f=open(filename,"r")
            grid=[]
            for i in xrange(9):
                grid.append(eval(f.readline()))
            f.close()
            self.allClear()
            for i in xrange(1,18,2):
              for j in xrange(1,18,2):
                if self.sudoku.grid[i/2][j/2] != 0:
                    self.SudokuLabel[i][j]["text"] = str(self.sudoku.grid[i/2][j/2])
          except:
            showinfo("错误","打开失败")
        #-----------------------------------------------------------------------
    def saveFile(self):
        filename = asksaveasfilename(defaultextension = 'txt',
                                 filetypes = [('Text Files','.txt'), ('All Files','.*')])
        if filename != '':
            f=open(filename,"w")
            self.updateGrid()
            f.write("\n".join(map(str,self.sudoku.grid)))
            f.close()
        #-----------------------------------------------------------------------
    def disAbled(self,event):
        self.allClear()
        self.EasyMode["state"]="disabled"
        self.MediumMode["state"]="disabled"
        self.HardMode["state"]="disabled"
        self.ExtremeMode["state"]="disabled"
        self.StartButton["state"]="disabled"
        #-----------------------------------------------------------------------
    def abled(self,event):
        self.allClear()
        self.EasyMode["state"]="normal"
        self.MediumMode["state"]="normal"
        self.HardMode["state"]="normal"
        self.ExtremeMode["state"]="normal"
        self.StartButton["state"]="normal"
        #-----------------------------------------------------------------------
    def focusWidget(self,event):
        if self.difine:
            return
        event.widget.focus()
        if self.focus:
            self.focus["relief"]="flat"
        self.focus=event.widget
        self.focus["relief"]="groove"
        #-----------------------------------------------------------------------
    def addKey(self,event):
        if self.difine or event.widget["fg"] == "blue":
            return
        if event.keysym == "BackSpace" or event.char == '0':
            event.widget["text"]=''
            self.showColor(self.ShowVar.get())
        elif event.char >= '1' and event.char <= '9':
            event.widget["text"]=event.char
            self.showColor(self.ShowVar.get())
        #-----------------------------------------------------------------------
    def allClear(self):
        self.check=[[False for i in xrange(9)]for j in xrange(9)]
        for row in xrange(1,18,2):
            for col in xrange(1,18,2):
                self.SudokuLabel[row][col]["text"]=''
                self.SudokuLabel[row][col]["fg"]="black"
        if self.focus:
            self.focus["relief"]="flat"
            self.focus=None
        #-----------------------------------------------------------------------
    def selfDifine(self):
        self.difine=True
        self.allClear()
        for i in xrange(1,18,2):
            for j in xrange(2,17,2):
                self.SudokuLabel[j][i]["image"]=self.normallineh
                self.SudokuLabel[i][j]["image"]=self.normallinev
                self.SudokuLabel[i][j]["cursor"]="hand2"
                self.SudokuLabel[j][i]["cursor"]="hand2"
        for row in xrange(1,18,2):
            for col in xrange(1,18,2):
                self.SudokuLabel[row][col]["cursor"]="arrow"
        self.Box=[[-1 for i in xrange(9)] for j in xrange(9)]
        self.LineChange=[]
        #-----------------------------------------------------------------------
    def seperatev(self,event):
        if not self.difine:
            return
        event.widget["image"]=self.seperatelinev
        self.LineChange.append(event.widget)
        #-----------------------------------------------------------------------
    def seperateh(self,event):
        if not self.difine:
            return
        event.widget["image"]=self.seperatelineh
        self.LineChange.append(event.widget)
        #-----------------------------------------------------------------------
    def floodFill(self,row,col,flag):
        self.Check+=1
        if self.Check > 9 :
            return
        i=row/2
        j=col/2
        self.Box[i][j] = flag
        if i > 0 and self.Box[i-1][j] == -1 and self.SudokuLabel[row-1][col]["image"] == str(self.normallineh):
            self.floodFill(row-2,col,flag)
        if j > 0 and self.Box[i][j-1] == -1 and self.SudokuLabel[row][col-1]["image"] == str(self.normallinev):
            self.floodFill(row,col-2,flag)
        if i < 8 and self.Box[i+1][j] == -1 and self.SudokuLabel[row+1][col]["image"] == str(self.normallineh):
            self.floodFill(row+2,col,flag)
        if j < 8 and self.Box[i][j+1] == -1 and self.SudokuLabel[row][col+1]["image"] == str(self.normallinev):
            self.floodFill(row,col+2,flag)
        #-----------------------------------------------------------------------
    def floodFillCheck(self):
        flag=0
        for i in xrange(9):
            for j in xrange(9):
                if self.Box[i][j] == -1:
                    self.Check=0
                    self.floodFill(i*2+1,j*2+1,flag)
                    if self.Check != 9 :
                        self.Box=[[-1 for i in xrange(9)] for j in xrange(9)]
                        return False
                    flag+=1
        return True
        #-----------------------------------------------------------------------
    def selfDifineCheck(self):
        if not self.difine:
            return
        if self.floodFillCheck() :
            answer=askokcancel("确认","确定要修改为如图锯齿数独？")
            if answer:
              try:
                self.sudoku.setBox(self.Box)
                self.difine=False
                self.changeCursor()
                showinfo("提示","修改成功")
              except:
                showinfo("提示","修改失败")
        else:
            showinfo("错误","该修改不符合数独要求，请重试")
        #-----------------------------------------------------------------------
    def changeCursor(self):
        if self.difine:
            for i in xrange(1,18,2):
                for j in xrange(2,17,2):
                    self.SudokuLabel[i][j]["cursor"]="hand2"
                    self.SudokuLabel[j][i]["cursor"]="hand2"
            for row in xrange(1,18,2):
                for col in xrange(1,18,2):
                    self.SudokuLabel[row][col]["cursor"]="arrow"
        else:
            for i in xrange(1,18,2):
                for j in xrange(2,17,2):
                    self.SudokuLabel[i][j]["cursor"]="arrow"
                    self.SudokuLabel[j][i]["cursor"]="arrow"
            for row in xrange(1,18,2):
                for col in xrange(1,18,2):
                    self.SudokuLabel[row][col]["cursor"]="hand2"
        #-----------------------------------------------------------------------
    def reInitSudoku(self):
        if not self.difine :
            return
        for i in xrange(1,18,2):
          for j in xrange(0,19,2):
              if j in [0,6,12,18]:
                self.SudokuLabel[j][i]["image"]=self.seperatelineh
                self.SudokuLabel[i][j]["image"]=self.seperatelinev
                self.SudokuLabel[i][j]["cursor"]="arrow"
                self.SudokuLabel[j][i]["cursor"]="arrow"
              else:
                self.SudokuLabel[j][i]["image"]=self.normallineh
                self.SudokuLabel[i][j]["image"]=self.normallinev
                self.SudokuLabel[i][j]["cursor"]="arrow"
                self.SudokuLabel[j][i]["cursor"]="arrow"
        for row in xrange(1,18,2):
            for col in xrange(1,18,2):
                self.SudokuLabel[row][col]["cursor"]="hand2"
                self.SudokuLabel[row][col]["fg"]="black"
        #-----------------------------------------------------------------------
        self.difine=False
        if self.focus:
            self.focus["relief"]="flat"
            self.focus=None
        self.Box=[[0,0,0,1,1,1,2,2,2],
                  [0,0,0,1,1,1,2,2,2],
                  [0,0,0,1,1,1,2,2,2],
                  [3,3,3,4,4,4,5,5,5],
                  [3,3,3,4,4,4,5,5,5],
                  [3,3,3,4,4,4,5,5,5],
                  [6,6,6,7,7,7,8,8,8],
                  [6,6,6,7,7,7,8,8,8],
                  [6,6,6,7,7,7,8,8,8]]
        #-----------------------------------------------------------------------
    def lineCancel(self):
        if not self.difine or self.LineChange == []:
            return
        line=self.LineChange.pop()
        if line["image"] == str(self.seperatelinev):
            line["image"] = self.normallinev
        else:
            line["image"] = self.normallineh
        #-----------------------------------------------------------------------
    def start(self):
        if self.difine:
            return
        self.sudoku.createGrid()
        while 1:
            if not self.sudoku.makeGrid(self.DifficultyVar.get()):
                self.sudoku.createGrid()
            else:
                self.showQuestion()
                return
        '''rand = randrange(256)
        filename = open("data/data.txt","r")
        grid=[]
        for i in xrange(rand-1):
            for j in xrange(9):
                filename.readline()
        for i in xrange(9):
            grid.append(eval(filename.readline()))
        self.sudoku.setGrid(grid)
        filename.close()
        self.showQuestion()'''
        #-----------------------------------------------------------------------
    def showSolve(self):
        for i in xrange(1,18,2):
            for j in xrange(1,18,2):
                if self.sudoku.grid[i/2][j/2] != 0:
                    self.SudokuLabel[i][j]["text"] = str(self.sudoku.grid[i/2][j/2])
        #-----------------------------------------------------------------------
    def solve(self):
        if self.difine:
            return
        self.updateGrid()
        try:
            for solution in self.sudoku.solveSudoku(self.sudoku.grid):
                self.sudoku.setGrid(solution)
                self.showSolve()
                return
        except:
            pass
        showinfo("错误","你的数独有误")
        #-----------------------------------------------------------------------
    def updateGrid(self):
        solution=[[0 for i in xrange(9)]for j in xrange(9)]
        for i in xrange(1,18,2):
            for j in xrange(1,18,2):
                if self.SudokuLabel[i][j]["text"] != "":
                    solution[i/2][j/2] = int(self.SudokuLabel[i][j]["text"])
        self.sudoku.setGrid(solution)
        #-----------------------------------------------------------------------
    def showColor(self,color):
        if self.difine:
            return
        self.updateGrid()
        self.sudoku.updateCheck()
        for i in xrange(1,18,2):
            for j in xrange(1,18,2):
                if self.sudoku.check[i/2][j/2] and not self.check[i/2][j/2]:
                    self.SudokuLabel[i][j]["fg"] = color
                elif not self.check[i/2][j/2]:
                    self.SudokuLabel[i][j]["fg"] = "black"
        #-----------------------------------------------------------------------
    def showQuestion(self):
        self.allClear()
        self.check=[[False for i in xrange(9)]for j in xrange(9)]
        for i in xrange(1,18,2):
            for j in xrange(1,18,2):
                if self.sudoku.grid[i/2][j/2] != 0:
                    self.check[i/2][j/2] = True
                    self.SudokuLabel[i][j]["text"] = str(self.sudoku.grid[i/2][j/2])
                    self.SudokuLabel[i][j]["fg"] = "blue"
        #-----------------------------------------------------------------------
    def submit(self):
        if self.difine:
            showinfo("错误","提交无效")
            return
        self.updateGrid()
        self.sudoku.updateCheck()
        for i in xrange(9):
            for j in xrange(9):
                if self.sudoku.check[i][j] or self.sudoku.grid[i][j] == 0:
                    showinfo("提示","你的数独有误")
                    return
        showinfo("恭喜你","数独已完成,若要开始新一局请点击开始按钮")

        
if __name__=="__main__":
    app=MyGUI()
    app.mainloop()
