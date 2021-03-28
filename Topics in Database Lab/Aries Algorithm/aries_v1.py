import aries_ds as ds

def get_value(ins, a, b):
    if (ins.find('+') > -1): return a + b
    if (ins.find('-') > -1): return a - b
    if (ins.find('*') > -1): return a * b
    if (ins.find('/') > -1): return a / b

def execute_instructions():
    LSN = 0
    file = open('schedule_input.txt', 'r')
    data = []

    for line in file:
        data.append(line.strip())
    instrus_count = int(data[0])
    instructions = data[1:]

    for i in range(instrus_count):
        ins = instructions[i]  

        #* Normal Operations
        if (ins.find('(') != -1):
            operation = ins[0:ins.find('(')]
            if (operation == "BEGIN"):
                transactionId = ins[ins.find('(') + 1:ins.find(')')] 

                log_record = ds.LogRecord(LSN, None, transactionId, 'BEGIN', '-', 0, 0, None)
                ds.LOG_DISK[LSN] = log_record
                tRecord = ds.ActiveTransaction(transactionId, 'UNDO', LSN)
                ds.active_transaction_table[transactionId] = tRecord
                LSN += 1
            
            if (operation == 'READ'):
                data_item = ins[ins.find('(') + 1:ins.find(',')]
                transactionId = ins[ins.find(' ') + 1:ins.find(')')]

                #* Search data items page in main_memory, if found great else look in disk
                pageId = ds.page_table[data_item]
                if ds.main_memory.get(pageId): continue
                else: 
                    page = ds.disk_memory.get(pageId)
                    ds.main_memory[pageId] = page
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

            b = int(b)

            #* Check if a is modified and present in ds.temp_values
            if ds.temp_values.get(a): 
                a = ds.temp_values[a]
            else:                     
                pageId = ds.page_table[a]
                a = ds.main_memory[pageId].get_data_value(a)
            
            updated_value = get_value(ins, a, b)
            ds.temp_values[updating_data] = updated_value


if __name__ == '__main__':
    execute_instructions()


    # print("Log Records")
    # for LSN, logR in ds.LOG_DISK.items():
    #     print(logR)
    
    # # print("\n")
    # print("Active Transaction Table")
    # for tId, trans in ds.active_transaction_table.items():
    #     print(trans)
    
    # print("Main Memory")
    # for pageId, page in ds.main_memory.items():
    #     print(page)