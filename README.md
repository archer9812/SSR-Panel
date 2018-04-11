# SSR-Panel
A Beautiful Panel for SSR

## 项目说明 ##
本项目用于使用简洁的WEB进行管理ShadowsocksR程序，方便几个人用来科学上网。

## 搭建流程 ##
### SSR程序安装 ###
使用秋水逸冰的脚本进行安装（本程序对此版本进行了适配，其他版本可能存在问题）。脚本来源于 [秋水逸冰](https://teddysun.com/486.html)
```Shell
wget --no-check-certificate -O shadowsocks-all.sh https://raw.githubusercontent.com/teddysun/shadowsocks_install/master/shadowsocks-all.sh
chmod +x shadowsocks-all.sh
./shadowsocks-all.sh 2>&1 | tee shadowsocks-all.log
```
### SSR-Panel 安装 in Ubuntu ###
```PowerShell
apt-get update
apt-get -y install python3-pip
apt-get -y install zip
pip3 install --upgrade pip
wget https://github.com/archer9812/SSR-Panel/archive/master.zip
pip3 install flask
pip3 install flask_wtf
unzip master.zip
cd SSR-Panel-master
cp -f config/config.json /etc/shadowsocks-r/config.json
nohup python3 manage.py
```
