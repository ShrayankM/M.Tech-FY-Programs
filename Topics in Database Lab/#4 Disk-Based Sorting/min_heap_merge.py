import sys

# arrs = {
#     1: [5, 11, 23, 34, 56, 78, 80, 91, 101, 120],
#     2: [1, 8, 31, 55, 61, 66, 81, 92, 97, 111],
#     3: [7, 32, 57, 58, 62, 72, 89, 99, 100, 150],
# }

arrs = {
    1: [1, 3, 5, 6, 7],
    2: [2, 4, 7, 8, 10],
    3: [1, 4, 5, 6, 9],
}

inf = sys.maxsize

#* Main memory has space for 10 elements (7 for heap, 3 for sorted)

main_output = []
sorted_output = []

class data:
    def __init__(self, value, id):
        self.value = value
        self.id = id
    
    def __str__(self):
        return '[' + str(self.value) + ', ' + str(self.id) + ']\t' 

index_dict = dict()
def create_index_dict(k):
    for i in range(k):
        index_dict[i + 1] = 0;

class Heap:
    def __init__(self):
        self.heap = [data(-1, 0)]
    
    def fillHeap(self, k):
        for i in range(k):
            self.heap.append(data(arrs[i + 1][0], i + 1))
            self.heap.append(data(arrs[i + 1][1], i + 1))
            index_dict[i + 1] += 2
    
    def heapify(self, start_index, N):
        smallest = self.heap[start_index].value
        index = start_index
        L = 2 * start_index
        R = 2 * start_index + 1

        if (L <= N) and self.heap[L].value < smallest:
            index = L
            smallest = self.heap[L].value
        
        if (R <= N) and self.heap[R].value < smallest:
            index = R
            smallest = self.heap[R].value
        
        if (smallest != self.heap[start_index].value): 
            temp = self.heap[start_index]
            self.heap[start_index] = self.heap[index]
            self.heap[index] = temp
            self.heapify(index, N)

    def merging(self, N, A):
        counter = 0
        while (self.heap[1].value != inf):
            if counter < 3:
                sorted_output.append(self.heap[1].value)
                counter += 1
                id = self.heap[1].id

                if index_dict[id] >= A: #* Elements in individual Array
                    self.heap[1].value = inf
                    self.heapify(1, N)
                else:
                    self.heap[1].value = arrs[id][index_dict[id]]
                    index_dict[id] += 1

                    self.heapify(1, N)
            else:
                for i in range(counter):
                    main_output.append(sorted_output[i])
                sorted_output.clear()
                counter = 0
        for i in range(counter):
            main_output.append(sorted_output[i])
        sorted_output.clear()


if __name__ == '__main__':
    k = len(arrs)
    create_index_dict(k)
    h = Heap()

    h.fillHeap(k) 

    A = len(arrs[1])
    N = k * 2
    #* Initial Heap Creation
    start_index = int(N/2)

    while start_index > 0:
        h.heapify(start_index, N)
        # print(start_index)
        start_index -= 1
    # for i in range(len(h.heap)):
    #     print(h.heap[i])
    
    h.merging(N, A)
    
    print(index_dict)
    print(len(main_output))

    for i in range(len(h.heap)):
        print(h.heap[i])
    print(main_output)
    

