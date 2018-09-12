import time
import requests
import itchat
from itchat.content import TEXT
import re
from process_provider import Operation,OperationSequence
import csv

def parse_msg(msg:str):
    alert_content_valid_flag = True
    loc = msg.find("【智能告警分析】")
    if loc > -1:
        return "alert"
    else:
        return "unknown"


def parse_ne_type(alert_content:str):
    alert_content_valid_flag = True
    loc1 = alert_content.find("告警对象")
    loc2 = alert_content.find("时间")
    if loc1 > -1:
        alert_content = alert_content[loc1:loc2]
        loc1 = alert_content.find("：")
        alert_content= alert_content[loc1+1:].lstrip().rstrip()
    pg_pattern = re.compile(r'((GZ)|(SZH)|(FOS)|(JIM)|(ZJI))HSS[0-9]+(BE)0[1-2]BER_PG$')
    cudb_pattern = re.compile(r'((GZ)|(SZH)|(FOS)|(JIM)|(ZJI))HSS[0-9]+(BE)0[1-2]BER$')
    hlr_pattern = re.compile(r'((GZ)|(SZH)|(FOS)|(JIM)|(ZJI))HSS[0-9]+(FE)20[1-2]BER$')
    hss_pattern = re.compile(r'((GZ)|(SZH)|(FOS)|(JIM)|(ZJI))HSS[0-9]+(FE)10[1-2]BER$')
    if pg_pattern.match(alert_content) is not None:
        return "PG"
    if cudb_pattern.match(alert_content) is not None:
        return "CUDB"
    if hlr_pattern.match(alert_content) is not None:
        return "HLR"
    if hss_pattern.match(alert_content) is not None:
        return "HSS"
    return None


def parse_alert_result(alert_content:str):
    alert_content_valid_flag = True

    loc = alert_content.find("分析结果")
    if loc > -1 :
        alert_content = alert_content[loc:]
        loc = alert_content.find('{')
        if loc > -1:
            alert_content = alert_content[loc+1:]
            loc = alert_content.find('}')
            if loc > -1:
                alert_content = alert_content[0:loc].lstrip().rstrip()
                alert_content_valid_flag = True

            else:
                alert_content_valid_flag = False
        else:
            alert_content_valid_flag = False
    else:
        alert_content_valid_flag = False

    result_dict = dict()
    if alert_content_valid_flag :
        result_list = alert_content.split(',')
        for result in result_list:
            pa = result.split(':')
            result_dict[pa[0].lstrip().rstrip()] = pa[1].lstrip().rstrip()
    return result_dict


@itchat.msg_register(TEXT, isGroupChat=True)
def reply_otp(msg):
    fromuser = str(msg['FromUserName'])
    touser = str(msg['ToUserName'])

    group_id=""
    if(fromuser.startswith("@@")):
        group_id = fromuser
    if (touser.startswith("@@")):
        group_id = touser
    username = msg['ActualNickName']
    print(msg)

    if(group_id=='@@66147814a90627e81db7633364b852f209dc49eedcda4f50447e7e582b9ba5a7'):
        print(msg)
        print(username)
        msgText = msg['Text']

        type = parse_msg(msgText)
        if type == 'alert':
            ne_type = parse_ne_type(msgText)

            if ne_type == 'PG':

                print('Handling PG alert...')
                resut_dict = parse_alert_result(msgText)
                itchat.send_msg('系统判断故障概率分布为：'+str(resut_dict),toUserName='@@66147814a90627e81db7633364b852f209dc49eedcda4f50447e7e582b9ba5a7')


                if list(resut_dict.keys())[0] in ['PG', 'HLR', 'HSS', 'CUDB', 'UserData', 'Boss']:
                    file_name = r'C:\Users\esuizha\PycharmProjects\qubit\input\pg_operations.csv'
                    operation_list = []
                    with open(file_name, encoding='utf-8') as f:
                        f_csv = csv.reader(f)
                        # headers = next(f_csv)
                        next(f_csv, None)

                        for row in f_csv:
                            # print(row)
                            root_id = row[0]
                            sub_id = row[1]
                            slogan = row[2]
                            type = row[3]
                            node = row[4]
                            mode = row[5]
                            command = row[6]
                            operation = Operation(root_id, sub_id, slogan, type, node, mode, command)
                            operation_list.append(operation)

                    #for op in operation_list:
                        #print(op)


                    all_pg_ops = OperationSequence(operation_list)
                    # print(all_pg_ops)

                    pg_pg_ops = OperationSequence(operation_list[0:12])

                    pg_hlr_ops = OperationSequence(operation_list[25:30])

                    pg_cudb_ops = OperationSequence(operation_list[15:25])
                    pg_hss_ops = OperationSequence(operation_list[35:37])
                    pg_userdata_ops = OperationSequence(operation_list[30:35])
                    pg_boss_ops = OperationSequence(operation_list[37:])

                    ops_dict = dict()
                    ops_dict['PG'] = pg_pg_ops
                    ops_dict['HLR'] = pg_hlr_ops
                    ops_dict['CUDB'] = pg_cudb_ops
                    ops_dict['HSS'] = pg_hss_ops

                    ops_dict['UserData'] = pg_userdata_ops
                    ops_dict['Boss'] = pg_boss_ops
                    #print(ops_dict[resut_dict.keys()[0]])
                    itchat.send_msg(str(ops_dict[list(resut_dict.keys())[0]]),toUserName='@@66147814a90627e81db7633364b852f209dc49eedcda4f50447e7e582b9ba5a7')
                # elif input_string=="End":
                else:
                    print('Invalid input')

            else:
                print('Not implement yet!')
        else:
            print('unknown')



if __name__ == '__main__':
    itchat.auto_login(hotReload=True)

    friend_idct = dict()
    group_idct = dict()

    friend_list = itchat.get_friends(update=True)[1:]
    chatroom_list = itchat.get_chatrooms(update=True)[1:]

    for friend in friend_list:
        friend_idct[friend['NickName']] = friend['UserName']

    for chatroom in chatroom_list:
        group_idct[chatroom['NickName']] = chatroom['UserName']

    for f_name in group_idct.keys():
        print(f_name, group_idct[f_name])

    itchat.run()

    #@@66147814a90627e81db7633364b852f209dc49eedcda4f50447e7e582b9ba5a7