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

You can find talos at the address you chose during install in your preferred browser.

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
