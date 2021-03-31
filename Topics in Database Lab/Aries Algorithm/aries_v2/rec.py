import ds
import copy

def analysis_phase():
    for LSN, log in ds.LOG_DISK.items():

        #* Add the transaction in ATT with status UNDO
        if log.type == 'BEGIN':
            ds.ATT[log.TxnId] = ds.ActiveTransaction(log.TxnId, 'UNDO', log.LSN)
        
        #* Add the page in DPT if not present and set recLSN with current LSN
        if log.type == 'UPDATE':
            pageId = ds.page_mapping[log.dataItem]

            if not ds.DPT.get(pageId):
                ds.DPT[pageId] = log.LSN

            ds.MEMORY[pageId] = copy.deepcopy(ds.DISK_MEMORY[pageId])
            ds.ATT[log.TxnId].lastLSN = log.LSN
        
        # if log.type == 'COMMIT':
        #     ds.ATT[log.TxnId].status = 'COMMIT'
        #     ds.ATT[log.TxnId].lastLSN = log.LSN

        if log.type == 'COMMIT' or log.type == 'END':
            ds.ATT.pop(log.TxnId)


def redo_phase():
    LSN = 100

    #* Get Minimum LSN to start redo scanning
    for pageId, recLSN in ds.DPT.items():
        if LSN > recLSN: LSN = recLSN
    
    smallestLSN = LSN

    #* Redo all the update instructions
    while ds.LOG_DISK.get(LSN):
        log = ds.LOG_DISK[LSN]
        LSN += 1

        if log.type == 'UPDATE' or log.type == 'CLR':
            pageId = ds.page_mapping[log.dataItem]
            
            for pId, recLSN in ds.DPT.items():
                #* Checking for ignore conditions
                if pageId == pId or log.LSN > smallestLSN or ds.MEMORY[pId].pageLSN >= LSN:
                    continue
                else:
                    ds.MEMORY[pId].data[log.dataItem] = log.after
                    ds.MEMORY[pId].pageLSN = log.LSN

    transactions_to_remove = []
    for transactionId, transactionInfo in ds.ATT.items():
        if transactionInfo.status == 'COMMIT':
            transactions_to_remove.append(transactionId)
            prevLSN = ds.ATT[transactionId].lastLSN
            log = ds.LogRecord(LSN, prevLSN, transactionId, 'END', '-', '-', '-', '-')
            ds.LOG_MEMORY[LSN] = log
            LSN += 1
    
    for tid in transactions_to_remove:
        ds.ATT.pop(tid)

def undo_phase():
    currentLSN = 0

    for LSN in ds.LOG_DISK.keys():
        currentLSN = LSN
    
    transactions_to_remove = []
    for transactionId, transaction in ds.ATT.items():
        LSN = transaction.lastLSN

        while LSN != None:
            log = ds.LOG_DISK[LSN]
            if log.type == 'UPDATE':
                prevLSN = ds.ATT[transactionId].lastLSN
                ds.ATT[transactionId].lastLSN = currentLSN

                #* Adding CLR's for undo Updates
                clr_log = ds.LogRecord(currentLSN, prevLSN, transactionId, 'CLR', log.dataItem, log.after, log.before, log.prevLSN)
                ds.LOG_MEMORY[currentLSN] = clr_log

                #* Undoing the operations on pages
                pageId = ds.page_mapping[log.dataItem]
                ds.MEMORY[pageId].data[log.dataItem] = log.before
                ds.MEMORY[pageId].pageLSN = currentLSN

                currentLSN += 1
            LSN = log.prevLSN
        
        prevLSN = ds.ATT[transactionId].lastLSN
        log = ds.LogRecord(currentLSN, prevLSN, transactionId, 'ABORT', '-', '-', '-', '-')

        ds.LOG_MEMORY[currentLSN] = log

        #* Flushing all logs from MEMORY to DISK
        for LSN, log in ds.LOG_MEMORY.items():
            ds.LOG_DISK[LSN] = log
        ds.LOG_MEMORY.clear()
        
        ds.flushedLSN = currentLSN
        currentLSN += 1

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
        prevLSN = ds.ATT[transactionId].lastLSN
        log = ds.LogRecord(currentLSN, prevLSN, transactionId, 'END', '-', '-', '-', '-')
        ds.LOG_MEMORY[currentLSN] = log

        transactions_to_remove.append(transactionId)
        currentLSN += 1
    
    for tid in transactions_to_remove:
        ds.ATT.pop(tid)


def execute_recovery():
    #* Start the analysis Phase To create ATT and DPT
    analysis_phase()

    redo_phase()

    undo_phase()

    ds.view_system_state(0)