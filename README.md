These notes are still very much a WiP; it was developed on Ubuntu 18.04 in Python 3.6

# Installation
## Install Script
You can choose to install Talos manually on your device, or you can use the following script:\
(note to self, when the installscript is done, add it here)
```bash
wget scriptwildcard.sh
chmod a+x scriptwildcard.sh
./scriptwildcard.sh
```

## Manual install
### Requirements
Make sure you have the following installed:
* Python 3.6, including pip3 and virtualenv
* Git
* A clone of the Talos repository

```bash
$ sudo apt-get install -y python3-pip python3-venv git
$ cd ~/to/your/preferred/location
$ git clone https://github.com/Holtder/Talos.git
$ cd Talos
```

### Virtual environment
In order to prevent any problems with python versions or packages, it is recommended to use a virtual environment for python 3.6.8.\
`$ python3 -m venv .env`

To activate the environment, use `source`:\
`$ source .env/bin/activate`

### Dependencies
The following packages are used in Talos:
* Play Scraper
* Flask
* Flask-WTF
* Flask-SQLAlchemy
* Celery
* Redis

Install them with the following command (if you chose to not use  a virtual environment, use `pip3` instead of `pip`):\
`$ pip install -r requirements`


# Usage
## Start and stop scripts
A planned feature is to provide the user with scripts to start and stop the server. For now you will be required to use the manual method.

## Starting the server manually
Start redis from the terminal
```bash
$ redis-server --daemonize yes
```
  
Then open two terminals in the virtual environment (`$ source .env/bin/activate`) and run the two python scripts separately (if you chose to not use  a virtual environment, use `python3` instead of `python`)

Terminal 1:
```bash
$ celery -A entrypoint_celery.celery worker
```
Terminal 2:
```bash
$ python entrypoiny_app.py
```

You can now find Talos at [`127.0.0.1:5000`](http://127.0.0.1:5000) in your preferred browser.


# Notes
The following functions are to be implemented in the future:
* Docker packaging, which should remove the need for the aforementioned installrequirements and instructions
* Serving a webserver with Flask (using g-unicorn & nginx)

# Aknowledgements
Github User [zenyui](https://https://github.com/zenyui) wrote a clear and concise [example](https://github.com/zenyui/celery-flask-factory) of how to properly implement both Flask and Celery in one app. 
The Talos script [`appfactory.py`](https://github.com/Holtder/Talos/blob/master/talos/appfactory.py) is based on the example script [`core.py`](https://github.com/zenyui/celery-flask-factory/blob/master/server/core.py) 