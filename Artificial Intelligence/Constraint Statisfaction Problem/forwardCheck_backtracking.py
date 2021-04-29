import helper as h

def forwardCheck_backtracking(graph, assigned):
    return_ans = True
    assign = False
    ans = list()
    temp = list()
    forward = False

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
        color_value = h.select_color(graph, node, color, assigned)

        if color_value == -1:
            ans.append(-1)
            return ans
        
        if h.check_consistency(graph, node, color_value, assigned):
            assigned[node] = color_value

            print("COLOR given to Node " + str(node) + " is " + str(color_value))
            assign = True

            for i in range(0, h.NODES):
                    temp.append(h.color_matrix[i][color_value])

            inference = h.check_forward(graph, node, color_value)
            if (inference):
                forward = True
                h.add_forward(graph, node, color_value)
                result = forwardCheck_backtracking(graph, assigned)

                if (len(result) != 1):
                    return result
        if assign: assigned[node] = -1
        if forward: h.revert_forward(color_value, temp)
    ans.append(-1)
    return ans