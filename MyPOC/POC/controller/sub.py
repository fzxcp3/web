# coding=utf-8
import os
import subprocess
import re
import redis

def sub(domain):
    dic = {}
    queue_db = redis.Redis(host="localhost",port=6379,db=0)
    message = ""
    if queue_db.exists(domain):
        lt = queue_db.hgetall(domain)
        for i in lt:
            lt[i] = re.split(", ",lt[i])
        message = "已在任务队列中，目前发现子站数量为"+str(len(lt))
        return lt,message
    else:
        print os.getcwd()
        os.chdir("F:/django/MyPOC/POC/controller/subDomain")
        dir = list(os.walk("./"))[0][2]
        print domain+".txt"
        if domain+".txt" not in dir:
            p = subprocess.Popen("python subDomainsBrute.py "+domain+" -t 500",shell=True)
            os.chdir("../../")
            return {},"已经添加到任务队列中，刷新有惊喜..."
        else:
            with open(domain+".txt") as fd:
                os.chdir("../../")
                content = fd.readlines()
                for i in content:
                    domain,ip = re.split(" *",i.rstrip().lstrip(),maxsplit=1)
                    ip = re.split(", ",ip)
                    dic[domain] = ip
            os.chdir("../../../")
            message = "任务执行完毕，发现的子站数目为"+str(len(dic))
            return dic,message
