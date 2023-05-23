#!/usr/bin/env python
import json
import base64
import urllib.request

external_ip = urllib.request.urlopen('https://ident.me').read().decode('utf8')

config = json.load(open("/var/snap/shadowsocks-libev/common/etc/shadowsocks-libev/config.json"))
u=config['method']+":"+config['password']
u= base64.b64encode(u.encode("utf-8")).decode("utf-8")
print("ss://"+u+"@"+str(external_ip)+":"+str(config["server_port"]))
