domain=$1
port=$2
echo "domain=$domain, port=$port"
# install nginx
echo "installing nginx"
yum -y install nginx 2>/dev/null >/dev/null
(curl https://raw.githubusercontent.com/Jeromexsu/Vmess/main/templates/server/nginx/nginx.conf | sed -e "s/~domain/jeromesu.com/g" -e "s/~port/10053/" >/etc/nginx/nginx.conf) 2>/dev/null >/dev/null
echo "conf for nginx: /etc/nginx/nginx.conf"

# ssl
(curl https://get.acme.sh | sh -s email=suchuanxj@gmail.com) 2>/dev/null >/dev/null
echo "applying certificates"
.acme.sh/acme.sh --issue -d $domain --nginx 2>/dev/null >/dev/null
mkdir /etc/pki/nginx/
mkdir /etc/pki/nginx/private
echo "installing certificates"
acme.sh --install-cert -d $domain --key-file /etc/pki/nginx/private/server.key --fullchain-file /etc/pki/nginx/server.crt 2>/dev/null >/dev/null

# install v2ray
echo "installing v2ray"
(curl https://raw.githubusercontent.com/v2fly/fhs-install-v2ray/master/install-release.sh | bash) 2>/dev/null >/dev/null
(curl https://raw.githubusercontent.com/v2fly/fhs-install-v2ray/master/install-dat-release.sh| bash) 2>/dev/null >/dev/null
id=$(uuidgen)
echo "uuid for test client: $id"
(curl https://raw.githubusercontent.com/Jeromexsu/Vmess/main/templates/server/v2ray/conf.json | sed -e "s/~port/$port/" -e "s/~id/$id/" > /usr/local/etc/v2ray/config.json) 2>/dev/null >/dev/null
