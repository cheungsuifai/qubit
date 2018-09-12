import csv

class Operation():
    def __init__(self,root_id,sub_id,slogan,type,node,mode,command):
        self.info = dict()
        self.info['root_id'] = root_id
        self.info['sub_id'] = sub_id
        self.info['slogan'] = slogan
        self.info['type'] = type
        self.info['node'] = node
        self.info['mode'] = mode
        self.info['command'] = command

    def get_title(self):
        return self.info['root_id']+"."+self.info['sub_id']+" "+self.info['slogan']
    def __str__(self):
        return str(self.info)


class OperationSequence():
    #def __init__(self,*operations):
    #    self.operation_dict = dict()
    #    for op in operations:
    #        self.operation_dict[op.get_title()]=op

    def __init__(self,operation_list):
        self.operation_dict = dict()
        for op in operation_list:
            self.operation_dict[op.get_title()] = op


    def __str__(self):
        info = ''

        for op in self.operation_dict.values():
            info = info +op.get_title()+'\n'

        return info


if __name__ == '__main__':
    print("Qubit! pg process provider")
    file_name = r'C:\Users\esuizha\PycharmProjects\qubit\input\pg_operations.csv'
    operation_list=[]
    with open(file_name,encoding='utf-8') as f:
        f_csv = csv.reader(f)
        #headers = next(f_csv)
        next(f_csv, None)

        for row in f_csv:
            #print(row)
            root_id = row[0]
            sub_id = row[1]
            slogan = row[2]
            type = row[3]
            node = row[4]
            mode = row[5]
            command = row[6]
            operation = Operation(root_id,sub_id,slogan,type,node,mode,command)
            operation_list.append(operation)

    for op in operation_list:
        print(op)

    all_pg_ops = OperationSequence(operation_list)
    #print(all_pg_ops)

    pg_pg_ops = OperationSequence(operation_list[0:12])

    pg_hlr_ops = OperationSequence(operation_list[25:30])

    pg_cudb_ops = OperationSequence(operation_list[15:25])
    pg_hss_ops = OperationSequence(operation_list[35:37])
    pg_userdata_ops = OperationSequence(operation_list[30:35])
    pg_boss_ops = OperationSequence(operation_list[37:])

