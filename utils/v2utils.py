import argparse
import v2client
from utils import mail
default_path = "/usr/local/etc/v2ray/config.json"
parser = argparse.ArgumentParser("v2utils")
parser.add_argument("-l","--list",action="store_true",help="list all clients and exit")
parser.add_argument("-a","--all",nargs="+",help="add clients",metavar="email")
parser.add_argument("-d","--delete",nargs="+",help="invalidate clients",metavar="email")
parser.add_argument("-c","--clean",action="store_true",help="remove all invalid clients")
parser.add_argument("-p","--config_path",default=default_path)
args = parser.parse_args()
print(args)
config_path = args.config_path
if(args.list): 
    v2client.list()
    exit(0)
if(args.all != None):
    for email in args.all :
        id = v2client.add(email,config_path)
        if id != None :
            print(email+"\t" + str(id))
            mail("csu22@m.fudan.edu.cn","PsYRXuo2FAJJaJTF","22210170021@m.fudan.edu.cn","你好，你的UUID是"+id,"注册成功")
        else: print(email+"\tuser existed!")
if(args.delete != None):
    for email in args.delete:
        v2client.invalidate(email,config_path)
if(args.clean): v2client.clean()