import requests
import Queue
import threading
import re
import sys
import time
import bing.IPy.IPy
from bing.bingC import *
import dns.resolver
from pprint import pprint

def bing_Query(ip):
    result = []
    try:
        _list = IPy.IP(ip)
    except Exception, e:
        sys.exit('Invalid IP/MASK, %s' % e)
    for each in _list:
        queue.put(str(each))
    runThreads()
    for id,res in enumerate(ips):
        ip ,res = re.split(" -> ",res)
        netloc =  re.split(" | ",res)[0]
        title = re.split(" | ",res)[2]
        result.append({ip:{netloc:title}})
    return result

def Query(query):
    d = ""
    if re.search("/(\d+)",query):
        query,d =  re.split("/",query)
    if not re.match("((\d+)\.(\d+)\.(\d+)\.\d+)",query):
        ip = dns.resolver.query(query,"A")
        for i in ip:
            i = str(i)
            ip_c = re.match("((\d+)\.(\d+)\.(\d+)\.)",i)
            ip_c = ip_c.group(0)+"0"
            try:
                generate = ip_c+"/"+d
            except:
                generate = ip_c

Query("www.wecash.net")


def conver(query):
    if not re.match("((\d+)\.(\d+)\.(\d+)\.\d+)",query):
        ip = dns.resolver.query(query,"A")
        ips = ""
        for i in ip:
            ips += str(i)+" "
        return ips
    else:
        return query

#pprint(bing_Query("www.wecash.net"))

#result = "127.0.0.1 -> www.baidu.com | abcd"
#print re.split(" -> ",result)
