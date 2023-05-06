domain=$1
port=$2

# install nginx
yum install nginx
sed -i e "s/~domain/$domain/" ../templates/server/nginx/nginx1.conf
sed -i e "s/~port/$port/" ../templates/server/nginx/nginx.conf

# ssl
curl https://get.acme.sh | sh -s email=suchuanxj@gmail.com
acme.sh --issue -d $domain --nginx
mkdir /etc/pki/nginx/
mkdir /etc/pki/nginx/private
acme.sh --install-cert -d $domain --key-file /etc/pki/nginx/private/server.key --fullchain-file /etc/pki/nginx/server.crt

# install v2ray
bash <(curl -L https://raw.githubusercontent.com/v2fly/fhs-install-v2ray/master/install-release.sh)
bash <(curl -L https://raw.githubusercontent.com/v2fly/fhs-install-v2ray/master/install-dat-release.sh)
curl https://raw.githubusercontent.com/Jeromexsu/Vmess/main/templates/server/v2ray/conf.json > /usr/local/etc/v2ray/config.json
sed -i e "s/~port/$port/" ../templates/server/v2ray/conf.json
sed -i e "s/~id/$(uuidgen)/" ../templates/server/v2ray/conf.json


firewall-cmd --zone=public --add-port=10053
setenforce 0