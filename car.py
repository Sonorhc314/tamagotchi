import agent

class Car:
    def __init__(self):
        self.coordinates = (3,3)
        self.maze = [
            ['0','0','S','R','0'],
            ['M','1','1','1','0'],
            ['0','1','0','0','0'],
            ['0','1','1','1','0'],
            ['0','0','0','0','0']]
        self.turn = 4
    def get_goal(self, goal):
        for i in range(len(self.maze)):
            if goal in self.maze[i]:
                x = i
                y = self.maze[i].index(goal)
        return x, y
    def get_turn(self):
        return self.turn
    def get_coordinates(self):
        return self.coordinates
    def get_maze(self):
        return self.maze
    def set_maze(self, maze):
        self.maze = maze
        return self.maze
    def set_turn(self, turn):
        self.turn = turn
    def set_coordinates(self, coordinates):
        self.coordinates = coordinates
    def get_actions(self, goal):
        goal = self.get_goal(goal)
        dop_maze = [row[:] for row in self.maze]
        actions, self.turn, self.coordinates = agent.run_path(dop_maze, self.coordinates, goal, self.turn)
        actions.append('S')
        actions = [x.lower() for x in actions]
        return(actions)
