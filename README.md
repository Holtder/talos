# Note to self, when developing on new device:
`$ pip3 install virtualenv`
`$ virtualenv --no-site-packages --distribute .env && source .env/bin/activate && pip install -r requirements.txt`

Next time:

`& source .env/bin/activate`

# AppStoreScraper
## Requirements
### Python Packages
Make sure you have Python (3.6.8) and pip3 installed. There are many tutorials online that do a far better job on how to accomplish this than I ever could. Once you get that done, install the following python packages:

* Play Scraper
* requests
* Flask
* Flask SQLAlchemy
* WT Forms 

You can install these all at the same time using either:

`$ pip3 install -r requirements.txt`

or 

`$ pip3 install play-scraper requests Flask Flask-SQLAlchemy WTForms`


### Redis
Besides python and the packages alongside it, you need a functioning Redis server running.

## Notes
This is still a work in progress, proper installation instructions will follow.
