domain=$1
port=$2

# install nginx
yum install nginx
curl https://raw.githubusercontent.com/Jeromexsu/Vmess/main/templates/server/nginx/nginx.conf | sed -e "s/~domain/jeromesu.com/" -e "s/~port/10053/" > /etc/nginx/conf/nginx.conf

# ssl
curl https://get.acme.sh | sh -s email=suchuanxj@gmail.com
acme.sh --issue -d $domain --nginx
mkdir /etc/pki/nginx/
mkdir /etc/pki/nginx/private
acme.sh --install-cert -d $domain --key-file /etc/pki/nginx/private/server.key --fullchain-file /etc/pki/nginx/server.crt

# install v2ray
bash <(curl -L https://raw.githubusercontent.com/v2fly/fhs-install-v2ray/master/install-release.sh)
bash <(curl -L https://raw.githubusercontent.com/v2fly/fhs-install-v2ray/master/install-dat-release.sh)
curl https://raw.githubusercontent.com/Jeromexsu/Vmess/main/templates/server/v2ray/conf.json | sed -e "s/~port/$port/" -e "s/~id/$(uuidgen)/" > /usr/local/etc/v2ray/config.json