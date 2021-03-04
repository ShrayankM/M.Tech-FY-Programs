from tabulate import tabulate

#* GLOBAL VARIABLES
transactions_dict = {}
temp_values = {}
main_disk = {
    'A': 100,
    'B': 200,
    'C': 500,
    'D': 300,
    'E': 50,
    'F': -100,
}
cache_disk = {}
class transaction_data:
    def __init__(self, transaction_id):
        self.transaction_id = transaction_id
        self.data_items = list()
    
def get_value(ins, a, b):
    if (ins.find('+') > -1): return a + b
    if (ins.find('-') > -1): return a - b
    if (ins.find('*') > -1): return a * b
    if (ins.find('/') > -1): return a / b

def create_log(instrus_cnt, instructions):
    log_file = open("log.txt", "w")
    for i in range(instrus_cnt):
        ins = instructions[i]

        #* Normal Operations
        if (ins.find('(') != -1):
            operation = ins[0:ins.find('(')]
            if (operation == "BEGIN"):
                transaction = ins[ins.find('(') + 1:ins.find(')')]
                log_file.write(f"<START {transaction}>\n")
                transactions_dict[transaction] = transaction_data(transaction)

            if (operation == 'READ'):
                data_item = ins[ins.find('(') + 1:ins.find(',')]
                transaction = ins[ins.find(' ') + 1:ins.find(')')]
                log_file.write(f"<{transaction} READ {data_item}>\n")
                temp_values[data_item] = cache_disk[data_item]
            
            if (operation == 'WRITE'):
                data_item = ins[ins.find('(') + 1:ins.find(',')]
                transaction = ins[ins.find(' ') + 1:ins.find(')')]
                log_file.write(f"<{transaction} WRITE {data_item}>\n")
                cache_disk[data_item] = temp_values[data_item]
                transactions_dict[transaction].data_items.append(data_item)
            
            if (operation == 'COMMIT'):
                transaction = ins[ins.find('(') + 1:ins.find(')')]
                log_file.write(f"<COMMIT {transaction}>\n")
                data_list = transactions_dict[transaction].data_items

                for d in data_list:
                    main_disk[d] = cache_disk[d]

        #* Arithematic Operations
        else: 
            updating_data = ins[0]
            a = ins[ins.find('[') + 1]

            #* Code to Refactor
            b = ''
            index = ins.find(']') - 1
            while (ins[index] != ' '):
                b += ins[index]
                index -= 1
            b = b[::-1]

            try:
                temp_b = int(b)
                b = temp_b
                a = cache_disk[a]
            except:
                #* GET BOTH a and b FROM MAIN DISK
                a = cache_disk[a]
                b = cache_disk[b]
            current_value = cache_disk[updating_data]
            updated_value = get_value(ins, a, b)
            log_file.write(f"<{ins[ins.find('_') + 1:]} {updating_data} {current_value} {updated_value}>\n")
            temp_values[updating_data] = updated_value
            continue  

def simulate_crash(log_file):
    started_transactions = set()
    commited_transactions = set()
    uncommited_transactions = set()
    temp_values = {}

    #* Get all started transactions
    file = open(log_file, "r")
    for line in file:
        if line.find('START') == 1:
            started_transactions.add(line[line.find(' ') + 1:line.find('>')])
    file.close()
    
    #* Get all commited transactions
    file = open(log_file, "r")
    for line in file:
        if line.find('COMMIT') == 1:
            commited_transactions.add(line[line.find(' ') + 1:line.find('>')])
    file.close()

    # uncommited_transactions = started_transactions - commited_transactions

    #TODO For all Commited Transactions (Redo)
    #TODO For all Uncommited Transactions (Undo)

    file = open(log_file, "r")
    for line in file:
        if (line.find('START') == 1 or line.find('COMMIT') == 1): 
            continue
        line = line.replace('>', '').replace('<', '').replace('\n', '').split(' ')
        
        if len(line) == 3: #* READ/WRITE OPERATION
            if line[1] == 'READ': 
                continue

            transaction_id, _, data_item = line[0:]
            # print(temp_values)
            data_list = temp_values[transaction_id]

            for data in data_list:
                if (data[0] == data_item):
                    main_disk[data_item] = data[1]


        if len(line) == 4:
            transaction_id, data_item, old_value, new_value = line[0:]
            flag = False
            for t in commited_transactions:   
                if t == transaction_id:
                    flag = True
                    break
            
            if temp_values.get(transaction_id) == None:
                temp_values[transaction_id] = list()
            
            if flag:
                temp_values[transaction_id].append([data_item, new_value])
            else:
                temp_values[transaction_id].append([data_item, old_value])

                 

def load_data_to_cache(main_disk, cache_disk):
    for key, value in main_disk.items():
        cache_disk[key] = value

def read_transaction_file(filename):
    file = open(filename, "r")
    data = []

    for line in file:
        data.append(line.strip())

    instrus_cnt = int(data[0])
    instructions = data[1:]
    return instrus_cnt, instructions

if __name__ == "__main__":
    filename = "transaction_input.txt"
    instrus_cnt, instructions = read_transaction_file(filename)

    load_data_to_cache(main_disk, cache_disk)
    create_log(instrus_cnt, instructions)

    # print("========== BEFORE CRASH ========== ")
    # print(f"CACHE_DISK = {cache_disk}")
    # print(f"DATABASE = {main_disk}\n")

    # log_filename = "log.txt"
    # simulate_crash(log_filename)

    # print("========== AFTER CRASH ========== ")
    # print(f"DATABASE = {main_disk}\n")

    cnt = 1
    data = []

    data_items = list(cache_disk.keys())
    cache_values = list(cache_disk.values())
    disk_bc = list(main_disk.values())

    log_filename = "log.txt"
    simulate_crash(log_filename)

    disk_ac = list(main_disk.values())

    while cnt <= len(data_items):
        data.append([cnt, data_items[cnt - 1], cache_values[cnt - 1], disk_bc[cnt - 1], disk_ac[cnt - 1]])
        cnt += 1
    
    # print(data)
    print (tabulate(data, headers=["No.", "Data Item", "Cache", "Disk[Before Crash]", "Disk[After Crash]"]))
