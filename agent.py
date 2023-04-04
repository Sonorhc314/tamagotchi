from priorityqueue import PriorityQueue


class Frontier:
    # Note the heuristic function is passed in as a parameter
    # Python borrows some nice features from functional programming
    def __init__(self, heuristic, start_node=None):
        self.heuristic = heuristic

        self.queue = PriorityQueue()
        self.states = set()

        if start_node is not None:
            self.push(start_node)
            
    def push(self, node):
        cost = self.heuristic(node)
        # get_priority returns math.inf if the task is not in the queue
        if cost < self.queue.get_priority(node):
            self.queue.push(node, priority=cost)
            self.states.add(node.state)
        
    def pop(self):
        node = self.queue.pop()
        self.states.remove(node.state)
        return node
        
    def contains(self, state):
        return state in self.states
    
    def length(self):
        return self.queue.length()
    
def valid_space(maze, space):
    return 0 <= space[0] < len(maze) \
           and 0 <= space[1] < len(maze[0]) \
           and maze[space[0]][space[1]] == '1'

class Node:
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
        if parent is None:
            self.path_cost = 0
        else:
            self.path_cost = parent.path_cost + 1

    def __eq__(self, other):
        return self.state == other.state

    def __lt__(self, other):
        return self.state < other.state

    def __hash__(self):
        return hash(self.state)

    def __str__(self):
        return f"Node space {self.state}"
    
def a_star_search(maze, start, goal):

    maze[goal[0]][goal[1]] = '1'
    # This is the key line that turns the greedy search into A*
    heuristic = lambda node: node.path_cost + \
                            abs(goal[0] - node.state[0]) + abs(goal[1] - node.state[1])
    frontier = Frontier(heuristic, Node(start))
    explored = set()

    current_node = frontier.pop()
    number_explored = 0
    
    while not current_node.state == goal:
        current_state = current_node.state

        number_explored += 1
        explored.add(current_state)
        
        # the four neigbouring locations
        right = (current_state[0], current_state[1] + 1)
        left = (current_state[0], current_state[1] - 1)
        down = (current_state[0] + 1, current_state[1])
        up = (current_state[0] - 1, current_state[1])
        
        for space in [right, left, down, up]:
            if valid_space(maze, space) \
            and space not in explored:
                node = Node(space, parent=current_node)
                frontier.push(node)

        if frontier.length() == 0:
            return None, number_explored

        current_node = frontier.pop()
    
    return current_node, number_explored

# The main code is mostly the same as above, just have to call the correct function!

def run_path(maze, start, finish, my_turn):
    final_node, number_explored = a_star_search(maze, start, finish)
    coordinates=[]
    if final_node is None:
        return
        #print("No path exists!\n")
    else:
        node = final_node
        steps = 0
        while node.parent is not None:
            state = node.state
            coordinates.append(state)
            maze[state[0]][state[1]] = 'X'
            steps += 1
            node = node.parent

        state = node.state
        coordinates.append(state)
        maze[state[0]][state[1]] = 'X'
        
        #print(f"Total steps on path: {steps}")
        #print(f"Total states explored: {number_explored}")

    coordinates.reverse()
    def actions(coordinates, turn): #4
        actions_arr=[]
        for xy in range(len(coordinates)-1):
            if coordinates[xy+1][1]<coordinates[xy][1]:
                turn_gone=4
                if turn_gone>turn:
                    while(turn<turn_gone):
                        actions_arr.append("R")
                        turn=turn+1
                if turn_gone==turn:
                    actions_arr.append("F")
            elif coordinates[xy+1][1]>coordinates[xy][1]:
                turn_gone=2
                if turn_gone>turn:
                    while(turn<turn_gone):
                        actions_arr.append("R")
                        turn=turn+1
                elif turn_gone<turn:
                    while(turn>turn_gone):
                        actions_arr.append("L")
                        turn=turn-1
                if turn_gone==turn:
                    actions_arr.append("F")
            elif coordinates[xy+1][0]<coordinates[xy][0]:
                turn_gone = 1
                if turn_gone<turn:
                    while(turn>turn_gone):
                        #print(coordinates[xy+1])
                        actions_arr.append("L")
                        turn=turn-1
                if turn_gone==turn:
                    #print(coordinates[xy])
                    actions_arr.append("F")
            elif coordinates[xy+1][0]>coordinates[xy][0]:
                turn_gone = 3
                if turn_gone<turn:
                    while(turn>turn_gone):
                        actions_arr.append("L")
                        turn=turn-1
                elif turn_gone>turn:
                    while(turn<turn_gone):
                        actions_arr.append("R")
                        turn=turn+1
                if turn_gone==turn:
                    actions_arr.append("F")
        actions_arr.pop()
        return actions_arr, turn, coordinates[xy]

    def replace_elements(lst):
        result = []
        i = 0
        while i < len(lst):
            if i+2 < len(lst) and lst[i] == lst[i+1] == lst[i+2]:
                if lst[i] == 'L':
                    result.append('R')
                elif lst[i] == 'R':
                    result.append('L')
                i += 3
            else:
                result.append(lst[i])
                i += 1
        return result
    my_actions, turn, coords=actions(coordinates, my_turn)
    my_actions=replace_elements(my_actions)
    return my_actions, turn, coords




# #print(coordinates)
# my_actions=actions(coordinates, 4)
# my_actions=replace_elements(my_actions)

# print(maze)