# Talos


(These notes are still very much a WiP; Talos is being developed on WSL-Ubuntu 18.04 in Python 3.6)

## Installation

Make sure you have the following installed:

* A Linux distribution which supports the following:
  * Python 3.6, including pip3 and virtualenv

Suggestion: *If you are running Windows 10, use WSL, open the microsoft store and install Ubuntu 18.04. Then open wsl as your terminal. The following steps should work just as well.*

### Automatic installation (Install Script)

You can choose to install Talos manually on your device, or you can use the following script:

```bash
source <(curl -s https://raw.githubusercontent.com/Holtder/Talos/master/installtalos.sh)
```

Please note: It is good practice not to trust install scripts like these out of the box, feel free to check out its [contents](https://github.com/Holtder/Talos/blob/master/installtalos.sh) before using the command above!

### Manual install

#### Requirements

The following Terminal commands install required packages and write a clone in your specified location.

```bash
sudo apt-get install -y python3-pip python3-venv git
cd ~/to/your/preferred/location
git clone https://github.com/Holtder/Talos.git
cd Talos
```

#### Virtual environment

*Note: If you choose to skip this step the scripts to automatically start and stop Talos will be unusable and you have to do so manually!*

In order to prevent any problems with python versions or packages, it is recommended to use a virtual environment for python 3.6.8.\
`python3 -m venv .env`

To activate the environment, use `source`:\
`source .env/bin/activate`

#### Dependencies

The following packages are used in Talos:

* Play Scraper
* Flask
* Flask-WTF
* Flask-SQLAlchemy
* Celery
* Redis

Install them with the following command (if you chose to not use  a virtual environment, use `pip3` instead of `pip`):\
`$ pip install -r requirements`

#### Finishing touches

Make the script that starts Talos executable:\
chmod a+x talos.sh

Remove the automatic installscript:\
rm installscript.sh

## Usage

### Start and stop scripts

A planned feature is to provide the user with scripts to start and stop the server. For now you will be required to use the manual method.

### Starting the server manually

Start redis from the terminal

```bash
redis-server --daemonize yes
```
  
Then open two terminals in the virtual environment (`$ source .env/bin/activate`) and run the two python scripts separately (if you chose to not use  a virtual environment, use `python3` instead of `python`). You can see if you are in a virtual environment if your usual `username@hostname`: is preceded by `(.env)`

Terminal 1:

```bash
celery -A entrypoint_celery.celery worker --concurrency=1
```

Terminal 2:

```bash
FLASK_APP=entrypoint_app.py flask run
```

You can now find Talos at [`127.0.0.1:5000`](http://127.0.0.1:5000) in your preferred browser.

## Planned features

The following functions, features and files are to be implemented in the future:

* Docker packaging, which should remove the need for the aforementioned installrequirements and instructions
* Serving a webserver with Flask (using g-unicorn & nginx)
  * Alongside this a privacy policy, as search queries are stored for functional reasons
    * Due to privacy reasons, the publicly hosted version of Talos will delete all queries older than 24h
* Autodeletion of jobs stuck in 'In progress' queue
* Workflow optimisation: If multiple jobs are started the database will overload, at the moment all jobs are queued after eachother. In the future I want to switch from a SQLite database to something more powerful, allowing concurrent task running. For now this'll do

## Acknowledgements

Github User and good friend [thijsmie](https://github.com/thijsmie) spared me some precious time from his thesis and helped a lot by providing feedback on basically everything, from which I learned a lot.

Github User [zenyui](https://https://github.com/zenyui) wrote a clear and concise [example](https://github.com/zenyui/celery-flask-factory) of how to properly implement both Flask and Celery in one app.
The Talos script [`appfactory.py`](https://github.com/Holtder/Talos/blob/master/talos/appfactory.py) is based on the example script [`core.py`](https://github.com/zenyui/celery-flask-factory/blob/master/server/core.py)
