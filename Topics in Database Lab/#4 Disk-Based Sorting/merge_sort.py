import numpy as np

np.random.seed(2)
main_disk_data = np.random.randint(1, 100, 200)

# print(main_disk_data)

#* Main memory can hold atmost 10 elements
main_memory = list()

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

i = 1
arrs = dict()

j = 0
while j < len(main_disk_data):
    main_memory = main_disk_data[j:j + 10]
    main_memory = sorting(main_memory)
    arrs[i] = main_memory
    i = i + 1
    j = j + 10

for key, value in arrs.items():
    print(key, len(value))
