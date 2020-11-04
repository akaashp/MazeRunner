from FireMaze import *
from Node import *
from Search import *
from timeit import default_timer as timer
import numpy as np
from matplotlib import pyplot as plt


def Approach1(Map):
    traveledPath = []
    for node in Map.path:
        if not Map.fireArr: return 1
        state = Map.fireArr[0]
        x = node.x; y = node.y
        if not (state[x,y] == 0 or state[x,y] == 1): 
            #print("agent on fire!",state[x,y])
            return 2 
        traveledPath.append((x,y))
        for x,y in traveledPath:
            state[x,y] = 6 #if state[x,y] == 0 or state[x,y] == 1 else  state[x,y]
        Map.setNextState()
        #Map.printMaze() 
    
    #print("reached end!")
    return 4
          
def Approach2(Map):
    path = Search()
    traveledPath = []
    while Map.path:
        node = Map.path.pop(0)
        if not Map.fireArr: return 1
        state = Map.fireArr[0]
        x = node.x; y = node.y
        if not (state[x,y] == 0 or state[x,y] == 1):
            #print("agent on fire! at ",x,y)
            return 2
        traveledPath.append((x,y))
        for x,y in traveledPath:
            state[x,y] = 6 #if state[x,y] == 0 or state[x,y] == 1 else  state[x,y]
        Map.setNextState()
        #Map.printMaze() 
        temp = Node(node.x,node.y)
        if not path.aStar(Map, end1 = None,start1 = temp): 
            #print("no path to finish")
            return 3
        Map.path.pop(0)
    
    #print("reached end!")
    return 4

def Approach3(Map):
    path = Search()
    traveledPath = []
    while Map.path:
        node = Map.path.pop(0)
        if not Map.fireArr: return 1
        state = Map.fireArr[0]
        x = node.x; y = node.y
        if not (state[x,y] == 0 or state[x,y] == 1):
            #print("agent on fire! at ",x,y)
            return 2
        traveledPath.append((x,y))
        for x,y in traveledPath:
            state[x,y] = 6 #if state[x,y] == 0 or state[x,y] == 1 else  state[x,y]
        Map.setNextState()
        #Map.printMaze() #uncomment this to print maze at each step the agent takes
        temp = Node(node.x,node.y)
        if not path.HUPSAA(Map, end1 = None,start1 = temp): 
            #print("no path to finish")
            return 3
        Map.path.pop(0)
    
    #print("reached end!")
    return 4

def runAll(dim,p,q,iterations):
    #####################################################################################
    #ResultsArr notation
    #index 0 = #of mazes w/ no initial path to finish
    #index 1 = #of mazes w/ no initial path from fire to agent 
    #index 2 = #of good mazes which agent sets on fire
    #index 3 = #of good mazes which no longer have a viable path to end
    #index 4 = #of good mazes which agent reaches the end
    #####################################################################################
    resultsArr = np.zeros((3,5))
    goodMazes = 0
    t1=t2=t3 = 0
    while goodMazes <iterations: #generate the same 500 good mazes with same fire position
        Map = FireMaze()
        Map.generateMaze(dim,p,q)
        if not Map.initFire() : #no path from fire to agent
            continue
        map2 = Map.copy()
        map3 = Map.copy()
        path = Search()
        if not path.aStar(Map, end1 = None): #no path to finish
            continue
        if not path.aStar(map2, end1 = None): 
            continue
        
        if not path.HUPSAA(map3, end1 = None): 
            continue

        start = timer()
        check1 = Approach1(Map) #to account for rare bad maze bug
        if check1 ==1: continue
        resultsArr[0][check1]+=1
        end = timer()
        t1 += end-start
        
        start = timer()
        check2 = Approach2(map2)
        resultsArr[1][check2]+=1
        end = timer()
        t2 += end-start
        
        start = timer()
        check3 = Approach3(map3)
        resultsArr[2][check3]+=1
        end = timer()
        t3 += end-start
        if check1 == 4 and check2 == 4 or check3==4: 
          Map.printMaze()
          map2.printMaze()
          map3.printMaze()
        goodMazes+=1

    #print(resultsArr)
    #print("Approach1 time: ",t1,"\nApproach2 time: ",t2,"\nApproach3 time: ",t3)
    return ((resultsArr[0][4],resultsArr[1][4],resultsArr[2][4],t1,t2,t3))

#use below section to generate the data and show the successes vs flammability graph
'''
qVals = np.arange(0.0,1.05,.05)
print(qVals)
A1Successes = []; avg1 = 0
A2Successes = []; avg2 = 0
A3Successes = []; avg3 = 0
for q in qVals:
    tup = runAll(100,.3,q,10)
    A1Successes.append(tup[0])
    A2Successes.append(tup[1])
    A3Successes.append(tup[2])
    avg1 += tup[3]; avg2 += tup[4]; avg3 += tup[5]

avg1 = avg1/100; avg2 = avg2/100; avg3 = avg3/100; 
print("A1: ",avg1,"A2: ",avg2,"A3",avg3)
plt.figure(figsize = (10,6))
colors = ["orange","cyan","purple"]
colormap =  matplotlib.colors.ListedColormap(colors)
plt.plot(qVals,A1Successes,label="Approach 1: A*")
plt.plot(qVals,A2Successes,label="Approach 2: Adaptive A*")
plt.plot(qVals,A3Successes,label="Approach 3: HUPSAA")
plt.xticks(qVals)
plt.title("Average Successes vs Flammability" )
plt.xlabel("Flammability (q)")
plt.ylabel("Successes")
plt.legend()
plt.show()
'''

