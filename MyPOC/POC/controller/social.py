from bs4 import BeautifulSoup
import requests
import json
import re
from pprint import pprint

def get_core():
    try:
        req = requests.get("http://localhost:8983/solr/admin/cores?wt=json&indexInfo=false",timeout=5)
    except Exception,e:
        return []
    res = json.loads(req.text)
    result = []
    for i in res['status']:
        result.append(i)
    return result

def get_query(keyword,cores):
    result = {}
    result["keyword"] = []
    result["content"] = []
    for core in cores:
        if core == "solr_mysql":
            url = "http://localhost:8983/solr/{1}/select?q=content%3A{0}&wt=json&indent=true".format(keyword,core)
            try:
                req =  requests.get(url)
                res = json.loads(req.text)
                for i in res["response"]["docs"]:
                    i["content"] = i["content"].rstrip().lstrip()
                    i["content"] = re.sub("\t+"," |- - - - - - - - - - - - - - - - - -  - - - - - - -| ",i["content"])
                    i["content"] = re.sub("----"," |- - - - - - - - - - - - - - - - - -  - - - - - - -| ",i["content"])
                    i["content"] = re.sub(" # "," |- - - - - - - - - - - - - - - - - -  - - - - - - -| ",i["content"])
                    result["content"].append(i)
            except Exception,e:
                pass
        else :
            url = "http://localhost:8983/solr/{1}/select?q=keyword%3A{0}&wt=json&indent=true".format(keyword,core)
            try:
                req =  requests.get(url)
                res = json.loads(req.text)
                for i in res["response"]["docs"]:
                    result["keyword"].append(i)
            except Exception,e:
                pass
    return result

