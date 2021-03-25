# -*- coding: utf-8 -*-
"""
Created on (10//08/2020)

@author: Isaac Altice
"""
import heapq
import math


# The grid values must be separated by spaces, e.g.
# 1 1 1 1 1 
# 1 0 0 0 1
# 1 0 0 0 1
# 1 1 1 1 1
# Returns a 2D list of 1s and 0s
def readGrid(filename):
    #print('In readGrid')
    grid = []
    with open(filename) as f:
        for l in f.readlines():
            grid.append([int(x) for x in l.split()])
    
    f.close()
    #print 'Exiting readGrid'
    return grid
 
 
# Writes a 2D list of 1s and 0s with spaces in between each character
# 1 1 1 1 1 
# 1 0 0 0 1
# 1 0 0 0 1
# 1 1 1 1 1
def outputGrid(grid, start, goal, path):
    #print('In outputGrid')
    filenameStr = 'pathInformed.txt'
 
    # Open filename
    f = open(filenameStr, 'w')
 
    # Mark the start and goal points
    grid[start[0]][start[1]] = 'S'
    grid[goal[0]][goal[1]] = 'G'
 
    # Mark intermediate points with *
    for i, p in enumerate(path):
        if i > 0 and i < len(path)-1:
            grid[p[0]][p[1]] = '*'
 
    # Write the grid to a file
    for r, row in enumerate(grid):
        for c, col in enumerate(row):
            
            # Don't add a ' ' at the end of a line
            if c < len(row)-1:
                f.write(str(col)+' ')
            else:
                f.write(str(col))
 
        # Don't add a '\n' after the last line
        if r < len(grid)-1:
            f.write("\n")
 
    # Close file
    f.close()
    #print('Exiting outputGrid')
    
def heuristicCost(start,goal):
    cost = math.sqrt((start[0] - goal[0])**2)  + math.sqrt((start[1] - goal[1])**2)
    return cost

def informedSearch(grid, start, goal, algorithm):
    if(algorithm == "Greedy"):
        startNode = Node(start,None,0, heuristicCost(start,goal))
        openList = []
        heapq.heappush(openList, (startNode.h, startNode))
        closedList = []
    if(algorithm == "A*"):
        startNode = Node(start,None,0, heuristicCost(start,goal))
        openList = []
        heapq.heappush(openList,(startNode.f, startNode))
        closedList = []
    
    nodesExpanded = 1
    while(len(openList) != 0):
        nextInHeap = heapq.heappop(openList)
        currentNode = nextInHeap[1]
        if(currentNode.value == goal):
            break
        closedList.append(currentNode)
        if(algorithm == "Greedy"):
            expandNodeGreedy(currentNode,openList,closedList,grid,goal)
        if(algorithm == "A*"):
            print(currentNode.value)
            expandNodeA(currentNode,openList,closedList,grid,goal)
        nodesExpanded += 1
        
        
        
       
    path = [] #some path
    if(currentNode.value != goal):
        print("Final path: No path found")
        if(algorithm == "Greedy"):
            print("Local minima: ", end="")
            print(currentNode.value)
    else:
        setPath(currentNode,path)
        print("Final path: ", end="")
        print(path)
    print("Number of nodes expanded: ", end="")
    print(nodesExpanded)
    if(currentNode.value != goal):
        print("Path cost: No path found")
    else:
        print("Path cost: ",end="")
        print(currentNode.g)
        
    return path

    
def getNeighbors(location, grid):
    neighbors = []
    up =  [location[0] - 1, location[1], ]
    right =  [location[0], location[1] + 1]
    down = [location[0] + 1, location[1]]
    left = [location[0], location[1] - 1]
    
    if((up[0] < len(grid) and (up[0] >= 0))  and (grid[up[0]][up[1]] != 0)):
        neighbors.append(up)
    if((right[1] < len(grid[0]) and (right[1] >= 0))  and (grid[right[0]][right[1]] != 0)):
        neighbors.append(right)
    if((down[0] < len(grid) and (down[0] >= 0))  and (grid[down[0]][down[1]] != 0)):
        neighbors.append(down)
    if((left[1] < len(grid[0]) and (left[1] >= 0))  and (grid[left[0]][left[1]] != 0)):
        neighbors.append(left)
     
    return neighbors
    
def expandNodeGreedy(node,openList,closedList,grid,goal):
    location = node.value
    neighbors = getNeighbors(location,grid)
    
    for neighbor in neighbors:
        tempNode = Node(neighbor,node,node.g + grid[neighbor[0]][neighbor[1]], heuristicCost(neighbor,goal))
        if(checkForNodeInOpenList(tempNode, openList) == False and checkForNodeInClosedList(tempNode,closedList) == False):
            heapq.heappush(openList,(tempNode.h,tempNode))
            
def expandNodeA(node,openList,closedList,grid,goal):
    location = node.value
    neighbors = getNeighbors(location,grid)
    
    for neighbor in neighbors:
        tempNode = ((node.g + grid[neighbor[0]][neighbor[1]]) + heuristicCost(neighbor,goal), Node(neighbor,node,node.g + grid[neighbor[0]][neighbor[1]], heuristicCost(neighbor,goal)))
        
        if(checkForNodeInOpenList(tempNode[1], openList) == True):
            newG = tempNode[1].g
            tempList = []
            while(len(openList) != 0):
                    current = (heapq.heappop(openList))
                    if(compareNodes(current[1],tempNode[1])):
                        if(newG < current[1].g):
                            current = tempNode
                            if(checkForNodeInClosedList(current[1],closedList)):
                                closedList.remove(current[1])
                    tempList.append(current)
            for obj in tempList:
                heapq.heappush(openList, obj)
        elif (not(checkForNodeInClosedList(tempNode[1],closedList))):
                heapq.heappush(openList,tempNode)               
                        
            
            
        
def compareNodes(node1, node2):
    if(node1.value == node2.value):
        return True
    else:
        return False

def checkForNodeInOpenList(node,inList):
    found = False
    current = None
    tempList = []
    while(len(inList) != 0):
        current = ((heapq.heappop(inList)))
        tempList.append(current)
        currentNode = current[1]
        if(compareNodes(node,currentNode)):
            found = True
            break
    for n in tempList:
        heapq.heappush(inList,n) 
    return found

def checkForNodeInClosedList(node,inList):
    found = False
    current = None
    tempList = []
    while(len(inList) != 0):
        current = (heapq.heappop(inList))
        tempList.append(current)
        if(compareNodes(node,current)):
            found = True
    for n in tempList:
        inList.append(n)
    return found
    
def setPath(current, path):
    
    while(current.parent is not None):
        path.append(current.value)
        current = current.parent
    path.append(current.value)
    path.reverse()
    
    
def getStart(grid): 
    start = []
    x = input("Enter x coordinate of starting point: ")
    y = input("Enter y coordinate of starting point: ")
    if(x.isdigit() and int(x) >= 0 and int(x) < len(grid[0]) and y.isdigit() and int(y) >= 0 and int(y) < len(grid)):
        start.append(int(x))
        start.append(int(y))       
    else: 
        print("Invalid Start point, using default: [1,1]")
        start = [0,0]
    return start

def getGoal(grid):
    goal = []
    x = input("Enter x coordinate of goal point: ")
    y = input("Enter y coordinate of goal point: ")
    if(x.isdigit() and int(x) >= 0 and int(x) < len(grid[0]) and y.isdigit() and int(y) >= 0 and int(y) < len(grid)):
        goal.append(int(x))
        goal.append(int(y))       
    else: 
        print("Invalid Goal point, using default: [4,4]")
        goal = [2,3]
    return goal
    
class Node:
    algorithm = input("Enter search algorithm Greedy or A*(case sensitive): ")
    if(algorithm == "Greedy" or algorithm == "A*"):
        print("Selected: ", end="")
        print(algorithm)
    else:
        print("Invalid algorithm, using default Greedy")
        algorithm = "Greedy"
    
    
    def changeAlgorithm(inAlgorithm):
        return inAlgorithm
        
    def __init__(self, inValue = [],inParent = None,inG = 0.00,inH = 0.00):
        self.value = inValue
        self.parent = inParent
        self.g = inG
        self.h = inH
        self.f = self.g + self.h
        
        
        
    if(algorithm == "Greedy"):
        def __lt__(self,other):
            return self.h < other.h
        
        def __gt__(self,other):
            return self.h > other.h
        
        def __le__(self,other):
            return self.h <= other.h
        
        def __ge__(self,other):
            return self.h >= other.h
    elif(algorithm == "A*"):
        def __lt__(self,other):
            return self.f < other.f
        
        def __gt__(self,other):
            return self.f > other.f
        
        def __le__(self,other):
            return self.f <= other.f
        
        def __ge__(self,other):
            return self.f >= other.f
        
        
    def __eq__(self,other):
        return self.value == other.value
    
    def __ne__(self,other):
        return not self.__eq__(other)
    
def main():
    filename = "gridInformed.txt"
    grid = readGrid(filename)
    start = []
    goal = []
    
    print("Grid read from file:")
    for row in range(len(grid)):
        for column in range(len(grid[row])):
            print(grid[row][column], end=" ")
        print()
    
    start = getStart(grid)
    goal = getGoal(grid)
    
    print()
    print("Starting search, type: " + Node.algorithm)
    print("Start: ",end="")
    print(start)
    print("Goal: ", end="")
    print(goal)
    print("Heuristic function: Manhattan distance")
    print()
    
    
    outputGrid(grid,start,goal,informedSearch(grid,start,goal,Node.algorithm))
    
    print("Path written to file path.txt")
    
 
main()

