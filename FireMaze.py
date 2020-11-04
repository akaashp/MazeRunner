import numpy as np
from matplotlib import pyplot as plt
import matplotlib.colors
import random as rand
from Search import *
from Node import *
import copy

class FireMaze:

    def __init__(self): #set default values for a maze
        self.maze = np.zeros((15,15), dtype= int)
        self.dim = 15
        self.p = .3
        self.q = .3
        self.walls = 0
        self.fireList = []
        self.path = []
        self.isCopy = False
        self.fireArr = [] #store next dim x dim iterations of fireMazes

    def generateMaze(self,dim,p,q): #generate a new maze given the parameters dim, p, q
        self.maze = np.zeros((dim,dim), dtype= int)
        self.dim = dim
        self.p = p
        self.q = q

        self.maze[0,0] = self.maze[dim-1,dim-1] = 1

        for i in range(dim):
            for j in range(dim):
                if i == 0 and j == 0 or i== dim-1 and j == dim-1 :
                    continue
                
                if rand.random() <= self.p:
                    self.maze[i,j] = 10  
                    self.walls+=1
                else:
                    self.maze[i,j] = 0
    
    def copy(self): # deep copy
        newFireMaze = FireMaze()
        newFireMaze.maze = np.copy(self.maze)
        newFireMaze.dim = self.dim
        newFireMaze.p = self.p
        newFireMaze.q = self.q
        newFireMaze.walls = self.walls
        newFireMaze.path = copy.deepcopy(self.path)
        newFireMaze.fireList = self.fireList
        newFireMaze.fireArr = copy.deepcopy(self.fireArr)
        newFireMaze.isCopy = self.isCopy
        return newFireMaze

    def spreadFire(self):
        tempList = {} #key is (x,y). 1 - val is probability of setting cell on fire
        cardinal = [(-1,0), (0,-1), (1,0), (0,1)]
        tempMaze = np.copy(self.fireArr[-1])
        for x,y in self.fireList:
            tempx = x; tempy = y
            for mov in cardinal:
                x = tempx; y = tempy
                x += mov[0]; y += mov[1]
                if (x >= 0 and x < self.dim and y >=0 and y < self.dim):
                    if tempMaze[x,y] == 0:
                        if tempList.get((x,y)) is not None:
                            tempList[(x,y)] = tempList[(x,y)]*(1-self.q)
                        else:
                            tempList[(x,y)] = (1-self.q)
        if len(tempList)==0:
            return False
        for key, val in tempList.items():
            x = key[0]; y = key[1]
            if rand.random() <= 1-val :
                tempMaze[x,y] = 8
                self.fireList.append((x,y))
                
        self.fireArr.append(tempMaze)
        return True

    
    def generateAllFire(self):
        
        for i in range(self.dim**2):
            if len(self.fireList) >= self.dim**2-self.walls-2:
                break  
            if not self.spreadFire():
                break

    def initFire(self):
        tempMaze = self.copy()
        tempMaze.isCopy = True
        dim = tempMaze.dim
        i = 0
        while True: #set a random position on fire (must have route to start)
            if i >dim**2: return False #try to init fire dim**2 worst case
            i+=1
            x = rand.randint(0,dim-1); y = rand.randint(0,dim-1)
            if tempMaze.maze[x,y] == 0:
                if Search().aStar(tempMaze, end1 = Node(x,y)):
                    self.maze[x,y] = 8
                    self.fireList.append((x,y))
                    self.fireArr.append(self.maze)
                    break
                    
        self.generateAllFire()
        return True
                  

    def setNextState(self):
        self.maze = self.fireArr.pop(0)
    
    def printMaze(self): #display the maze
        plt.figure(figsize = (6,6))
        colors = ["beige", "beige", "orange","cyan","orange", "black"]
        colormap =  matplotlib.colors.ListedColormap(colors)
        plt.pcolor(self.maze,edgecolors = "black", cmap = colormap, linewidths = 1)
        plt.tight_layout()
        plt.gca().invert_yaxis()
        plt.show() #block=False
        #plt.pause(.2)
        #plt.close()
