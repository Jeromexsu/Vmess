import argparse
import v2client
parser = argparse.ArgumentParser("v2utils")
parser.add_argument("-l","--list",action="store_true",help="list all clients and exit")
parser.add_argument("-a","--all",nargs="+",help="add clients",metavar="email")
parser.add_argument("-d","--delete",nargs="+",help="invalidate clients",metavar="email")
parser.add_argument("-c","--clean",action="store_true",help="remove all invalid clients")
args = parser.parse_args()
if(args.list): 
    v2client.list()
    exit(0)
if(args.all != None):
    for email in args.all :
        id = v2client.add(email)
        if id != None :print(email+"\t" + str(id))
        else: print(email+"\tuser existed!")
if(args.delete != None):
    for email in args.delete:
        v2client.invalidate(email)
if(args.clean): v2client.clean()