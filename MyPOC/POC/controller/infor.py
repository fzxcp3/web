#coding=utf-8
import requests
from bs4 import BeautifulSoup
import re
from C_bing import bing_Query,conver
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import redis
import threading

def information(domain):
    infor_db = redis.Redis(host='localhost', port=6379, db=1)
    try:
        dic = {domain:{}}
        try:
            req = requests.get("http://"+domain)
        except:
            print "http://"+domain
            req = requests.get("https://"+domain)
        meta_reg = r"<meta.*?charset=['\"]?([^'\"><]*)?.*?>"
        if req.encoding == 'ISO-8859-1':
            try:
                m = re.search(meta_reg, req.text, re.I)
                if m:
                    req.encoding = m.group(1)
                else:
                    req.encoding = 'utf-8'
            except:
                pass
        bs = BeautifulSoup(req.text,'lxml')
        title = bs.html.head.title.string
        infor_db.hmset(domain,{"title":title})
        for i in req.headers:
            if re.search("server",i,re.I):
                servers = req.headers[i]
            elif re.search("power",i,re.I):
                servers += req.headers[i]
        infor_db.hmset(domain,{"servers":servers})
    except Exception,e:
        print e.message
        infor_db.hmset(domain,{"title":""})
        infor_db.hmset(domain,{"servers":""})
    return

