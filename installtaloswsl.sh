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
echo " - Python3-wheel"
echo
echo "It will also install redis and nginx on your server. Make sure you have uninstalled any webservers beforehand!"
echo "Additionally, if you are running a fresh installation of WSL, make sure to first run sudo apt-get update."
echo "If you haven't run it, WSL will close"
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
sudo service redis-server start
redissuccess="$(sudo service redis-server status)"
if [ "$redissuccess" != " * redis-server is running" ]; then
    echo "Error: Redis failure*"
    exit 1
fi

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
rm "installtaloswsl.sh"
rm -rf ".git"
rm -f ".gitignore"
rm -f "README.md"

cwd=$(pwd)

echo "Creating virtual environment and installing Required Packages"

python3 -m venv .env || exit 1
pip3 install wheel || exit 1
source ".env/bin/activate" || exit 1
pip install wheel || exit 1
pip install -r "requirements.txt" || exit 1
rm -f "requirements.txt"
