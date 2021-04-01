import ds
import rec
import copy

def get_value(ins, a, b):
    if (ins.find('+') > -1): return a + b
    if (ins.find('-') > -1): return a - b
    if (ins.find('*') > -1): return a * b
    if (ins.find('/') > -1): return a / b

def execute_instructions(instructions):
    LSN = 0
    for ins in instructions:

        #* Normal Operations
        if (ins.find('(') != -1):
            operation = ins[0:ins.find('(')]
            if (operation == 'CRASH'):
                ds.view_system_state(1)
                ds.LOG_MEMORY.clear()
                ds.DPT.clear()
                ds.ATT.clear()
                ds.MEMORY.clear()
                rec.execute_recovery()
            
            if (operation == "BEGIN"):
                transactionId = ins[ins.find('(') + 1:ins.find(')')]
                log = ds.LogRecord(LSN, None, transactionId, 'BEGIN', '-', '-', '-', '-')
                ds.LOG_MEMORY[LSN] = log
                ds.ATT[transactionId] = ds.ActiveTransaction(transactionId, 'UNDO', LSN)
                LSN += 1
            
            if (operation == 'READ'):
                data_variable = ins[ins.find('(') + 1:ins.find(',')]
                transactionId = ins[ins.find(' ') + 1:ins.find(')')]

                pageId = ds.page_mapping[data_variable]
                if ds.MEMORY.get(pageId):                              #* Page already present in MEMORY
                    continue
                else:
                    ds.MEMORY[pageId] = copy.deepcopy(ds.DISK_MEMORY[pageId])
            
            if (operation == 'WRITE'):
                data_variable = ins[ins.find('(') + 1:ins.find(',')]
                transactionId = ins[ins.find(' ') + 1:ins.find(')')]

                prevLSN = ds.ATT[transactionId].lastLSN
                ds.ATT[transactionId].lastLSN = LSN

                pageId = ds.page_mapping[data_variable]
                before = ds.MEMORY[pageId].data.get(data_variable)
                after = ds.temp_buffer[data_variable]

                #* Writing Update Log record to MEMORY
                log = ds.LogRecord(LSN, prevLSN, transactionId, 'UPDATE', data_variable, before, after, '-')
                ds.LOG_MEMORY[LSN] = log
                
                #* Updating the pages in MEMORY
                ds.MEMORY[pageId].data[data_variable] = after
                ds.MEMORY[pageId].pageLSN = LSN

                if ds.MEMORY[pageId].recLSN == None:
                    ds.MEMORY[pageId].recLSN = LSN
                
                #* Adding pages to dirty page table (DPT)
                if ds.DPT.get(pageId) == None:
                    ds.DPT[pageId] = LSN

                LSN += 1

            if (operation == 'COMMIT'):
                transactionId = ins[ins.find('(') + 1:ins.find(')')]

                # print('COMMITING TRANSACTION ' + str(transactionId))

                ds.ATT[transactionId].status = 'COMMIT'

                prevLSN = ds.ATT[transactionId].lastLSN
                ds.ATT[transactionId].lastLSN = LSN

                #* Writing COMMIT Log record to MEMORY
                log = ds.LogRecord(LSN, prevLSN, transactionId, 'COMMIT', '-', '-', '-', '-')
                ds.LOG_MEMORY[LSN] = log

                #* Flushing all logs from MEMORY to DISK
                for LSN, log in ds.LOG_MEMORY.items():
                    ds.LOG_DISK[LSN] = log
                ds.LOG_MEMORY.clear()

                ds.flushedLSN = LSN
                LSN += 1

                # print(ds.flushedLSN)

                #* Flushing pages from MEMORY TO DISK
                pages_to_remove = []
                for pageId, recLSN in ds.DPT.items():
                    if recLSN <= ds.flushedLSN:
                        ds.DISK_MEMORY[pageId] = copy.deepcopy(ds.MEMORY[pageId])
                        ds.MEMORY[pageId].pageLSN = None
                        ds.MEMORY[pageId].recLSN = None
                        pages_to_remove.append(pageId)
                
                #* Clearing out flushed pages from DPT
                for id in pages_to_remove:
                    ds.DPT.pop(id)
                
                #* Writing the TXN-END log record
                # prevLSN = ds.ATT[transactionId].lastLSN
                # log = ds.LogRecord(LSN, prevLSN, transactionId, 'END', '-', '-', '-', '-')
                # ds.LOG_MEMORY[LSN] = log

                # ds.ATT.pop(transactionId)

                # LSN += 1

            if (operation == 'ABORT'):
                transactionId = ins[ins.find('(') + 1:ins.find(')')]

                ds.ATT[transactionId].status = 'ABORT'

                prevLSN = ds.ATT[transactionId].lastLSN
                ds.ATT[transactionId].lastLSN = LSN

                #* Writing ABORT Log record to MEMORY
                log = ds.LogRecord(LSN, prevLSN, transactionId, 'ABORT', '-', '-', '-', '-')
                ds.LOG_MEMORY[LSN] = log

                LSN += 1

                prev = prevLSN
                while prev != None:
                    log = ds.LOG_MEMORY[prev]
                    if log.type == 'UPDATE':
                        prevLSN = ds.ATT[transactionId].lastLSN
                        ds.ATT[transactionId].lastLSN = LSN
                        clr_log = ds.LogRecord(LSN, prevLSN, transactionId, 'CLR', log.dataItem, log.after, log.before, log.prevLSN)
                        ds.LOG_MEMORY[LSN] = clr_log

                        pageId = ds.page_mapping[log.dataItem]
                        #* Updating the pages in MEMORY
                        ds.MEMORY[pageId].data[log.dataItem] = log.before
                        ds.MEMORY[pageId].pageLSN = LSN
                        LSN += 1
                    prev = log.prevLSN
                
                #* Flushing all logs from MEMORY to DISK
                for LSN, log in ds.LOG_MEMORY.items():
                    ds.LOG_DISK[LSN] = log
                ds.LOG_MEMORY.clear()

                ds.flushedLSN = LSN

                #* Flushing pages from MEMORY TO DISK
                pages_to_remove = []
                for pageId, recLSN in ds.DPT.items():
                    if recLSN <= ds.flushedLSN:
                        ds.DISK_MEMORY[pageId] = copy.deepcopy(ds.MEMORY[pageId])
                        pages_to_remove.append(pageId)
                
                #* Clearing out flushed pages from DPT
                for id in pages_to_remove:
                    ds.DPT.pop(id)
                
                #* Writing the TXN-END log record
                # prevLSN = ds.ATT[transactionId].lastLSN
                # log = ds.LogRecord(LSN, prevLSN, transactionId, 'END', '-', '-', '-', '-')
                # ds.LOG_MEMORY[LSN] = log

                # ds.ATT.pop(transactionId)
                # LSN += 1

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

            pageId = ds.page_mapping[a]
            a = ds.MEMORY[pageId].data.get(a)
            updated_value = get_value(ins, a, b)
            ds.temp_buffer[updating_data] = updated_value


if __name__ == '__main__':
    schedule = open('schedule_input.txt', 'r')
    data = []

    for instruction in schedule:
        data.append(instruction.strip())

    #* Getting all instructions in the schedule
    instructions = data[0:]

    execute_instructions(instructions)

