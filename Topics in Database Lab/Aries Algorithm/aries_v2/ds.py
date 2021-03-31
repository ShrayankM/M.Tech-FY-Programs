from tabulate import tabulate

#* Storage for Log Records(On disk and on Memory)
LOG_DISK = {}
LOG_MEMORY = {}

#* Keep track of lastLSN flushed from memory to disk
flushedLSN = None

#* Class for log records
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

#* Class for pages
class Page:
    def __init__(self, pageId, data):
        self.pageId = pageId
        self.pageLSN = None
        self.recLSN = None
        self.data = data
    
    def get_page(self):
        return [str(self.pageId), str(self.pageLSN), str(self.recLSN), str(self.data)] 
    
#* Class for transactions in Active Transaction Table (ATT)
class ActiveTransaction:
    def __init__(self, id, status, lastLSN):
        self.transactionId = id
        self.status = status
        self.lastLSN = lastLSN
    
    def get_transaction(self):
        return [str(self.transactionId), str(self.status), str(self.lastLSN)]


#* Represents the data on DISK(Non-volatile)
DISK_MEMORY = {
    '1': Page('1', {'A': 5, 'B': 15}),
    '2': Page('2', {'C': 10, 'D': 6})
}

#* Represents the data on MEMORY(Volatile)
MEMORY = {}

#* Mapping variables to the pages they belong
page_mapping = {
    'A': '1',
    'B': '1',
    'C': '2',
    'D': '2'
}

#* Tempory buffer for modified data_variables
temp_buffer = {}

#* Active Transaction Table(ATT)
ATT = {}

#* Dirty Page Table (DPT)
DPT = {}

#* state = 1 (view before crash), state = 0 (view after recovery)
def view_system_state(state):
    if (state == 1):
        print('############################# SYSTEM STATE BEFORE CRASH #############################')
    
    if (state == 0):
        print('############################# SYSTEM STATE AFTER RECOVERY ###########################')

    main_records = []
    print("  Log Records[On MAIN]")
    for LSN, logR in LOG_MEMORY.items():
        main_records.append(logR.get_record())
    print(tabulate(main_records, headers = ["LSN", "prevLSN", "TxnId", "type", "data", "before", "after", "undoNext"]))

    print()
    disk_records = []
    print("  Log Records[On DISK]")
    for LSN, logR in LOG_DISK.items():
        disk_records.append(logR.get_record())
    print(tabulate(disk_records, headers = ["LSN", "prevLSN", "TxnId", "type", "data", "before", "after", "undoNext"]))

    print()
    print("  Memory")
    pages = []
    for pageId, page in MEMORY.items():
        pages.append(page.get_page())
    print(tabulate(pages, ["pageId", "pageLSN", "recLSN", "data"]))

    print()
    print("  DISK MEMORY")
    pages = []
    for pageId, page in DISK_MEMORY.items():
        pages.append(page.get_page())
    print(tabulate(pages, ["pageId", "pageLSN", "recLSN", "data"]))

    print()
    print("  Dirty Page Table(DPT)")
    dirty_pages = []
    for pageId, recLSN in DPT.items():
        dirty_pages.append([pageId, recLSN])
    print(tabulate(dirty_pages, headers = ["PageId", "recLSN"]))

    print()
    print("Active Transaction Table(ATT)")
    transactions = []
    for transactionId, transaction in ATT.items():
        transactions.append(transaction.get_transaction())
    print(tabulate(transactions, headers = ["TransactionId", "status", "lastLSN"]))
    
    print('#####################################################################################')