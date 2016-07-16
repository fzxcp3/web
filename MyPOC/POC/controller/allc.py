#coding=utf-8
import requests
from bing.api import BingSearch
from bing.IPy import IPy
import nmap
import threading
import queue
import time
import redis
import re


class GetAllC(object):
    def __init__(self,ip):
        self.ip = ip
        self.allc_db = redis.Redis(host="localhost",port=6379,db=3)
        self.count1 = 20
        self.count2 = 20

    def AllC(self,ip):
        try:
            result = BingSearch("ip:{0}".format(ip))['d']['results']
        except :
            try:
                result = BingSearch("ip:{0}".format(ip))['d']['results']
            except:
                result = {}
        res={}
        for i in result:
            res[i['Url']] = i['Title']
            '''
            res['Url'].append(i['Url'])
            res['Title'].append(i['Title'])
            '''
        self.allc_db.hmset(ip,{"bingC":res})
        return

    def portScan(self,ip):
        nm=nmap.PortScanner()
        nm.scan(hosts=ip,ports="21-25,80-89,389,443,873,1080,1090,1433,1434,1521,7001,8000-8090,8888,9000,2181,27017,28017,5432,11211,9001,4848,2375,1352,5984,5666,3128,3306,3389,9080,9081,9090,8649,9200,9043,4848,50060,3690",arguments='-sV --script=banner')
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
                    try:
                        for key,banner in nm[host]['tcp'][i]['script'].items():
                            res[host][i]['banner'] += banner+";"
                    except:
                        pass
            try:
                self.allc_db.hmset(ip,{"nmap":res[host]})
            except:
                pass
        return

    def getALL(self):
        ip = self.ip
        ips = self.ipGenerate(ip)
        pool_0 = []
        pool_1 = []
        q_0 = queue.Queue()
        q_1 = queue.Queue()
        for i in ips:
            q_0.put(i)
            q_1.put(i)
        for i in xrange(20):
            t1 = threading.Thread(target=self.AllC,args=(q_0.get(),))
            t2 = threading.Thread(target=self.portScan,args=(q_1.get(),))
            pool_0.append(t1)
            pool_1.append(t2)
            t1.setDaemon(True)
            t1.start()
            t2.setDaemon(True)
            t2.start()
        while True:
            for x in pool_0:
                if not x.isAlive():
                    pool_0.remove(x)
                    if not q_0.empty():
                        t1 = threading.Thread(target=self.AllC,args=(q_0.get(),))
                        pool_0.insert(0,t1)
                        t1.setDaemon(True)
                        t1.start()
            for y in pool_1:
                if not y.isAlive():
                    pool_1.remove(y)
                    if not q_1.empty():
                        t2 = threading.Thread(target=self.portScan,args=(q_1.get(),))
                        pool_1.insert(0,t2)
                        t2.setDaemon(True)
                        t2.start()
            if len(pool_0) == 0 and len(pool_1) == 0:
                break
            time.sleep(1)
        return


    def ipGenerate(self,ip):
        ips = []
        if not re.match('^(10|127|172|192)+.\d+.\d+.\d+',ip):
            ip=re.findall(r'\d+.\d+.\d+.',ip)
            for i in range(1,256):
                ip1=ip[0]+str(i)
                ips.append(ip1)
        return ips



def ScanC(ip):
    allc_db = redis.Redis(host="localhost",port=6379,db=3)
    ip_c = re.search("(.+?)\.(.+?)\.(.+?)\.",ip).group(0)+"*"
    res = allc_db.keys(ip_c)
    if len(res) == 0:
        f = lambda x : GetAllC(ip).getALL()
        t1 = threading.Thread(target=f,args=(ip,))
        t1.setDaemon(True)
        t1.start()
        return {},"已添加到任务队列..."
    else:
        result = {}
        for i in res:
            result[i] = allc_db.hgetall(i)
            for t in result[i]:
                result[i][t] = eval(result[i][t])
        return result,"扫描进行中/已经完成，已得到结果:"+str(len(res))