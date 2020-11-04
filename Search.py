from Node import Node
from Node import PriorityQueue
import numpy as np

class Search:
    
    def manhattanD(self, currNode, End):
        return abs(End.y-currNode.x)+abs(End.x-currNode.y)
    
    def euclidianD(self, currNode, End):
        return ((currNode.x - End.x)** 2 + (currNode.y - End.y)** 2)**0.5

    def aStar(self, maze, end1, start1 = Node(0,0)):
        maze.path = []
        start = start1
        end = Node(maze.dim-1,maze.dim-1) if end1 is None else end1
        pq = PriorityQueue()
        pq.put(self.euclidianD(start,end),start)
        fringeMaze = np.copy(maze.maze)
        
        visited = np.zeros((maze.dim,maze.dim), dtype= bool)
        cardinal = [(-1,0), (0,-1), (1,0), (0,1)]
        while not pq.isEmpty(): #add children to fringe (pq) in format (manhattanD, Node)
            #if (i>maze.dim**2): #rare edge case

            currNode = pq.get()[2]
            visited[currNode.x,currNode.y] = True
            
            if end == currNode:
                if (maze.isCopy):
                    return True
                #print("found a path to end")
                
                while True: #write the optimal path
                    maze.path.insert(0,currNode)
                    #maze.maze[currNode.x,currNode.y] = 6
                    currNode = currNode.parent
                    if currNode is None: break
                #maze.printMaze()
                return True
            for mov in cardinal:
                x = currNode.x; y = currNode.y
                x += mov[0]; y += mov[1]
                if (x >= 0 and x < maze.dim and y >=0 and y < maze.dim and 
                not visited[x,y]): #if within bounds of maze and not already visited
                    temp = Node(x,y)
                    
                    if fringeMaze[x,y] == 0 or fringeMaze[x,y] == 1  and not (any(temp == c for a,b,c in pq.heap)): #or fringeMaze[x,y] == 6 to allow backtracking
                        fringeMaze[x,y] = 3
                        temp.parent = currNode
                        pq.put(self.euclidianD(temp,end),temp)
        
        return False
    
    def HUPSAA(self, maze, end1, start1 = Node(0,0)):
        maze.path = []
        start = start1
        end = Node(maze.dim-1,maze.dim-1) if end1 is None else end1
        pq = PriorityQueue()
        pq.put(self.euclidianD(start,end),start)
        fringeMaze = np.copy(maze.maze)
        
        visited = np.zeros((maze.dim,maze.dim), dtype= bool)
        cardinal = [(-1,0), (0,-1), (1,0), (0,1)]
        #fullcardinal = [(-1,0), (0,-1), (1,0), (0,1),(-1,-1), (1,-1), (1,1), (-1,1)]
        while not pq.isEmpty(): #add children to fringe (pq) in format (hueristic, Node)
            #if (i>maze.dim**2): #rare edge case
          
            currNode = pq.get()[2]
            visited[currNode.x,currNode.y] = True
            
            if end == currNode:
                if (maze.isCopy):
                    return True
                while True: #write the optimal path
                    maze.path.insert(0,currNode)
                    currNode = currNode.parent
                    if currNode is None: break
                return True
            for mov in cardinal:
                x = currNode.x; y = currNode.y
                x += mov[0]; y += mov[1]
                if (x >= 0 and x < maze.dim and y >=0 and y < maze.dim and 
                not visited[x,y]): #if within bounds of maze and not already visited
                    temp = Node(x,y)
                    fireProximity = 0

                    if fringeMaze[x,y] == 0 or fringeMaze[x,y] == 1  and not (any(temp == c for a,b,c in pq.heap)):
                        for neighbor in cardinal: #generate fireProximity portion of hueristic based on whether nodes tba are adjacent to fire #can use fullcardinal for diagonals
                            m = neighbor[0]+x; n = neighbor[1]+y
                            if not (m >= 0 and m < maze.dim and n >=0 and n < maze.dim): continue
                            if neighbor[0]+mov[0] == 0 and neighbor[1]+mov[1] == 0: continue #avoid backtrack
                            
                            if fringeMaze[m,n] == 8: 
                                fireProximity+=4

                        fringeMaze[x,y] = 3
                        temp.parent = currNode
                        pq.put(self.euclidianD(temp,end)+fireProximity,temp)
        
        return False
