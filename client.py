import socket
import csv

class ArgosClient():
    def __init__(self, dst_ip, dst_port, csv_path):
        self.dst_ip = dst_ip
        self.dst_port=dst_port
        self.csv_path=csv_path

    """ Send single UDP package on socket """
    def send_single_message(self,message):
        print  '--> '+message
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(message, (self.dst_ip, self.dst_port))

    """
    CSV should contain fields: 'MSG_ID', 'LENGTH', 'DATA' (case sensitive!!!)
    There is no validation for CAN package content in code
     """
    def send_messages_from_csv(self):
        with open(self.csv_path) as f:
            reader = csv.DictReader(f)
            for row in reader:
                message=row['MSG_ID']+'0'+row['LENGTH']+row['DATA']+'00000'
                self.send_single_message(message)