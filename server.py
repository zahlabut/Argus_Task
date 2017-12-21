import socket
import datetime
import csv
from collections import Counter

class ArgosServer():

    def __init__(self, ip, port, timeout):
        self.ip = ip
        self.port=port
        self.timeout=timeout

    """ Parse CAN package, if len is less that 4 WARNING will be printed and package will be ignored"""
    def parse_package(self, data):
        if len(data)>4:
            MSG_ID=data[0:2]
            LENGTH=data[2:4]
            DATA=data[4:-5]
            return {'MSG_ID':MSG_ID,'LENGTH':LENGTH,'DATA':DATA}
        else:
            print 'WARNING '+data+' is not valid CAN Package!'
            return {'MSG_ID':None,'LENGTH':None,'DATA':data}

    """ Save text to file (overriding existing content in file) """
    def save_text_to_file(self, file_name, content):
        fil=open(file_name,'w')
        fil.write(content)
        fil.close()

    """ Generate statistics content + saving logs"""
    def save_logs(self):
        data_list=self.activate_server()
        all_ids=[i['MSG_ID'] for i in data_list]
        statistics_content=''
        statistics_content+='-'*70+'\n'
        statistics_content+='How many times a specific CAN msg-id appear.'+'\n'
        statistics_content+='(MSG_ID, Counter)'+'\n'
        for item in Counter(all_ids).iteritems():
            statistics_content+=str(item)+'\n'
        statistics_content+='-'*70+'\n'
        statistics_content+='What is the sum of all messages data length received by the server.'+'\n'
        statistics_content+=str(sum([int(i['LENGTH']) for i in data_list]))+'[Bytes]'+'\n'
        statistics_content+='-'*70+'\n'
        statistics_content+='How many packets received by the server.'+'\n'
        statistics_content+=str(len(data_list))+' packages'+'\n'
        statistics_content+='-'*70+'\n'
        self.save_text_to_file('Statistics.log',statistics_content)
        self.save_list_of_dicts_csv('Received_Packages.csv',self.received_packages)

    """ Write list of received CAN packages (dictionaries) to CSV file"""
    def save_list_of_dicts_csv(self, scv_name,list_of_dicts):
        if len(list_of_dicts)>0:
            with open(scv_name,'w') as csvfile:
                fieldnames = list_of_dicts[0].keys()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames,lineterminator='\n')
                writer.writeheader()
                for d in list_of_dicts:
                    writer.writerow(d)
        else:
            print 'WARNING received by function list of dictionaries is empty!'

    """
    Activate UDP server + exception handling: socket timeout, port is already in use, and so on...
    Method returns list of dictionaries, where each dictionary is a parsed CAN package
    """
    def activate_server(self):
        self.received_packages=[]
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((self.ip, self.port))
        sock.settimeout(self.timeout)
        try:
            counter=0
            while True:
                data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
                counter+=1
                print "--> ",counter,datetime.datetime.now(),'\t',data
                self.received_packages.append(self.parse_package(data))
        except Exception,e:
            print e
        return self.received_packages
