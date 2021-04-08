import ds
import copy

def analysis_phase():
    lsn = ds.masterRecord[0]
    ds.ATT = copy.deepcopy(ds.masterRecord[1].ATT)
    ds.DPT = copy.deepcopy(ds.masterRecord[1].DPT)

    while ds.LOG_DISK.get(lsn):
        log = ds.LOG_DISK[lsn]

        #* Add the transaction in ATT with status UNDO
        if log.type == 'BEGIN':
            ds.ATT[log.TxnId] = ds.ActiveTransaction(log.TxnId, 'UNDO', log.LSN)
        
        #* Add the page in DPT if not present and set recLSN with current LSN
        if log.type == 'UPDATE':
            pageId = ds.page_mapping[log.dataItem]

            if not ds.DPT.get(pageId):
                ds.DPT[pageId] = log.LSN

            ds.ATT[log.TxnId].lastLSN = log.LSN
        
        if log.type == 'COMMIT':
            ds.ATT[log.TxnId].status = 'COMMIT'
            ds.ATT[log.TxnId].lastLSN = log.LSN
        
        if log.type == 'ABORT':
            ds.ATT[log.TxnId].status = 'ABORT'
            ds.ATT[log.TxnId].lastLSN = log.LSN

        if log.type == 'END':
            ds.ATT.pop(log.TxnId)
        lsn += 1

def redo_phase():
    LSN = 100

    #* Get Minimum LSN to start redo scanning
    for pageId, recLSN in ds.DPT.items():
        if LSN > recLSN: LSN = recLSN
    

    #* Redo all the update instructions
    while ds.LOG_DISK.get(LSN):
        log = ds.LOG_DISK[LSN]
        LSN += 1

        if log.type == 'UPDATE' or log.type == 'CLR':
            pageId = ds.page_mapping[log.dataItem]

            if not ds.DPT.get(pageId) or ds.DPT[pageId] > log.LSN:
                continue
            
            if not ds.MEMORY.get(pageId): 
                ds.MEMORY[pageId] = copy.deepcopy(ds.DISK_MEMORY[pageId])

            if ds.MEMORY[pageId].pageLSN != None and ds.MEMORY[pageId].pageLSN >= log.LSN:
                continue
            else:
                if ds.MEMORY[pageId].recLSN == None:
                    ds.MEMORY[pageId].recLSN = log.LSN
                ds.MEMORY[pageId].data[log.dataItem] = log.after
                ds.MEMORY[pageId].pageLSN = log.LSN

    transactions_to_remove = []
    for transactionId, transactionInfo in ds.ATT.items():
        if transactionInfo.status == 'COMMIT' or transactionInfo.status == 'ABORT':
            transactions_to_remove.append(transactionId)
            prevLSN = ds.ATT[transactionId].lastLSN
            log = ds.LogRecord(ds.LSN, prevLSN, transactionId, 'END', '-', '-', '-', '-')
            ds.LOG_MEMORY[ds.LSN] = log
            ds.LSN += 1
    
    for tid in transactions_to_remove:
        ds.ATT.pop(tid)


def undo_phase():
    
    transactions_to_remove = []
    for transactionId, transaction in ds.ATT.items():
        LSN = transaction.lastLSN

        while LSN != None:
            log = ds.LOG_DISK[LSN]
            if log.type == 'UPDATE':
                prevLSN = ds.ATT[transactionId].lastLSN
                ds.ATT[transactionId].lastLSN = ds.LSN

                #* Adding CLR's for undo Updates
                clr_log = ds.LogRecord(ds.LSN, prevLSN, transactionId, 'CLR', log.dataItem, log.after, log.before, log.prevLSN)
                ds.LOG_MEMORY[ds.LSN] = clr_log

                #* Undoing the operations on pages
                pageId = ds.page_mapping[log.dataItem]
                ds.MEMORY[pageId].data[log.dataItem] = log.before
                ds.MEMORY[pageId].pageLSN = ds.LSN

                ds.LSN += 1
            LSN = log.prevLSN
        
        prevLSN = ds.ATT[transactionId].lastLSN
        ds.ATT[transactionId].lastLSN = ds.LSN
        log = ds.LogRecord(ds.LSN, prevLSN, transactionId, 'ABORT', '-', '-', '-', '-')

        ds.LOG_MEMORY[ds.LSN] = log

        #* Flushing all logs from MEMORY to DISK
        for LSN, log in ds.LOG_MEMORY.items():
            ds.LOG_DISK[LSN] = log
        ds.LOG_MEMORY.clear()
        
        ds.flushedLSN = ds.LSN
        ds.LSN += 1
        
        #* Writing the TXN-END log record
        prevLSN = ds.ATT[transactionId].lastLSN
        log = ds.LogRecord(ds.LSN, prevLSN, transactionId, 'END', '-', '-', '-', '-')
        ds.LOG_MEMORY[ds.LSN] = log

        transactions_to_remove.append(transactionId)
        ds.LSN += 1
    
    for tid in transactions_to_remove:
        ds.ATT.pop(tid)

    #* Flushing pages from MEMORY TO DISK
    for pageId, recLSN in ds.DPT.items():
        if recLSN <= ds.flushedLSN:
            ds.DISK_MEMORY[pageId] = copy.deepcopy(ds.MEMORY[pageId])

def execute_recovery():
    #* Start the analysis Phase To create ATT and DPT
    analysis_phase()
    redo_phase()
    undo_phase()

    ds.view_system_state(0)