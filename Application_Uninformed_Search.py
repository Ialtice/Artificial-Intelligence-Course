# -*- coding: utf-8 -*-
"""
Created on (10//08/2020)

@author: Isaac Altice
"""
import queue

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
    filenameStr = 'path.txt'
 
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
    
    
def uniformedSearch(grid, start, goal, algorithm):
    if(algorithm == "bfs"):
        openList = queue.Queue()
        closedList = queue.Queue()
    if(algorithm == "dfs"):
        openList = queue.LifoQueue()
        closedList = queue.Queue()
    
    openList.put(Node(start))
    nodesExpanded = 0
    while(openList.empty() != True):
        current = openList.get()
        if(current.value == goal):
            break
        
        expandNode(current,openList,closedList,grid,algorithm)
        nodesExpanded += 1
        closedList.put(current)
        
    path = [] #some path
    if(current.value != goal):
        print("Final path: No path found")
    else:
        setPath(current,path)
        print("Final path: ", end="")
        print(path)
    print()
    print("Number of nodes expanded: ", end="")
    print(nodesExpanded)
    if(current.value != goal):
        print("Path cost: No path found")
    else:
        print("Path cost: ",end="")
        print(len(path) - 1)
        
    return path

    
def getNeighbors(location, grid):
    neighbors = []
    up =  [location[0] - 1, location[1]]
    right =  [location[0], location[1] + 1]
    down = [location[0] + 1, location[1]]
    left = [location[0], location[1] - 1]
    
    if((grid[up[0]][up[1]] == 0) and (up[0] < len(grid) and (up[0] >= 0))):
        neighbors.append(up)
    if(grid[right[0]][right[1]] == 0) and (right[1] < len(grid[0]) and right[1] >= 0):
        neighbors.append(right)
    if((grid[down[0]][down[1]] == 0) and (down[0] < len(grid) and down[0] >= 0)):
        neighbors.append(down)
    if(grid[left[0]][left[1]] == 0) and (left[1] < len(grid[0]) and left[1] >= 0):
        neighbors.append(left)
     
    return neighbors
    
def expandNode(node,openList,closedList,grid,algorithm):
    location = node.value
    neighbors = getNeighbors(location,grid)
    
    for neighbor in neighbors:
        tempNode = Node(neighbor)
        if(checkForNodeInList(tempNode, openList,algorithm) == False and checkForNodeInList(tempNode,closedList,algorithm) == False):
            tempNode.parent = node
            openList.put(tempNode)
            
        

def compareNodes(node1, node2):
    if(node1.value == node2.value):
        return True
    else:
        return False

def checkForNodeInList(node,inList,algorithm):
    found = False
    current = None
    tempList = []
    while(inList.empty() != True):
        current = (inList.get())
        tempList.append(current)
        if(compareNodes(node,current)):
            found = True
            
    if(algorithm == "bfs"):
        for n in tempList:
            inList.put(n)
    else:
        tempList.reverse()
        for n in tempList:
            inList.put(n)
            
    return found
    
def setPath(current, path):
    
    while(current.parent != None):
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
        start = [1,1]
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
        goal = [4,4]
    return goal
    
class Node:
    value = []
    parent = None
    
    def __init__(self, inValue = None):
        self.value = inValue
        self.parent = None
        

def main():
    filename = "grid.txt"
    grid = readGrid(filename)
    start = []
    goal = []
    
    print("Grid read from file:")
    print(grid)
    
    start = getStart(grid)
    goal = getGoal(grid)
    
    algorithm = input("Enter bfs or dfs:")
    if not(algorithm != "bfs" or algorithm != "dfs"):
        print("Invalid algorithm, using default bfs")
        algorithm = "bfs"
        
    print("Starting search, type: " + algorithm)
    print("Start: ",end="")
    print(start)
    print("Goal: ", end="")
    print(goal)
    print()
    
    outputGrid(grid,start,goal,uniformedSearch(grid,start,goal,algorithm))
    
    print("Path written to file path.txt")
    
    
main()

