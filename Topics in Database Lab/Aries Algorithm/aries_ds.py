from tabulate import tabulate

#* Data-Structures

LOG_MAIN = {}
LOG_DISK = {}

flushedLSN = None

class LogRecord:
    def __init__(self, LSN, prevLSN, TxnId, type, dataItem, before, after, undoNext):
        self.LSN = LSN
        self.prevLSN = prevLSN
        self.TxnId = TxnId
        self.type = type
        self.dataItem = dataItem
        self.before = before
        self.after = after
        self.undoNext = undoNext
    
    def get_record(self):
        return [str(self.LSN), str(self.prevLSN), str(self.TxnId), str(self.type), str(self.dataItem), str(self.before), str(self.after), str(self.undoNext)] 

class Page:
    def __init__(self, pageId, data):
        self.pageId = pageId
        self.pageLSN = None
        self.recLSN = None
        self.data = data
    
    def get_page(self):
        return [str(self.pageId), str(self.pageLSN), str(self.recLSN), str(self.data)] 
    
    def search_data(self, d):
        if self.data.get(d): return self.pageId
        return -1
    
    def get_data_value(self, dId):
        return self.data[dId]

class ActiveTransaction:
    def __init__(self, id, status, lastLSN):
        self.transactionId = id
        self.status = status
        self.lastLSN = lastLSN
    
    def get_active_transaction(self):
        return [str(self.transactionId), str(self.status), str(self.lastLSN)]

page_table = {
    'A': '1',
    'B': '1',
    'C': '2',
    'D': '2'
} 

main_memory = {}

disk_memory = {
    '1': Page('1', {'A': 5, 'B': 6}),
    '2': Page('2', {'C': 10, 'D': 9})
}

active_transaction_table = {}
dirty_page_table = {}

temp_values = {}
