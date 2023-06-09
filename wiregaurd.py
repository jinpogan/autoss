from os import system as cmd
import os
import requests
cmd('''sudo apt -y update&&sudo apt -y install wireguard ufw&&wg genkey | sudo tee /etc/wireguard/private.key&&sudo chmod go= /etc/wireguard/private.key&&sudo cat /etc/wireguard/private.key | wg pubkey | sudo tee /etc/wireguard/public.key''')
with open("/etc/wireguard/private.key","r") as f:
    spk=f.read()
with open("/etc/wireguard/public.key","r") as f:
    sk=f.read()
with open("/etc/wireguard/wg0.conf","w") as f:
    a='''
[Interface]
PrivateKey = '''+spk+'''
Address = 10.8.0.1/24, fd0d:86fa:c3bc::1/64
ListenPort = 1314
SaveConfig = true
    '''
    f.write(a)
with open("/etc/sysctl.conf","a") as f:
    f.write("\nnet.ipv4.ip_forward=1\nnet.ipv6.conf.all.forwarding=1")
cmd("sudo sysctl -p")
interface  = os.popen('ip route list default').readlines()[0]
interface=interface[interface.find("dev"):interface.find("proto")].replace(" ","")

cmd("sudo ufw allow 1314/udp")
cmd("sudo systemctl enable wg-quick@wg0.service")
cmd("sudo systemctl start wg-quick@wg0.service")
cpk  = os.popen('wg genkey').readlines()[0]
ip=requests.get("https://ifconfig.me").content.decode("utf-8")
a='''
[Interface]
PrivateKey = '''+cpk+'''
Address = 10.8.0.2/24, fd0d:86fa:c3bc::2/64
DNS = 1.1.1.1

[Peer]
PublicKey = '''+sk+'''
AllowedIPs = 0.0.0.0/0, ::/0
Endpoint = '''+ip+''':1314
'''
cmd("sudo wg set wg0 peer "+cpk+" allowed-ips 10.8.0.2,fd0d:86fa:c3bc::2")
with open("client.conf","w") as f:
    f.write(a)

