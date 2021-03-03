def get_value(ins, a, b):
    if (ins.find('+')): return a + b
    if (ins.find('-')): return a - b
    if (ins.find('*')): return a * b
    if (ins.find('/')): return a / b

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
            
            if (operation == 'READ'):
                data_item = ins[ins.find('(') + 1:ins.find(',')]
                transaction = ins[ins.find(' ') + 1:ins.find(')')]
                log_file.write(f"<{transaction} READ {data_item}>\n")
            
            if (operation == 'WRITE'):
                data_item = ins[ins.find('(') + 1:ins.find(',')]
                transaction = ins[ins.find(' ') + 1:ins.find(')')]
                log_file.write(f"<{transaction} WRITE {data_item}>\n")
            
            if (operation == 'COMMIT'):
                transaction = ins[ins.find('(') + 1:ins.find(')')]
                log_file.write(f"<COMMIT {transaction}>\n")

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
                a = main_disk[a]
            except:
                #* GET BOTH a and b FROM MAIN DISK
                a = main_disk[a]
                b = main_disk[b]
            current_value = main_disk[updating_data]
            updated_value = get_value(ins, a, b)
            log_file.write(f"<{ins[ins.find('_') + 1:]} {updating_data} {current_value} {updated_value}>\n")
            continue                           


main_disk = {
    'A': 100,
    'B': 200
}

file = open("transaction_input.txt", "r")
data = []

for line in file:
    data.append(line.strip())

instrus_cnt = int(data[0])
instructions = data[1:]

create_log(instrus_cnt, instructions)