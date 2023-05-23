pw=`< /dev/urandom tr -dc _A-Z-a-z-0-9 | head -c${1:-32};echo;`   
ip=`curl ifconfig.me`   
country=`curl -s 'ipinfo.io' | jq -r '.country'`
curl -o /tmp/link.py http://<SERVER-IP-AND-PORT-HERE>/getlink
rm -rf  /var/snap/shadowsocks-libev/common/etc/shadowsocks-libev/config.json 
rm -rf /etc/systemd/system/shadowsocks-libev-server@.service 
apt update
apt upgrade -y  
apt install -y snapd 
apt install -y haveged 
#apt install -y nginx
snap install shadowsocks-libev 
mkdir -p /var/snap/shadowsocks-libev/common/etc/shadowsocks-libev 
touch /var/snap/shadowsocks-libev/common/etc/shadowsocks-libev/config.json 
echo "{
   \"server\":[\"[::0]\", \"0.0.0.0\"],
   \"mode\":\"tcp_and_udp\",
   \"server_port\":3773,
   \"password\":\""$pw"\",
   \"timeout\":60,
   \"method\":\"chacha20-ietf-poly1305\",
   \"nameserver\":\"1.1.1.1\"
}" >> /var/snap/shadowsocks-libev/common/etc/shadowsocks-libev/config.json 
touch /etc/systemd/system/shadowsocks-libev-server@.service 
echo "
[Unit]
Description=Shadowsocks-Libev Custom Server Service for %I
Documentation=man:ss-server(1)
After=network-online.target

[Service]
Type=simple
ExecStart=/usr/bin/snap run shadowsocks-libev.ss-server -c /var/snap/shadowsocks-libev/common/etc/shadowsocks-libev/%i.json

[Install]
WantedBy=multi-user.target
" >>  /etc/systemd/system/shadowsocks-libev-server@.service 
systemctl enable --now shadowsocks-libev-server@config 
ufw allow 3773
sslink=`python3 /tmp/link.py`
curl -X POST http://<SERVER-IP-AND-PORT-HERE>/newserver -H "Content-Type: application/json" -d "{"pw":\""$pw"\", "ip":\""$ip"\","link":\""$sslink"\","country":\""$country"\"}"
echo "成功安装"
