import numpy

def getIndexOfState(S, x, y):
    """ Get the index of the state that contains the (x,y) position in S
    
    Parameters:
        S (list): list of State objects
        x (integer): x coordinate of a cell
        y (integer): y coordinate of a cell
        
    Returns:
        int: in range [0,len(S)-1] if the position can be found. -1 otherwise
    """
    for i,s in enumerate(S):
        if s.x == x and s.y == y:
            return i
    return -1

def getPolicyForGrid(S, U, A, P, i_terminal_states):
    """ Computes the policy as a list of characters indicating which direction to move in at the state
    
    Parameters:
        S (list): States
        U (numpy array): Utilities
        A (list): Actions
        P (numpy array): Transition model matrix
        i_terminal_states (list): Indices of the terminal states
        
    Returns:
        list: 1d list of characters that indicate the action to take at each state
    """
    policy = []
    
    for i_s, s in enumerate(S):
        i_states = []
        
        # If it's a terminal state, then make the action be 'T'
        if i_s in i_terminal_states:
            action = 'T'
            
        # Otherwise, find the action that gives the best utility
        else:
            i_states = []
            
            # Get the index of each neighbor for a state
            i_up = getIndexOfState(S, s.x, s.y+1)
            i_right = getIndexOfState(S, s.x+1, s.y)
            i_down = getIndexOfState(S, s.x, s.y-1)
            i_left = getIndexOfState(S, s.x-1, s.y)                       
            
            # Check to make sure each one is not an obstacle            
            if i_up != -1:
                i_states.append(i_up)
                    
            if i_right != -1:
                i_states.append(i_right)
                
            if i_down != -1:
                i_states.append(i_down)                
                
            if i_left != -1:
                i_states.append(i_left)
                  
            # Append the state itself to consider the agent bouncing off the boundary
            i_states.append(i_s)
            
            # Calculate the expected utilities for each action in the state
            i_a_max_eu = 0
            max_eu = -100000 # don't wait to loop for i_a=0...
            for i_a, a in enumerate(A):
        
                # Get the expected utility for an action
                eu = 0                
                for i_neighbor in i_states:
                    u_s_prime = U[i_neighbor]
                    prob_s_prime = P[i_a, i_s, i_neighbor]
                    eu += (prob_s_prime * u_s_prime)

                # Check if max expected utility
                if eu > max_eu:
                    max_eu = eu
                    i_a_max_eu = i_a
            
            # Set the action character
            action = A[i_a_max_eu]
            
        # Add the action to the policy
        policy.append(action)              
    
    return policy
    

def printPolicyForGrid(policy, w, h, i_obs):
    """ Print out a policy in the form:
        ['r', 'r', 'r', 'T']
        ['u', '0', 'u', 'T']
        ['u', 'l', 'l', 'l']
        where the characters indicate the action to take at each state. 
        '0' elements are obstacles in the grid.
        
    Parameters:
        policy (list): 1d list of characters indicating which action to take for each state
        w (int): width of the grid
        h (int): height of the grid
        i_obs(list): list of indices where obstacles are located
        
    Returns:
        None
    """
    
    # Insert 0's for obstacle tiles
    for i_ob in i_obs:
        policy.insert(i_ob, '0')   

    # Blank line to isolate the policy
    print('\n')
    
    # Start at top of the grid, and print each row
    for y in range(h-1,-1,-1):
        row = [policy[ ((w*y)+i) ] for i in range(0,w)]
        print(row)
   
def valueIteration(S,A,P,R_states,discount,terminal_index_reward_pairs):
    epsilon = 0.00000001 #error to stop algorithm on,error between 2 iterations
    gamma = discount #discount, y looking thing
    U  = numpy.array([[0.0],[0.0],[0.0],[0.0],[0.0],[0.0],[-1.0],[0.0],[0.0],[0.0],[1.0]]) #current utilities
    U_prime =numpy.array([[0.0],[0.0],[0.0],[0.0],[0.0],[0.0],[-1.0],[0.0],[0.0],[0.0],[1.0]]) #next utiliteis
    delta = 1 #max change of difference of utilities any state in a iteration
    
    while(delta > epsilon):
        U = U_prime.copy()
        delta = 0.0
        for index,s in enumerate(S):
            if(index != tr[0] and index != tr[1]):
                U_prime[index] = R_states[index] + (gamma * getExpectedUtility(P,U, index, S,A))
                if (abs(U_prime[index] - U[index]) > delta):
                    delta = (abs(U_prime[index] - U[index]))
    return U;

def getExpectedUtility(P,U, stateIndex,S,A):
    U_list = []
    for index,a in enumerate(A):
        total = 0.0
        i = index
        for index1,s in enumerate(S):
            j = index1
            total += P[i][stateIndex][j] * U[j]
        U_list.append(total)
        
    return max(U_list)
    
class State:
    x = 0
    y = 0
    def __init__(self, numX, numY):
        x = numX
        y = numY

S = [State(1,1),State(1,2),State(1,3),State(1,4),State(2,1),State(2,3),State(2,4),State(3,1),State(3,2),State(3,3),State(3,4)]  
#S = [State(0,0),State(0,1),State(0,2),State(0,3),State(1,0),State(1,2),State(1,3),State(2,0),State(2,1),State(2,2),State(2,3)] #stateobjects

w= 4
h = 3   
discount = 1.0
reward = -0.04
tr =[6,10] # location of terminal values, used so we dont have to do iterations on them
R_states = numpy.array([[reward],[reward],[reward],[reward],[reward],[reward],[-1],[reward],[reward],[reward],[1]]) #awards array?
A = ['u','r','d','l'] #actions
        
# P is the transition model matrix for the 4x3 grid world problem
# P gets converted to a numpy array after it is hard-coded here
# actions are in order: up, right, down, left
# rows -> s
# cols -> s'
# [action, state, outcome], [a, s, s']
P = [[[0.1, 0.1, 0.,  0.,  0.8, 0.,  0.,  0.,  0.,  0.,  0.],
  [0.1, 0.8, 0.1, 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0. ],
  [0.,  0.1, 0.,  0.1, 0.,  0.8, 0.,  0.,  0.,  0.,  0. ],
  [0.,  0.,  0.1, 0.1, 0.,  0.,  0.8, 0.,  0.,  0.,  0. ],
  [0.,  0.,  0.,  0.,  0.2, 0.,  0.,  0.8, 0.,  0.,  0. ],
  [0.,  0.,  0.,  0.,  0.,  0.1, 0.1, 0.,  0.,  0.8, 0. ],
  [0.,  0.,  0.,  0.,  0.,  0.1, 0.1, 0.,  0.,  0.,  0.8],
  [0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.9, 0.1, 0.,  0. ],
  [0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.1, 0.8, 0.1, 0. ],
  [0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.1, 0.8, 0.1],
  [0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.1, 0.9]],

 [[0.1, 0.8, 0.,  0.,  0.1, 0.,  0.,  0.,  0.,  0.,  0. ],
  [0.,  0.2, 0.8, 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0. ],
  [0.,  0.,  0.1, 0.8, 0.,  0.1, 0.,  0.,  0.,  0.,  0. ],
  [0.,  0.,  0.,  0.9, 0.,  0.,  0.1, 0.,  0.,  0.,  0. ],
  [0.1, 0.,  0.,  0.,  0.8, 0.,  0.,  0.1, 0.,  0.,  0. ],
  [0.,  0.,  0.1, 0.,  0.,  0.,  0.8, 0.,  0.,  0.1, 0. ],
  [0.,  0.,  0.,  0.1, 0.,  0.,  0.8, 0.,  0.,  0.,  0.1],
  [0.,  0.,  0.,  0.,  0.1, 0.,  0.,  0.1, 0.8, 0.,  0. ],
  [0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.2, 0.8, 0. ],
  [0.,  0.,  0.,  0.,  0.,  0.1, 0.,  0.,  0.,  0.1, 0.8],
  [0.,  0.,  0.,  0.,  0.,  0.,  0.1, 0.,  0.,  0.,  0.9]],

 [[0.9, 0.1, 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0. ],
  [0.1, 0.8, 0.1, 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0. ],
  [0.,  0.1, 0.8, 0.1, 0.,  0.,  0.,  0.,  0.,  0.,  0. ],
  [0.,  0.,  0.1, 0.9, 0.,  0.,  0.,  0.,  0.,  0.,  0. ],
  [0.8, 0.,  0.,  0.,  0.2, 0.,  0.,  0.,  0.,  0.,  0. ],
  [0.,  0.,  0.8, 0.,  0.,  0.1, 0.1, 0.,  0.,  0.,  0. ],
  [0.,  0.,  0.,  0.8, 0.,  0.1, 0.1, 0.,  0.,  0.,  0. ],
  [0.,  0.,  0.,  0.,  0.8, 0.,  0.,  0.1, 0.1, 0.,  0. ],
  [0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.1, 0.8, 0.1, 0. ],
  [0.,  0.,  0.,  0.,  0.,  0.8, 0.,  0.,  0.1, 0.,  0.1],
  [0.,  0.,  0.,  0.,  0.,  0.,  0.8, 0.,  0.,  0.1, 0.1]],

 [[0.9, 0.,  0.,  0.,  0.1, 0.,  0.,  0.,  0.,  0.,  0. ],
  [0.8, 0.2, 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0. ],
  [0.,  0.8, 0.1, 0.,  0.,  0.1, 0.,  0.,  0.,  0.,  0. ],
  [0.,  0.,  0.8, 0.1, 0.,  0.,  0.1, 0.,  0.,  0.,  0. ],
  [0.1, 0.,  0.,  0.,  0.8, 0.,  0.,  0.1, 0.,  0.,  0. ],
  [0.,  0.,  0.1, 0.,  0.,  0.8, 0.,  0.,  0.,  0.1, 0. ],
  [0.,  0.,  0.,  0.1, 0.,  0.8, 0.,  0.,  0.,  0.,  0.1],
  [0.,  0.,  0.,  0.,  0.1, 0.,  0.,  0.9, 0.,  0.,  0. ],
  [0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.8, 0.2, 0.,  0. ],
  [0.,  0.,  0.,  0.,  0.,  0.1, 0.,  0.,  0.8, 0.1, 0. ],
  [0.,  0.,  0.,  0.,  0.,  0.,  0.1, 0.,  0.,  0.8, 0.1]]]
P = numpy.array(P)



U = (valueIteration(S,A,P,R_states,discount,tr))


print('Discount = %s ' % discount)
print('Reward = %s' % reward)
print('Utilities: %s' % U)

I_terminals = [6,10]

policy = getPolicyForGrid(S,U,A,P, I_terminals)

print('Policy: %s' % policy)

printPolicyForGrid(policy,w,h,[5])