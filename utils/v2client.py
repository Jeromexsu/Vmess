import json
import uuid
default_path = "/usr/local/etc/v2ray/config.json"
def list(path:str=default_path):
    with open(path,"r") as v2ray_conf_file:
        js = json.load(v2ray_conf_file)
    clients = js["inbounds"][0]["settings"]["clients"]
    for client in clients:
        print(client)

def existed(email:str,path:str=default_path) -> bool:
    with open(path,"r") as v2ray_conf_file:
        js = json.load(v2ray_conf_file)
    clients = js["inbounds"][0]["settings"]["clients"]
    for client in clients:
        if client["email"] == email and client["id"] != 'a':
            return True
    return False

def add(email:str,path:str=default_path) -> str :
    with open(path,"r") as v2ray_conf_file:
        js = json.load(v2ray_conf_file)
    clients = js["inbounds"][0]["settings"]["clients"]
    
    if existed(email,path): return None

    id = str(uuid.uuid3(uuid.NAMESPACE_URL,email))
    client = {"email":email,"id":id,"level":0,"alertId":0}
    clients.append(client)
    with open(path,"w") as v2ray_conf_file:
        json.dump(js,v2ray_conf_file,indent=4)
    return id

def invalidate(email:str,path:str=default_path) -> None:
    with open(path,"r") as v2ray_conf_file:
        js = json.load(v2ray_conf_file)
    clients:list = js["inbounds"][0]["settings"]["clients"]
    for client in clients:
        if client["email"] == email:
            client["id"] = ""
    with open(path,"w") as v2ray_conf_file:
        json.dump(js,v2ray_conf_file,indent=4)

def clean(path:str=default_path) -> None: 
    with open(path,"r") as v2ray_conf_file:
        js = json.load(v2ray_conf_file)
    clients:list = js["inbounds"][0]["settings"]["clients"]
    clients.sort(key=lambda client: client["id"])
    while clients != [] and clients[0]["id"] == "":
        clients.pop(0)
    with open(path,"w") as v2ray_conf_file:
        json.dump(js,v2ray_conf_file,indent=4)

import argparse
if __name__ == "__main__":
    parser = argparse.ArgumentParser("v2utils")
    parser.add_argument("-l","--list",action="store_true",help="list all clients and exit")
    parser.add_argument("-a","--all",nargs="+",help="add clients",metavar="email")
    parser.add_argument("-d","--delete",nargs="+",help="invalidate clients",metavar="email")
    parser.add_argument("-c","--clean",action="store_true",help="remove all invalid clients")
    args = parser.parse_args()
    if(args.l): 
        list()
        exit(0)
    if(args.all != None):
       for email in args.all :
            id = add(email)
            if id != None :print(email+"\t" + str(id))
            else: print(email+"\tuser existed!")
    if(args.delete != None):
        for email in args.delete:
            invalidate(email)
    if(args.clean): clean()

    
