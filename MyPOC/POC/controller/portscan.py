#coding=utf-8
import nmap
import redis
import threading

def nmap_scan(ip):
    port_db = redis.Redis(host='localhost',port=6379,db=2)
    fd = open(ip+'.txt','w+')
    nm=nmap.PortScanner()
    nm.scan(hosts=ip,ports='21-25,80-89,389,443,873,1080,1090,1433,1434,1521,7001,8000-8090,8888,9000,2181,27017,28017,5432,11211,9001,4848,2375,1352,5984,5666,3128,3306,3389,9080,9081,9090,8649,9200,9043,4848,50060,3690',arguments='-sV --script=banner')
    hosts=nm.all_hosts()
    res = {}
    for host in hosts:
        result=nm[host]['tcp'].keys()
        for i in result:
            if nm[host]['tcp'][i]['state']=="open":
                res[host] = {}
                res[host][i]={}
                res[host][i]['service'] = nm[host]['tcp'][i]['product']
                res[host][i]['banner'] = ""
                for key,banner in nm[host]['tcp'][i]['script'].items():
                    res[host][i]['banner'] += banner+";"
                fd.write(str(i)+"|-|"+res[host][i]['service']+"|-|"+res[host][i]['banner'])
        port_db.hmset(host,res[host])
    return

def port_infor(ip):
    port_db = redis.Redis(host='localhost',port=6379,db=2)
    res = port_db.hgetall(ip)
    if res:
        return res,"扫描结束"
    else:
        t = threading.Thread(target=nmap_scan,args=(ip,))
        t.setDaemon(True)
        t.start()
        return {},"端口扫描中..."

