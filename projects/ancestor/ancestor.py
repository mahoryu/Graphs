from collections import deque

def createGraph(paths):
    # create a graph with the child as key and parents as the edge cases
    graph = {}
    for edge in paths:
        child, parent = edge[1], edge[0]
        if child in graph:
            graph[child].append(parent)
        else:
            graph[child] = [parent]
    return graph

def earliest_ancestor(ancestors, starting_node):
    """
    Graph Terminology
    vertex - person ID
    edge - parent child relationship
    path - child to ancestor
    need to find longest path and return that vertex

    Build graph:
    - take the list of ancestors and add the parent child pairs into the
        dictonary
    - make the direction going backwards for easy traversal (i.e. child
        points to parents)

    Traverse the graph
    - need to check the starting node and find the longest path
    - any input node with no parents should return -1
    """

    # Add ancestor pairs to dict
    ancestry = createGraph(ancestors)

    #return -1 if the starting node doesn't have any parents
    if starting_node not in ancestry:
        return -1

    # find the earliest ancestor
    queue = deque()
    queue.append(starting_node)
    visited = set()


    while len(queue) > 0:
        currNode = queue.popleft()
        # skip if already visited
        if currNode in visited:
            continue
        # end statement to return the furthest ancestor (queue will be emnpty if it is last)
        if currNode not in ancestry and len(queue) == 0:
            return currNode
        # has no ancestors but isn't the furthest
        if currNode not in ancestry:
            continue
        # the node has two parents only add parents if they have at least one parent
        if len(ancestry[currNode]) > 1:
            # marker to toggle depending on if both parents are tied for furthest
            end = True
            visited.add(currNode)
            for neighbor in ancestry[currNode]:
                if neighbor in ancestry:
                    queue.append(neighbor)
                    end = False
            # if they are tied, return the lesser valued one
            if end:
                if ancestry[currNode][0] < ancestry[currNode][1]:
                    return ancestry[currNode][0]
                else:
                    return ancestry[currNode][1]
        # normal traversal if there are no special conditions
        else:
            visited.add(currNode)
            for neighbor in ancestry[currNode]:
                queue.append(neighbor)



if __name__ == '__main__':

    test_ancestors = [(1, 3), (2, 3), (3, 6), (5, 6), (5, 7), (4, 5), (4, 8), (8, 9), (11, 8), (10, 1)]
    test = earliest_ancestor(test_ancestors, 10)
    print(test)

