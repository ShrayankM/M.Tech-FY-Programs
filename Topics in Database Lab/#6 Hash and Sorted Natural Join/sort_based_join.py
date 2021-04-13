from tabulate import tabulate

def hash_function(h):
    return h % 10

def sort_for_B(L):
    return L[1]

def sort_for_A(L):
    return L[0]

table_A = [
    ['CustId', 'CustName'],
    [1, 'C1'],
    [2, 'C2'],
    [3, 'C3']
]

table_B = [
    ['InvoiceId', 'CustomerId', 'Total'],
    [1, 2, '$44.20'],
    [2, 2, '$13.37'],
    [3, 1, '$144.5'],
    [4, 3, '$501.1'],
    [5, 3, '$66.77'],
    [6, 1, '$100.0']
]

headers = table_A[0] + table_B[0]

#* Sorting tables A, B on customerId
table_B = sorted(table_B[1:], key=sort_for_B)
table_A = sorted(table_A[1:], key=sort_for_A)

joined_table = list()
#* Natural Join Phase
j = 0
for i in range(len(table_A)):
    while j < len(table_B):
        if table_A[i][0] == table_B[j][1]:
            joined_table.append(list(table_A[i] + table_B[j]))
            j = j + 1
        else:
            break

print(tabulate(joined_table, headers))