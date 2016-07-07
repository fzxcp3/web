# coding=utf-8
import gevent
import os
import subprocess
import re
import redis
from infor import information
import threading

def sub(domain):
    dic = {}
    ResDict = {}
    queue_db = redis.Redis(host="localhost",port=6379,db=0)
    infor_db = redis.Redis(host="localhost",port=6379,db=1)
    message = ""
    if queue_db.exists(domain):
        lt = queue_db.hgetall(domain)
        for i in lt:
            lt[i] = re.split(", ",lt[i])
            ResDict[i] = {}
            ResDict[i]["ip"] = lt[i]
            infor = infor_db.hgetall(i)
            if infor:
                ResDict[i]["server"] = infor["servers"]
                ResDict[i]["title"] = infor["title"]
            else:
                t = threading.Thread(target=information,args=(i,))
                t.setDaemon(True)
                t.start()
                ResDict[i]["server"] = ""
                ResDict[i]["title"] = ""
        message = "已在任务队列中，目前发现子站数量为"+str(len(lt))
        return ResDict,message
    else:
        print os.getcwd()
        os.chdir("F:/django/MyPOC/POC/controller/subDomain")
        dir = list(os.walk("output/"))[0][2]
        if domain+".txt" not in dir:
            p = subprocess.Popen("python subDomainsBrute.py "+domain+" -t 500",shell=True)
            os.chdir("../../")
            return {},"已经添加到任务队列中，刷新有惊喜..."
        else:
            with open("output/"+domain+".txt") as fd:
                os.chdir("../../")
                content = fd.readlines()
                for i in content:
                    domain,ip = re.split(" *",i.rstrip().lstrip(),maxsplit=1)
                    ResDict[domain] = {}
                    ip = re.split(", ",ip)
                    ResDict[domain]['ip'] = ip
                    infor = infor_db.hgetall(domain)
                    if infor:
                        ResDict[domain]["server"] = infor["servers"]
                        ResDict[domain]["title"] = infor["title"]
                    else:
                        t = threading.Thread(target=information,args=(domain,))
                        t.setDaemon(True)
                        t.start()
                        ResDict[domain]["server"] = ""
                        ResDict[domain]["title"] = ""
            os.chdir("../../../")
            message = "任务执行完毕，发现的子站数目为"+str(len(ResDict))
            return ResDict,message


sub("wooyun.org")