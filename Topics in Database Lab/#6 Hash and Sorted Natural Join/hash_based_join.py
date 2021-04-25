from tabulate import tabulate

#* Hash function return ascii value
def hash_function(h):
    return ord(str(h))

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

#* Build Phase
build_table = {}

for i in range(1, len(table_A)):
    h = hash_function(table_A[i][0])
    if build_table.get(h) == None:
        build_table[h] = list()
    t = [table_A[i][j] for j in range(0, len(table_A[i]))]
    build_table[h].append(t)


joined_table = list()
#* Natural Join Phase

for i in range(1, len(table_B)):
    h = hash_function(table_B[i][1])
    if build_table.get(h) == None:
        continue
    records_A = build_table[h]
    # t = [table_B[i][j] for j in range(0, len(table_B[i]))]
    t = table_B[i]
    for record in records_A:
        joined_table.append(list(record + t))

# for record in joined_table:
#     print(record)

headers = table_A[0] + table_B[0]
print(tabulate(joined_table, headers))