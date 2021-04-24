from tabulate import tabulate

def sort_for_B(L):
    return L[1]

def sort_for_A(L):
    return L[0]

table_A = [
    ['CustomerId', 'CustomerName'],
    [1, 'C1'],
    [2, 'C2'],
    [3, 'C3'],
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
primary_key_A = True
primary_key_B = False

#* Natural Join Phase
#* Gives Correct Output if the common attribute in table_A is primary key

if primary_key_A:
    j = 0
    for i in range(len(table_A)):
        while j < len(table_B):
            if table_A[i][0] == table_B[j][1]:
                joined_table.append(list(table_A[i] + table_B[j]))
                j = j + 1
            else:
                break
else:
    #* Grouping A
    groups_A = dict()
    a = 0
    while a < len(table_A):
        value = table_A[a][0]
        groups_A[value] = list()
        groups_A[value].append(table_A[a])

        k = a + 1
        while k < len(table_A) and value == table_A[k][0]:
            groups_A[value].append(table_A[k])
            k = k + 1
        a = k
    
    #* Mapping table_B to groups in A (Cross product among groups)
    for i in range(0, len(table_B)):
        value = table_B[i][1]
        records_A = groups_A[value]
        
        for r in records_A:
            joined_table.append(list(r + table_B[i]))


print(tabulate(joined_table, headers))