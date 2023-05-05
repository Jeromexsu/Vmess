import argparse
import v2client
from utils import mail
import json
def send_notice(id,email):
    url = "https://jeremysu.xyz/posts/jmess_help/"
    text = "<html>\
    <body>\
        <p>你好，你的JMess已注册成功。下方是你的uuid</p>\
        <p style=\"text-align: center;\"><b>%s</b></p>\
        <p style=\"color: brown;\">⚠️注意：无论在任何情况下，都不要泄露你的id。</p>\
        <p>📎附件是你可能用到的文件，使用方法参见<a href= %s>使用教程</a></p>\
    </body>\
    </html>" % (id,url)

    #write shadowrocket
    shr_conf_path = "../conf/shadowrocket.json"
    with open(shr_conf_path,"r") as shrfile:
        js = json.load(shrfile)
    js["uuid"] = id
    js["password"] = id
    with open(shr_conf_path,"w") as shrfile:
        json.dump(js,shrfile,indent=4)
    
    #write clashx
    clashx_temp_path = "../conf/JMess_ClashX_template.yaml"
    clashx_conf_path = "../conf/JMess_ClashX.yaml"
    with open(clashx_temp_path,"r") as temp:
        lines = temp.readlines()
        for (index,line) in enumerate(lines):
            if line == '    uuid:\n':
                lines[index] = line[:-1]+(" %s\n" % id)
    with open(clashx_conf_path,'w') as conf:
        for line in lines: conf.write(line)
    
    attaches = [shr_conf_path,clashx_conf_path]
    mail("csu22@m.fudan.edu.cn","PsYRXuo2FAJJaJTF",email,text,"[JMess]注册成功通知",attaches)

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
    v2client.list(config_path)
    exit(0)
if(args.all != None):
    for email in args.all :
        id = v2client.add(email,config_path)
        if id != None :
            print(email+"\t" + str(id))
            send_notice(id,email)
        else: print(email+"\tuser existed!")
if(args.delete != None):
    for email in args.delete:
        v2client.invalidate(email,config_path)
if(args.clean): v2client.clean(config_path)