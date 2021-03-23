import numpy as np
import math
import sys

inf = sys.maxsize
np.random.seed(2)

T = 300
main_disk_data = np.random.randint(1, 300, 300)

#* Main memory can hold atmost 20 elements
M = 60
main_memory = list()

#* Individual sorted files
files = dict()

#TODO Phase I
#********************** QUICKSORT ALGORITHM **************************#
def swap(A, i, j):
    temp = A[i]
    A[i] = A[j]
    A[j] = temp

def partition(A, L, H):
    pivot = A[L]
    i = L
    j = L + 1

    while j <= H:
        if A[j] <= pivot:
            i = i + 1
            swap(A, i, j)
        j = j + 1
    swap(A, L, i)
    return i

def quicksort(A, L, H):
    if L < H:
        pivotPos = partition(A, L, H)
        quicksort(A, L, pivotPos - 1)
        quicksort(A, pivotPos + 1, H)

def sorting(arr):
    N = len(arr)
    quicksort(arr, 0, N - 1)
    return arr

#*********************** Creating Sorted Chunks ***********************#
def make_sorted_files():
    file_counter = 1
    read_main_disk(files, file_counter)

def read_main_disk(files, file_counter):
    j = 0
    while j < len(main_disk_data):
        main_memory = main_disk_data[j:j + M]
        main_memory = sorting(main_memory)
        files[file_counter] = list(main_memory)
        file_counter += 1
        j = j + M

#TODO Phase II
#********************* Data Structures For Merging ********************#
#* Sorted Output on the disk 
main_output = []

S = 15
sorted_output = []

class data:
    def __init__(self, value, id):
        self.value = value
        self.id = id
    
    def __str__(self):
        return '[' + str(self.value) + ', ' + str(self.id) + ']\t'

#* Heap takes space of 7 elements, so sorted_output gets space for 3 elements
class Heap:
    def __init__(self):
        self.heap = [data(-1, 0)]
    
    def fillHeap(self, F, k):
        for i in range(F):
            for j in range(k):
                self.heap.append(data(files[i + 1][j], i + 1))
            index_dict[i + 1] += k
    
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
            if counter < S:
                sorted_output.append(self.heap[1].value)
                counter += 1
                id = self.heap[1].id

                if index_dict[id] >= A: #* Elements in individual Array
                    self.heap[1].value = inf
                    self.heapify(1, N)
                else:
                    self.heap[1].value = files[id][index_dict[id]]
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

#************************** Helper Functions and DS *********************#
#TODO Keep track on indexing of the files
index_dict = dict()
def create_index_dict(k):
    for i in range(k):
        index_dict[i + 1] = 0;
    
if __name__ == '__main__':
    make_sorted_files()
    F = int(T/M)
    H = M - S

    k = int(math.floor(H/F))
    heap_size = int(k * F)

    create_index_dict(F)
    h = Heap()

    h.fillHeap(F, k) 

    #* Initial Heap Creation
    start_index = int(heap_size/2)

    while start_index > 0:
        h.heapify(start_index, heap_size)
        start_index -= 1
    
    h.merging(heap_size, M)
    print(main_output)

    print(len(main_output))
    
