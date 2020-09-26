from room import Room
from player import Player
from world import World
from collections import deque

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

"""
-make a graph that holds the visited rooms with their exits
    and the room each exit connets to.
-Use a BFS to find all rooms so that we have the shortest paths
    the first "?" room marking the path we go
"""

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []
my_graph = {}

def move(direction):
    # cancel exception for the follow path function
    # so that it doesn't try to move when the path is
    # only listing the current room
    if direction == "c":
        return

    # get room id of this room and the one we are moving to
    currRoom = player.current_room.id
    nextRoom = player.current_room.get_room_in_direction(direction).id
    # replace the ? info for this room
    my_graph[currRoom][direction] = nextRoom
    # move to the next room
    player.travel(direction)
    # add movement to path
    traversal_path.append(direction)

    # add the next room to the graph if it is unexplored
    if nextRoom not in my_graph:
        add_curr_room_to_graph()

    # add the now privious room to the current room in the graph
    # to the direction opposite of the direction we just moved
    if direction == "n":
        my_graph[nextRoom]["s"] = currRoom
    elif direction == "s":
        my_graph[nextRoom]["n"] = currRoom
    elif direction == "e":
        my_graph[nextRoom]["w"] = currRoom
    elif direction == "w":
        my_graph[nextRoom]["e"] = currRoom


def add_curr_room_to_graph():
    # adds the new room to the graph making sure all exits are ?
    exits = {}
    for exit in player.current_room.get_exits():
        exits[exit] = "?"
    my_graph[player.current_room.id] = exits


def find_closest_new_room():
    # bredth first search to find the first empty room on the graph
    # returns a list of tuples that are the room id and the direction
    # needed to move to get to the listed room
    currRoom = player.current_room.id
    visited = set()
    queue = deque()
    queue.append([(currRoom,'c')])
    while len(queue) > 0:
        currPath = queue.popleft()
        currNode = currPath[-1][0]
        if currNode in visited:
            continue
        for key in list(my_graph[currNode].keys()):
            if my_graph[currNode][key] == "?":
                # returns the path as well as the direction of the first ? found
                return currPath, key

        visited.add(currNode)
        for key in list(my_graph[currNode].keys()):
            newPath = list(currPath)
            newPath.append((my_graph[currNode][key],key))
            queue.append(newPath)
    return None


def follow_path(path):
    if path == None:
        return None
    for direction in path[0]:
        move(direction[1])
    move(path[1])

def move_new_room():
    for key in list(my_graph[player.current_room.id].keys()):
        if my_graph[player.current_room.id][key] == "?":
            move(key)
            return True
    return None

# initial setup of the graph
add_curr_room_to_graph()
goal = len(room_graph)
while len(my_graph) < len(room_graph):
    keep_going = True
    # moves the player until there is no new room visible
    # to the player.
    while keep_going:
        keep_going = move_new_room()
    path = find_closest_new_room()
    follow_path(path)


### Testing ###

# print(find_closest_new_room())
# follow_path(find_closest_new_room())

# print(my_graph)
# print(f"Current Room: {player.current_room.id}")
###############


# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
