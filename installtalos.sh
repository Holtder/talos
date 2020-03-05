#!/bin/bash
pyv="$(python3 -V 2>&1)"
pyv="${pyv:7:3}"
if [ "$pyv" != "3.6" ]; then
    echo "Error: Requires Python 3.6.*"
    exit 1
fi

echo "Warning!"
echo "This script will attempt to install the following packages:"
echo " - Git"
echo " - Python3-pip"
echo " - Python3-venv"
echo
echo
echo "It will also install redis and nginx on your server. Make sure you have uninstalled any webservers beforehand!"
echo
while true; do
    read -p "Is this ok? (Y/N)" yn
    case $yn in
        [Yy]* ) sudo apt-get install -qq python3-pip python3-venv redis-server git nginx || exit 1; break;;
        [Nn]* ) echo "Exiting Talos installer"; exit;;
        * ) echo "Please answer yes or no. (Y/N)";;
    esac
done

echo "Enabling redis service"
sudo systemctl enable redis-server.service
sudo systemctl start redis-server.service

echo
echo
echo "Warning!"
echo
echo "This script will create a Talos directory at the location of the installscript"
echo "If a Talos installation is already present, it will be deleted!"
echo "If this is not what you want, decline this prompt, move the script to your preferred location and run it again."
echo "Current Installation Directory: $PWD/Talos"
echo
while true; do
    read -p "Is this ok? (Y/N)" yn
    case $yn in
        [Yy]* ) break;;
        [Nn]* ) echo "Exiting Talos installer"; exit;;
        * ) echo "Please answer yes or no. (Y/N)";;
    esac
done

rm -rf "Talos"
git clone -q https://github.com/Holtder/Talos.git || exit 1

cd "Talos" || exit 1

rm "installtalos.sh"
rm -rf ".git"

cwd=$(pwd)

echo "Creating virtual environment and installing Required Packages"

python3 -m venv .env || exit 1
source ".env/bin/activate" || exit 1
pip install -r "requirements.txt" || exit 1

echo "Starting Redis"
redis-server || exit 1

echo "Creating service"
sudo rm -f /etc/systemd/system/talos.service || exit 1
sudo cat <<EOT >> /etc/systemd/system/talos.service
#Metadata and dependencies section
[Unit]
Description=Talos service
After=network.target
#Define users and app working directory
[Service]
User=$USER
Group=www-data
WorkingDent==$cwd
Environment="PATH=$cwd/.env/bin"
ExecStart=$cwd/.env/bin/uwsgi --ini talos.ini
#Link the service to start on multi-user system up
[Install]
WantedBy=multi-user.target
EOT


echo "Generating supervisord config"
rm -f supervisord.conf || exit 1
echo_supervisord_conf > $cwd/supervisord.conf
cat <<EOT >> $cwd/supervisord.conf
[program:celeryd]
command=$cwd/.env/bin/celery -A entrypoint_celery.celery worker --concurrency=1
stdout_logfile=$cwd/celeryd.log
stderr_logfile=$cwd/celeryd.log
autostart=true
autorestart=true
startsecs=10
stopwaitsecs=600
EOT


sudo systemctl start talos
sudo systemctl enable talos
supervisord

echo "Configuring nginx"

echo "What is the address (domain or ip) you intend to serve Talos from [default=0.0.0.0]:"

read -e -i "0.0.0.0" hostedaddress

sudo rm -f /etc/nginx/sites-available/talos
sudo rm -f /etc/nginx/sites-enabled/talos

sudo cat <<EOT >> /etc/nginx/sites-available/talos
server {
    # the port your site will be served on
    listen 80;
    # the IP Address your site will be served on
    server_name $hostedaddress;
    # Proxy connections to application server
    location / {
        include uwsgi_params;
        uwsgi_pass unix:$cwd/talos.sock;
    }
}
EOT

sudo ln -s /etc/nginx/sites-available/talos /etc/nginx/sites-enabled

echo "Reloading nginx config and restarting nginx"
sudo ngnix -t
sudo systemctl restart nginx

