#!/bin/bash
pyv="$(python3 -V 2>&1)"
pyv="${pyv:7:3}"
if [ "$pyv" != "3.6" ]; then
    echo "Error: Requires Python 3.6.*"
    exit 1
fi

cd ~
if [ -f "Talos/celeryd.pid" ] 
    then
        echo "Celery was not shut down correctly last time, closing now."
        kill -9 `cat Talos/celeryd.pid`
        rm -f Talos/celeryd.pid
fi

# trap ctrl-c and call ctrl_c()
trap ctrl_c INT
function ctrl_c() {
        echo "** Closing Talos"
        if [ -f "Talos/celeryd.pid" ] 
            then
                cd ~
                echo "Killing celery"
                kill -9 `cat Talos/celeryd.pid`
                rm -f Talos/celeryd.pid
        fi
}
CHOICE=0
PS3='What do you wish to do?'
options=("(re)Install Talos" "Start Talos Server" "Quit")
select opt in "${options[@]}"
do
    case $opt in
        "(re)Install Talos")
            CHOICE=1
            break
            ;;
        "Start Talos Server")
            CHOICE=2
            break
            ;;
        "Quit")
            break
            ;;
        *) echo "invalid option $REPLY";;
    esac
done

clear
case $CHOICE in
        1)
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

            mv "installtaloswsl.sh" "../talos.sh"
            chmod +x ../talos.sh
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

            deactivate
            cd ~

            echo "Talos is now installed!"
            echo "Run talos with the following command:"
            echo "./talos.sh"
            ;;
        2)
            cd Talos
            source .env/bin/activate
            celery -A entrypoint_celery.celery worker --concurrency=1 --detach
            python entrypoint_app.py;;
        3)
            exit 1;;
esac

