#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import urllib3
import json

def es(cmd):
    try:
        header = { 'Content-Type': 'application/json' }
        data = {}
        if cmd[1] == "i":
            rtn = es_rtn('GET', "localhost:9200", data, header)
        elif cmd[1] == "h":
            rtn = es_rtn('GET', "localhost:9200" + "/_cat/health?v", data, header)
        elif cmd[1] == "n":
            rtn = es_rtn('GET', "localhost:9200" + "/_cat/nodes?v", data, header)
        elif cmd[1] == "m":
            rtn = es_rtn('GET', "localhost:9200" + "/_cat/master?v", data, header)
        elif cmd[1] == "idx":
            rtn = es_rtn('GET', "localhost:9200" + "/_cat/indices?v", data, header)
        elif cmd[1] == "re":
            data = '{ "transient" : { "cluster.routing.allocation.enable" : "new_primaries" } }'
            rtn = es_rtn('PUT', "localhost:9200" + "/_cluster/settings", json.loads(data), header)
        elif cmd[1] == "rd":
            data = '{ "transient" : { "cluster.routing.allocation.enable" : null } }'
            rtn = es_rtn('PUT', "localhost:9200" + "/_cluster/settings", json.loads(data), header)
        elif cmd[1] == "ex":
            rtn = es_rtn('POST', "localhost:9200" + "/_cluster/allocation/explain", data, header)
        elif cmd[1] == "f":
            rtn = es_rtn('POST', "localhost:9200" + "/_cluster/reroute?retry_failed", data, header)
        else:
            rtn = "incorrect commands"
        print rtn
        return rtn

    except IndexError:
        rtn = "Usage : ./esbot [options] \n\n\
        i : ES Info\n\
        h : ES Health\n\
        n : Node Info\n\
        m : master Info\n\
        idx : ES Health\n\
        re : routing enable\n\
        rd : routing disable\n\
        ex : routing disable\n\
        f : retry failed\n\
        "
        print rtn
        return rtn

def es_rtn(method, cmd, data=None, header=None):
    http = urllib3.PoolManager()

    try:
        rtn = http.request(method,cmd,body=json.dumps(data),headers=header).data
    except urllib3.exceptions.HTTPError as errh:
        rtn = "Http Error:",errh

    return rtn

if __name__ == '__main__':
    es(sys.argv)
