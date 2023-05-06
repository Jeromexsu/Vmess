domain=$1
port=$2
echo "domain=$domain, port=$port"
# allow http and https
echo "set firewall"
firewall-cmd --zone=public --add-service=http --add-service=https
firewall-cmd --zone=public --add-port=$port/tcp
# install nginx
echo "installing nginx"
yum -y install nginx 2>/dev/null >/dev/null
(curl https://raw.githubusercontent.com/Jeromexsu/Vmess/main/templates/server/nginx/nginx.conf  >/etc/nginx/nginx.conf) 2>/dev/null >/dev/null
(curl https://raw.githubusercontent.com/Jeromexsu/Vmess/main/templates/server/nginx/server80.conf | sed -e "s/~domain/$domain/g" >/etc/nginx/conf.d/server80.conf)
echo "conf for nginx: /etc/nginx/nginx.conf"
systemctl start nginx
echo "nginx started"

# ssl
(curl https://get.acme.sh | sh -s email=suchuanxj@gmail.com) 2>/dev/null >/dev/null
mkdir /etc/pki/nginx/
mkdir /etc/pki/nginx/private

echo "applying certificates"
.acme.sh/acme.sh --issue -d $domain --nginx 

echo "installing certificates"
.acme.sh/acme.sh --install-cert -d $domain --key-file /etc/pki/nginx/private/server.key --fullchain-file /etc/pki/nginx/server.crt >/dev/null

(curl https://raw.githubusercontent.com/Jeromexsu/Vmess/main/templates/server/nginx/server443.conf | sed -e "s/~domain/$domain/g" -e "s/~port/$port/" >/etc/nginx/conf.d/server443.conf)

# install v2ray
echo "installing v2ray"
(curl https://raw.githubusercontent.com/v2fly/fhs-install-v2ray/master/install-release.sh | bash) 2>/dev/null >/dev/null
(curl https://raw.githubusercontent.com/v2fly/fhs-install-v2ray/master/install-dat-release.sh| bash) 2>/dev/null >/dev/null
id=$(uuidgen)
echo "uuid for test client: $id"
(curl https://raw.githubusercontent.com/Jeromexsu/Vmess/main/templates/server/v2ray/conf.json | sed -e "s/~port/$port/" -e "s/~id/$id/" > /usr/local/etc/v2ray/config.json) 2>/dev/null >/dev/null
systemctl start v2ray
echo "v2ray started"

echo "install finished"

setenforce 0