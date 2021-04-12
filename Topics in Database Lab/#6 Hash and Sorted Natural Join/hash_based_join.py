# from tabulate import tabulate

def hash_function(h, k):
    return h % k;

class RecordA:
    def __init__(self, item_id, item_name, item_unit, company_id):
        self.item_id = item_id
        self.item_name = item_name
        self.item_unit = item_unit
        self.company_id = company_id
    
    def __str__(self):
        return str([str(self.item_id), str(self.item_name), str(self.item_unit), str(self.company_id)])


class RecordB:
    def __init__(self, company_id, company_name, company_city):
        self.company_id = company_id
        self.company_name = company_name
        self.company_city = company_city
        self.hash = None

#* The common attribute is company_id

relation_A = list()
relation_B = list()

relation_A.append(RecordA(1, 'Chex Mix', 'Pcs', 16))
relation_A.append(RecordA(6, 'Cheez-It', 'Pcs', 15))
relation_A.append(RecordA(2, 'BN Biscuit', 'Pcs', 15))
relation_A.append(RecordA(3, 'Mighty Munch', 'Pcs', 17))
relation_A.append(RecordA(4, 'Pot Rice', 'Pcs', 15))
relation_A.append(RecordA(5, 'Jaffa Cakes', 'Pcs', 18))
relation_A.append(RecordA(7, 'Salt n Shake', 'Pcs', 0))

relation_B.append(RecordB(18, 'Order All', 'Boston'))
relation_B.append(RecordB(15, 'Jack Hill Ltd', 'London'))
relation_B.append(RecordB(16, 'Akas Foods', 'Delhi'))
relation_B.append(RecordB(17, 'Foodies', 'London'))
relation_B.append(RecordB(19, 'Sip-n-Bite', 'New York'))

#* Build Phase
hashed_relation_A = {}
for record in relation_A:
    h = hash_function(record.company_id, len(relation_A))
    hashed_relation_A[h] = record

for hash_id, record in hashed_relation_A.items():
    print(hash_id, record)

