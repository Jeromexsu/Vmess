# install v2ray
bash <(curl -L https://raw.githubusercontent.com/v2fly/fhs-install-v2ray/master/install-release.sh)
bash <(curl -L https://raw.githubusercontent.com/v2fly/fhs-install-v2ray/master/install-dat-release.sh)
vim /usr/local/etc/v2ray/config.json

yum install nginx

curl https://get.acme.sh | sh -s email=suchuanxj@gmail.com
acme.sh --issue -d jeromesu.com --nginx
mkdir /etc/pki/nginx/
mkdir /etc/pki/nginx/private
acme.sh --install-cert -d jeromesu.com --key-file /etc/pki/nginx/private/server.key --fullchain-file /etc/pki/nginx/server.crt

firewall-cmd --zone=public --add-port=10053
setenforce 0