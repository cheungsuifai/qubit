

def parse_alert(alert_content:str):
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



if __name__ == '__main__':
    print("Qubit! pg analyzer")

    file_name = r'C:\Users\esuizha\PycharmProjects\qubit\input\pg_alert_sample.txt'
    #file_name = r'/Users/shinechan/PycharmProjects/qubit/input/pg_alert_sample.txt'
    file = open(file_name,'r')

    alert_content = ''

    for line in file.readlines():
        alert_content = alert_content +line
        #line = line.lstrip().rstrip()
        #print(line)
        #line.find("分析结果")
    print(alert_content)
    cont = parse_alert(alert_content)
    print(cont)
