import helper as h

def simple_backtracking(graph, assigned):

    return_ans = True
    assign = False

    #* Check if all colors are assigned
    for i in range(0, h.NODES):
        if assigned[i] == -1:
            return_ans = False
            break

    if return_ans: return assigned

    #* Getting the best node possible
    node = h.select_node(graph, assigned)

    print("Selected Node = " + str(node))

    for color in range(0, h.COLORS):
        color_value = color
        if color_value == -1:
            return
        
        if h.check_consistency(graph, node, color_value, assigned):
            assigned[node] = color_value
            assign = True
            print("COLOR given to Node " + str(node) + " is " + str(color_value))

            result = simple_backtracking(graph, assigned)
            if (len(result) != 1):
                return result
        if assign: assigned[node] = -1
    return