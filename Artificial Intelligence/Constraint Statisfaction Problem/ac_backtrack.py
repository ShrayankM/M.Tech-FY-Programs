import helper as h

def backtrack(graph, assigned):
    return_ans = True
    assign = False
    add_infer = False
    ans = list()
    temp = list()

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

        print("Color Selected = " + str(color_value))

        if color_value == -1:
            ans.append(-1)
            return ans
        
        if h.check_consistency(graph, node, color_value, assigned):
            assigned[node] = color_value

            print("COLOR given to Node " + str(node) + " is " + str(color_value))
            assign = True

            inference = h.AC3(graph, assigned, node)

            if inference:
                for i in range(0, h.NODES):
                    temp.append(h.color_matrix[i])
            add_infer = True
            result = backtrack(graph, assigned)

            if (len(result) != 1):
                return result
        if assign: assigned[node] = -1
        if add_infer: h.revert_inference_ac3(temp)
    ans.append(-1)
    return ans

