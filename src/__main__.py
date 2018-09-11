




if __name__ == '__main__':
    print("Qubit!")

    file = open(r'/Users/shinechan/PycharmProjects/qubit/log/FOSHSS01FE201BER.log','r')

    begin = False
    for line in file.readlines():
        line = line.lstrip().rstrip()
        #print(line)

        if line.lower().find('c7ltp:ls=all;') > -1:
            begin = True

        if begin and line == 'END':
            begin = False

        if begin:
            print(line)
