import math
from typing import Optional
from Map import Map_Obj





# Priority Queue, inspired by https://www.geeksforgeeks.org/priority-queue-in-python/
# Priority Queue is used to store the next positions to be visited, sorted by the cost to get to the position
class PriorityQueue():
    def __init__(self):
        self.queue: list[tuple(float, [int, int])] = []  # list of tuples, where the first element is the priority and the second element is the item

    def __str__(self):
        return ' '.join([str(i) for i in self.queue])
    
    def insert(self, priority: float, item: tuple([int, int])):
        self.queue.append((priority, item)) # append tuple to queue
    
    def isEmpty(self):
        return len(self.queue) == 0 # return True if queue is empty
    
    def delete(self):
        if self.isEmpty():
            return None # return None if queue is empty
        
        try:
            max_val_index = 0 # index of item with highest priority
            for i in range(len(self.queue)): 
                if self.queue[i][0] < self.queue[max_val_index][0]:
                    max_val_index = i # update index of item with highest priority
            max_val_item = self.queue[max_val_index]
            del self.queue[max_val_index] # delete item with highest priority
            return max_val_item[1] # return item with highest priority
        except IndexError: # if index is out of range
            print()
            exit()

# Heuristic function, finding the euclidean distance between two positions
def heuristic_euclidean(pos: tuple([int, int]), end_pos: tuple([int, int])) -> float:
    return math.sqrt((pos[0] - end_pos[0])**2 + (pos[1] - end_pos[1])**2)


# A* Search Algorithm, inspired by https://www.redblobgames.com/pathfinding/a-star/implementation.html
def a_star_search(map: Map_Obj, start: tuple([int, int]), end: tuple([int, int])):
    queue = PriorityQueue() 
    queue.insert(0, start)
    came_from: dict[tuple([int, int]), Optional(tuple([int, int]))] = {} # key: position, value: previous position
    cost_so_far: dict[tuple([int, int]), float] = {} # key: position, value: cost to get to position
    came_from[start] = None
    cost_so_far[start] = 0
    
    while not queue.isEmpty():
        current: tuple([int, int]) = queue.delete()

        if current == end:
            break

        for next_pos in map.get_neighbours(current):
            new_cost = cost_so_far[current] + map.get_cell_value(next_pos)
            if next_pos not in cost_so_far or new_cost < cost_so_far[next_pos]:
                cost_so_far[next_pos] = new_cost
                priority = new_cost + heuristic_euclidean(next_pos, end)
                queue.insert(priority, next_pos)
                came_from[next_pos] = current

    # Mark path on map
    while current != start:
        current = came_from[current]
        if(current != start and current != end):
            map.set_cell_value(current, ' P ') # P for path, marking the path green
    return came_from, cost_so_far




if __name__ == '__main__':
    # Task 1
    mapTask1 = Map_Obj(task=1)
    came_from, cost_so_far = a_star_search(mapTask1, mapTask1.get_start_pos(), mapTask1.get_end_goal_pos())
    mapTask1.show_map()

    # Task 2
    mapTask2 = Map_Obj(task=2)
    came_from, cost_so_far = a_star_search(mapTask2, mapTask2.get_start_pos(), mapTask2.get_end_goal_pos())
    mapTask2.show_map()

    # Task 3
    mapTask3 = Map_Obj(task=3)
    came_from, cost_so_far = a_star_search(mapTask3, mapTask3.get_start_pos(), mapTask3.get_end_goal_pos())
    mapTask3.show_map()

    # Task 4
    mapTask4 = Map_Obj(task=4)
    came_from, cost_so_far = a_star_search(mapTask4, mapTask4.get_start_pos(), mapTask4.get_end_goal_pos())
    mapTask4.show_map()
