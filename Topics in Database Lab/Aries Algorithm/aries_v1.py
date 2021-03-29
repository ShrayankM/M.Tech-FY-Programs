import aries_ds as ds
import copy

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
                ds.LOG_MAIN[LSN] = log_record
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
                    ds.main_memory[pageId] = copy.deepcopy(page)
            
            if (operation == 'WRITE'):
                data_item = ins[ins.find('(') + 1:ins.find(',')]
                transactionId = ins[ins.find(' ') + 1:ins.find(')')]
                prevLSN = ds.active_transaction_table[transactionId].lastLSN
                pageId = ds.page_table[data_item]
                before = ds.main_memory[pageId].get_data_value(data_item)
                after = ds.temp_values[data_item]
                log_record = ds.LogRecord(LSN, prevLSN, transactionId, 'UPDATE', data_item, before, after, None)
                ds.active_transaction_table[transactionId].lastLSN = LSN
                ds.LOG_MAIN[LSN] = log_record
                ds.main_memory[pageId].data[data_item] = after
                ds.main_memory[pageId].pageLSN = LSN

                if ds.dirty_page_table.get(pageId):
                    LSN += 1
                else:
                    ds.dirty_page_table[pageId] = LSN
                    ds.main_memory[pageId].recLSN = LSN 
                    LSN += 1
            
            if (operation == 'COMMIT'):
                transactionId = ins[ins.find('(') + 1:ins.find(')')]
                prevLSN = ds.active_transaction_table[transactionId].lastLSN
                ds.active_transaction_table[transactionId].lastLSN = LSN
                log_record = ds.LogRecord(LSN, prevLSN, transactionId, 'COMMIT', '-', '-', '-', '-')
                ds.LOG_MAIN[LSN] = log_record

                for LSN, log_record in ds.LOG_MAIN.items():
                    ds.LOG_DISK[LSN] = log_record
                
                ds.LOG_MAIN.clear()
                ds.flushedLSN = LSN
                LSN += 1

                #* We can know start flushing pages to main disk
                page_ids = []
                for pageId, recLSN in ds.dirty_page_table.items():
                    if recLSN <= ds.flushedLSN:
                        data_items = ds.main_memory[pageId].data
                        ds.disk_memory[pageId].data = data_items
                        page_ids.append(pageId)
                
                for id in page_ids:
                    ds.dirty_page_table.pop(id)
                
                prevLSN = ds.active_transaction_table[transactionId].lastLSN
                log_record = ds.LogRecord(LSN, prevLSN, transactionId, 'END', '-', '-', '-', '-')
                ds.LOG_MAIN[LSN] = log_record
                LSN += 1

                #* Removing completed transactions from active_transaction_table
                ds.active_transaction_table.pop(transactionId)
 
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

    # return tabulate(data, headers = ["LSN", "prevLSN", "TxnId", "type", "data", "before", "after", "undoNext"])
    main_records = []
    print("  Log Records[On MAIN]")
    for LSN, logR in ds.LOG_MAIN.items():
        main_records.append(logR.get_record())
    print(ds.tabulate(main_records, headers = ["LSN", "prevLSN", "TxnId", "type", "data", "before", "after", "undoNext"]))

    print()
    disk_records = []
    print("  Log Records[On DISK]")
    for LSN, logR in ds.LOG_DISK.items():
        disk_records.append(logR.get_record())
    print(ds.tabulate(disk_records, headers = ["LSN", "prevLSN", "TxnId", "type", "data", "before", "after", "undoNext"]))

    print()
    print("  Main Memory")
    pages = []
    for pageId, page in ds.main_memory.items():
        pages.append(page.get_page())
    print(ds.tabulate(pages, ["pageId", "pageLSN", "recLSN", "data"]))

    print()
    print("  Disk Memory")
    pages = []
    for pageId, page in ds.disk_memory.items():
        pages.append(page.get_page())
    print(ds.tabulate(pages, ["pageId", "pageLSN", "recLSN", "data"]))

    print()
    print("  Dirty Page Table")
    dirty_pages = []
    for pageId, recLSN in ds.dirty_page_table.items():
        dirty_pages.append([pageId, recLSN])
    print(ds.tabulate(dirty_pages, headers = ["PageId", "recLSN"]))

    print()
    print("Active Transaction Table")
    transactions = []
    for transactionId, transaction in ds.active_transaction_table.items():
        transactions.append(transaction.get_active_transaction())
    print(ds.tabulate(transactions, headers = ["TransactionId", "status", "lastLSN"]))

    # print("FLUSHED_LSN ", ds.flushedLSN)

    # print(ds.temp_values)