# Talos
*Talos was developed on Ubuntu 18.04 in Python 3.6*

## About
Talos is a self-hosted web-based search engine that allows the user to gather a list of apps available on the Apple and Google Play app stores. It allows region specification and the export of gathered data to .CSV files.

## Installation
A step-by-step guide on how to install and run Talos can be found on https://holtder.github.io/talos/.

You can find talos at the address you chose during install in your preferred browser.

## Planned features

The following functions, features, fixes and files are to be implemented in the future:

* Autodeletion of jobs stuck in 'In progress' queue
* Workflow optimisation: If multiple jobs are started the database will overload, at the moment all jobs are queued one after eachother. In the future I want to switch from a SQLite database to something more powerful, allowing concurrent task running. For now this'll do

## Acknowledgements
Github User and good friend [thijsmie](https://github.com/thijsmie) spared me some precious time from his thesis and helped a lot by providing feedback on basically everything, from which I learned a lot.

Github User [zenyui](https://https://github.com/zenyui) wrote a clear and concise [example](https://github.com/zenyui/celery-flask-factory) of how to properly implement both Flask and Celery in one app.
The Talos script [`appfactory.py`](https://github.com/Holtder/Talos/blob/master/talos/appfactory.py) is based on the example script [`core.py`](https://github.com/zenyui/celery-flask-factory/blob/master/server/core.py)
