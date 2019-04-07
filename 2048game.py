from tkinter import *
import random as r
from tkinter import messagebox as mb

class window:

    def __init__(self):
        self.Btns = []
        self.Btnst = []
        self.Titlelb = Label(tk, text = "2048", font = "arial 43 bold", fg = "orange")
        self.Titlelb.place(x = 8, y = 5)
        self.restlb = Label(tk, text = "Новая игра", font = "arial 20 bold")
        self.restlb.place(x = 8, y = 68)
        self.statlb = Label(tk, text = "Счёт", font = "arial 20 bold", justify = RIGHT)
        self.statlb.place(x = 320, y = 15)
        self.testVar = StringVar()
        self.testVar.set("0")
        self.testlb = Label(tk, textvariable = self.testVar, font = "arial 20 bold", justify = RIGHT)
        self.testlb.place(x = 320, y = 47)

        
        self.colors = {0: "#ccc0b4",
                       2: "#eee4da",
                       4: "#ece0c8",
                       8: "#f2d179",
                       16: "#ec8d53",
                       32: "#f57c5f",
                       64: "#e95937",
                       128: "#f3d96b",
                       256: "#f1d04b",
                       512: "#e4c02a",
                       1024: "#e3ba14",
                       2048: "#ecc400"}
        tk.bind('<KeyPress>', self.onKeyPress)
        self.restlb.bind('<Button 1>', self.click)
                       

        for i in range(4):
            lineBtns = []
            lineBtnst = []
            for j in range(4):
                lineBtnst.append(StringVar())
                lineBtnst[j].set(2048)
                lineBtns.append(Button(tk, width = 5, textvariable = lineBtnst[j], font = "arial 24 bold", height = 2))
                lineBtns[j].place(x = j * 95 + 7, y = i * 95 + 107)
            self.Btns.append(lineBtns)
            self.Btnst.append(lineBtnst)
            

        self.newgame()

    def click(self, event):
        self.newgame()

    def newgame(self):
        self.game = Game()
        self.game.np()
        self.game.np()        
        self.refresh() 


    def onKeyPress(self, event):
        if event.keycode == 38:
            self.game.move(1)
            self.refresh()
        elif event.keycode == 40:
            self.game.move(2)
            self.refresh()
        elif event.keycode == 37:
            self.game.move(3)
            self.refresh()
        elif event.keycode == 39:
            self.game.move(4)
            self.refresh()
        

    def refresh(self):
        self.testVar.set(self.game.score)
        if self.game.islose == True:
            a = mb.askyesno("Вы проиграли", "Начать заново?")
            if a == True:
                self.newgame()
            else:
                tk.destroy()
                return
        for i in range(4):
            for j in range(4):
                if self.game.map[i][j] != 0:
                    self.Btnst[i][j].set(self.game.map[i][j])
                else:
                    self.Btnst[i][j].set("")

                self.Btns[i][j].configure(bg = self.colors[self.game.map[i][j]])
        for i in range(4):
            for j in range(4):
                if self.game.map[i][j] == 2048:
                    a = mb.askyesno("Вы проиграли", "Начать заново?")
                    if a == True:
                        self.newgame()
                    else:
                        tk.destroy()
                        return
                    
class Game:
    def __init__(self):
        self.score = 0
        self.islose = False
        self.map = []
        for i in range(4):
            line = []
            for j in range(4):
                line.append(0)
            self.map.append(line)
       
    def np(self):
        free = []        
        for i in range(4):
            for j in range(4):
                if self.map[i][j] == 0:
                    point = []
                    point.append(i)
                    point.append(j)
                    free.append(point)
        
        p = r.choice(free)
        v = [2,2,2,2,2,2,2,2,2,4]
        self.map[p[0]][p[1]] = r.choice(v)

    def sumP(self, line):
        l = 0
        while l < len(line) - 1:
            if line[l] == line[l + 1]:
                line[l] *= 2
                self.score += line[l]
                del line[l + 1]
            l += 1
        return line
    
    def move(self, x):
        self.islose = True
        for i in range(3):
            for j in range(3):
                if (self.map[i][j] == self.map[i][j + 1]) or (self.map[i][j] == self.map[i + 1][j]) or (self.map[i][j + 1] == self.map[i + 1][j + 1]) or (self.map[i + 1][j] == self.map[i + 1][j + 1]):
                    self.islose = False
        for i in range(4):
            for j in range(4):
                if self.map[i][j] == 0:
                    self.islose = False
        if self.islose == True:
            return
                
        if x == 1:
            ispos = False
            for j in range(4):
                for i in range(3):
                    if (self.map[i][j] == self.map[i + 1][j] and self.map[i][j] != 0) or (self.map[i][j] == 0 and self.map[i + 1][j] != 0):
                        ispos = True
            if not ispos:
                return

            for j in range(4):
                line = []
                for i in range(4):
                    line.append(self.map[i][j])
                    self.map[i][j] = 0
                while 0 in line:
                    line.remove(0)
                self.sumP(line)

                for i in range(len(line)):
                    self.map[i][j] = line[i]
            self.np()

        elif x == 2:
            ispos = False
            for j in range(4):
                for i in range(3, 0, -1):
                    if (self.map[i][j] == self.map[i - 1][j] and self.map[i][j] != 0) or (self.map[i][j] == 0 and self.map[i - 1][j] != 0):
                        ispos = True
            if not ispos:
                return

            for j in range(4):
                line = []
                for i in range(4):
                    line.append(self.map[i][j])
                    self.map[i][j] = 0
                while 0 in line:
                    line.remove(0)
                line.reverse()
                self.sumP(line)
                while len(line) < 4:
                    line.append(0)
                line.reverse()

                for i in range(len(line)):
                    self.map[i][j] = line[i]
            self.np()

        elif x == 3:
            ispos = False
            for i in range(4):
                for j in range(3):
                    if (self.map[i][j] == self.map[i][j + 1] and self.map[i][j] != 0) or (self.map[i][j] == 0 and self.map[i][j + 1] != 0):
                        ispos = True
            if not ispos:
                return

            for i in range(4):
                line = []
                for j in range(4):
                    line.append(self.map[i][j])
                    self.map[i][j] = 0
                while 0 in line:
                    line.remove(0)
                self.sumP(line)
                for j in range(len(line)):
                    self.map[i][j] = line[j]
            self.np()

        elif x == 4:
            ispos = False
            for i in range(4):
                for j in range(3, 0, -1):
                    if (self.map[i][j] == self.map[i][j - 1] and self.map[i][j] != 0) or (self.map[i][j] == 0 and self.map[i][j - 1] != 0):
                        ispos = True
            if not ispos:
                return

            for i in range(4):
                line = []
                for j in range(4):
                    line.append(self.map[i][j])
                    self.map[i][j] = 0
                while 0 in line:
                    line.remove(0)
                line.reverse()
                self.sumP(line)
                while len(line) < 4:
                    line.append(0)
                line.reverse()

                for j in range(len(line)):
                    self.map[i][j] = line[j]
            self.np()
                    
        
        
                    

tk = Tk()
tk.geometry("400x500+300+150")
tk.resizable(False, False)
tk.title("2048")
wn = window()


tk.mainloop()
