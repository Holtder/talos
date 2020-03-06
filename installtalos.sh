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
echo " - Python3-wheel
echo
echo "It will also install redis and nginx on your server. Make sure you have uninstalled any webservers beforehand!"
echo
while true; do
    read -p "Is this ok? (Y/N)" yn
    case $yn in
        [Yy]* ) sudo apt-get install -qq python3-pip python3-venv python3-wheel redis-server git nginx || exit 1; break;;
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
rm -f ".gitignore"
rm -f "README.md"

cwd=$(pwd)

echo "Creating virtual environment and installing Required Packages"

python3 -m venv .env || exit 1
source ".env/bin/activate" || exit 1
pip install -r "requirements.txt" || exit 1
rm -f "requirements.txt"

echo "Stopping and deleting old Talos services if present"
sudo systemctl stop talos
sudo systemctl disable talos
sudo rm -f /etc/systemd/system/talos.service
sudo rm -f /etc/systemd/system/talos.service
sudo systemctl daemon-reload
sudo systemctl reset-failed

echo "Creating service"

sudo bash -c 'cat > /etc/systemd/system/talos.service' << EOT
#Metadata and dependencies section
[Unit]
Description=Talos service
After=network.target
#Define users and app working directory
[Service]
User=$USER
Group=www-data
WorkingDirectory=$cwd
Environment="PATH=$cwd/.env/bin"
ExecStart=$cwd/.env/bin/uwsgi --ini $cwd/talos.ini
#Link the service to start on multi-user system up
[Install]
WantedBy=multi-user.target
EOT

sudo systemctl daemon-reload

echo "Generating supervisord config"
sudo unlink /tmp/supervisor.sock
rm -f supervisord.conf
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

echo "Starting Talos and supervisord daemons"
sudo systemctl start talos
sudo systemctl enable talos
supervisord
supervisorctl restart celeryd

echo "Configuring nginx"
echo "What is the address (domain or ip) you intend to serve Talos from [default=0.0.0.0]:"
read -e -i "0.0.0.0" hostedaddress
sudo rm -f /etc/nginx/sites-available/talos
sudo rm -f /etc/nginx/sites-enabled/talos

sudo bash -c 'cat > /etc/nginx/sites-available/talos' << EOT
server {
    # the port your site will be served on
    listen 80;
    # the IP Address your site will be served on
    server_name $hostedaddress;
    # Proxy connections to application server
    location / {
        include uwsgi_params;
        uwsgi_pass unix:/tmp/talos.sock;
    }
}
EOT

sudo ln -s /etc/nginx/sites-available/talos /etc/nginx/sites-enabled

echo "Reloading nginx config and restarting nginx"
sudo nginx -t
sudo systemctl restart nginx

