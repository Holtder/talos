#!/bin/bash
pyv="$(python3 -V 2>&1)"
pyv="${pyv:7:5}"
if [ "$pyv" != "3.6.8" ]; then
    echo "Error: Requires Python 3.6.8"
    exit 1
fi

echo "Warning!"
echo "This script will attempt to install the following packages:"
echo " - Git"
echo " - Python3-pip"
echo " - Python3-venv"
echo 
while true; do
    read -p "Is this ok? (Y/N)" yn
    case $yn in
        [Yy]* ) sudo apt-get install -qq python3-pip python3-venv git; break;;
        [Nn]* ) echo "Exiting Talos installer"; exit;;
        * ) echo "Please answer yes or no. (Y/N)";;
    esac
done

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

cd "Talos"

rm "installtalos.sh"
rm -rf ".git"

python3 -m venv .env || exit 1
source ".env/bin/activate" || exit 1
pip install -r "requirements.txt" || exit 1