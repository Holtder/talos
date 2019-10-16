These notes are still very much a WiP; it was developed on Ubuntu 18.04 in Python 3.6

# Install instructions:
Decide for youself if you want to install all required packages in a venv or not, all version requirements are listed in requirements.txt

* Play Scraper
* requests
* Flask
* Flask SQLAlchemy
* WT Forms


Make sure you have the following installed:

* Python 3.6
* Redis `sudo apt-get install redis-server`

# Before using
Start redis and celery from the terminal

* `$ redis-server`
* `$ celery -A talos.celery worker`

# Usage
Start the Flask Server 

`$ python3 run.py`

Or if you are using a virtual environment:

`$ source venvname/bin/activate && python run.py`


You can now find Talos on '127.0.0.1:5000' in your preferred browser.
