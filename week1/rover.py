
"""
This script defines an object-oriented model for a rover navigating a grid map. 
It includes three classes:

1. Position - Represents a position on the map with x, y coordinates and a traversable flag.
2. Map - Represents the 2D grid of Position objects.
3. Rover - Represents the rover with battery life and current position, capable of traversing the map.


"""

class Position:
    """
    A class to represent a position on the map.
    
    Attributes:
    -----------
    x : int
        X-coordinate of the position.
    y : int
        Y-coordinate of the position.
    traversable : bool
        Whether this position can be traversed by the rover.
    """
    def __init__(self, x, y, traversable=True):
        self.x = x
        self.y = y
        self.traversable = traversable

    def __repr__(self):
        return f"Position(x={self.x}, y={self.y}, traversable={self.traversable})"


class Map:
    """
    A class to represent the grid map of Position objects.
    
    Attributes:
    width : int
        Width of the map (number of columns).
    height : int
        Height of the map (number of rows).
    grid : list of lists of Position
        2D array of Position objects representing the map.
    """
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[Position(x, y, True) for x in range(width)] for y in range(height)]
    
    def set_traversable(self, x, y, traversable):
        """
        Sets the traversable property of the position at (x, y).
        """
        if 0 <= x < self.width and 0 <= y < self.height:
            self.grid[y][x].traversable = traversable


class Rover:
    """
    A class to represent the rover.
    
    Attributes:
    battery_life : float
        Current battery life in percentage.
    current_position : Position
        Current position of the rover.
    
    Methods:
    traverse_to(target_x, target_y, map_obj):
        Uses BFS algorithm to move the rover to the specified position if possible.
        Returns number of steps taken, or -1 if not reachable.
    """
    def __init__(self, start_position):
        self.battery_life = 100.0
        self.current_position = start_position
    
    def traverse_to(self, target_x, target_y, map_obj):
        from collections import deque

        visited = [[False for i in range(map_obj.width)] for j in range(map_obj.height)]
        queue = deque()

        queue.append((self.current_position.x, self.current_position.y, 0))  #appending the current position of the rover
        visited[self.current_position.y][self.current_position.x] = True

        # Possible moves: up, down, left, right (non-diagonal)
        moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        while queue:       #traversing till the queue gets empty
            x, y, steps = queue.popleft()

            

            if (x == target_x and y == target_y):
                # Update rover state
                self.battery_life -= steps
                self.current_position = map_obj.grid[y][x]

                if (self.battery_life>0):
                    return steps
                else:
                    return -1

            for dx, dy in moves:
                nx, ny = x + dx, y + dy 
                if (0 <= nx < map_obj.width and 0 <= ny < map_obj.height and not visited[ny][nx] and map_obj.grid[ny][nx].traversable):
                    
                    visited[ny][nx] = True
                    queue.append((nx, ny, steps + 1))

        return -1



if __name__ == "__main__":

    
    # Create a map
    my_map = Map(width=5, height=5)

    #adding obstructions in the map by making them not traversable. You nay add as much as you want to make the rover's path much more complex
    my_map.set_traversable(2, 0, False)
    my_map.set_traversable(2, 1, False)
    my_map.set_traversable(2, 2, False)
    my_map.set_traversable(2, 3, False)
    my_map.set_traversable(2, 4, False)
    
    # Initializing rover at (0, 0) (you may choose another point keeping in mind that it exists in the map)
    rover = Rover(start_position=my_map.grid[0][0])
    
    # Move rover to (4, 4)
    steps = rover.traverse_to(4, 1, my_map)
    
    print(f"Steps taken: {steps}")

