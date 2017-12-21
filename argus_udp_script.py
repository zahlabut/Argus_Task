import argparse
import re
import sys
import os
import platform
from client import *
from server import *

""" Supports Windows Only """
if 'linux' in platform.system().lower():
    print 'ERROR This tool supports windows only!"'
    print "Sorry, but I don't have available Linux at home to test it :( "
    print "As far as I remember there are some differences in socket initiating on Linux"
    sys.exit(1)

"""
Setting command line parameters
Python "argparse" package is used  - module is
Each argument has both forms: short and long + help message
Help message provided per(-) forms
"""
parser = argparse.ArgumentParser(description="Argus CAN Client Server script")
parser.add_argument('-c', '--client',action='store_true',
                    help="If set the script will create a client object")
parser.add_argument('-s', '--server',action='store_true',
                    help="If set the script will create a server object")
parser.add_argument('-p', '--port', type=int,
                    help="port to send or listen to")
parser.add_argument('-a', '--address', type=str,
                    help="address to send or listen to")
parser.add_argument('-C', '--CSV_file_path', type=str,
                    help="path to csv file to read or write to")
parser.add_argument('-t', '--timeout', type=int,
                    help="timeout for the server in seconds")
args = parser.parse_args()



""" Stop execution if --client --serevr options combination is incorrect """
if args.client and args.server:
    print 'ERROR in configuration, you cannot set "--server" and "--client" modes at once!'
    print 'Please choose between "--client" and "--server" modes!'
    sys.exit(1)
if args.client==False  and args.server == False:
    print 'ERROR in configuration, no operation mode was provided by user!'
    print 'Please choose between "--client" and "--server" modes!'
    sys.exit(1)

""" Main """
def main():

    """ Client mode """
    if args.client:

        """ Mandatory variables  validations """
        mandatory_values={'address':args.address, 'port':args.port,'CSV_file_path':args.CSV_file_path}
        for k in mandatory_values.keys():
            if mandatory_values[k]==None:
                print 'ERROR "{}" is mandatory value!'.format(k)
                sys.exit(1)

        """ Validate IP with regex"""
        if re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$",args.address) == None:
            print "ERROR IP value: "+args.address + " is invalid!"
            sys.exit(1)

        """ Validate Port (integer in range 65535) """
        if args.port not in range(0,65535):
            print "ERROR port value: "+str(args.port) + " is not in range of valid ports!"
            sys.exit(1)

        """ Check if CSV path provided by user is existing """
        if os.path.isfile(args.CSV_file_path) == False:
            print "ERROR CSV file path: "+str(args.CSV_file_path) + " was not found!"
            sys.exit(1)

        """ Create Client Object"""
        client_object=ArgosClient(args.address, args.port, args.CSV_file_path)
        client_object.send_messages_from_csv()

    """ Server  mode """
    if args.server:
        """Mandatory variables  validations"""
        mandatory_values={'address':args.address, 'port':args.port,'timeout':args.timeout}
        for k in mandatory_values.keys():
            if mandatory_values[k]==None:
                print 'ERROR "{}" is mandatory value!'.format(k)
                sys.exit(1)

        """ Validate IP with regex"""
        if re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$",args.address) == None:
            print "ERROR IP value: "+args.address + " is invalid!"
            sys.exit(1)

        """ Validate Port (integer in range 65535) """
        if args.port not in range(0,65535):
            print "ERROR port value: "+str(args.port) + " is not in range of valid ports!"
            sys.exit(1)

        """ Create Server Object"""
        server_object=ArgosServer(args.address, args.port, args.timeout)
        server_object.save_logs()

if  __name__ =='__main__':
    main()



