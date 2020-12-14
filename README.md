# Talos


(Talos was developed on Ubuntu 18.04 in Python 3.6)

## Installation

This application was developed on Ubuntu 18.04 and is only supported on this platform for now. Get a Ubuntu 18.04 server and make sure you have no webservers (apache2, nginx and so on) installed/running on your server. 

Suggestion: *If you are running Windows 10, use WSL, open the microsoft store and install Ubuntu 18.04. Then open wsl as your terminal. The following steps should work just as well.*

### Automatic installation (Install Script)

You can choose to install Talos manually on your device, or you can use the following script:

```bash
source <(curl -s https://raw.githubusercontent.com/Holtder/Talos/master/installtalos.sh)
```

Please note: It is good practice not to trust install scripts like these out of the box, feel free to check out its [contents](https://github.com/Holtder/Talos/blob/master/installtalos.sh) before using the command above!

You can find talos at the address you chose during install in your preferred browser.

## Planned features

The following functions, features and files are to be implemented in the future:

* Autodeletion of jobs stuck in 'In progress' queue
* Workflow optimisation: If multiple jobs are started the database will overload, at the moment all jobs are queued after eachother. In the future I want to switch from a SQLite database to something more powerful, allowing concurrent task running. For now this'll do

## Acknowledgements

Github User and good friend [thijsmie](https://github.com/thijsmie) spared me some precious time from his thesis and helped a lot by providing feedback on basically everything, from which I learned a lot.

Github User [zenyui](https://https://github.com/zenyui) wrote a clear and concise [example](https://github.com/zenyui/celery-flask-factory) of how to properly implement both Flask and Celery in one app.
The Talos script [`appfactory.py`](https://github.com/Holtder/Talos/blob/master/talos/appfactory.py) is based on the example script [`core.py`](https://github.com/zenyui/celery-flask-factory/blob/master/server/core.py)
