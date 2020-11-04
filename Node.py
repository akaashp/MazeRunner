import heapq

class Node:

    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.parent = None

    
    def __eq__(self,Node):
        if self.x == Node.x and self.y == Node.y:
            return True
        else:
            return False

    def __str__(self):
        return str(self.x) + " " + str(self.y)

class PriorityQueue:

    def __init__(self):
        self.heap = []
        self.index = 0
    
    def isEmpty(self):
        return self.heap == []
    
    def put(self,priorityNum,Node):#self.index is used to solve the problem of ties
        heapq.heappush(self.heap,(priorityNum,self.index,Node))
        self.index-=1
    
    def get(self):
        return heapq.heappop(self.heap)


