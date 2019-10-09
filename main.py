import csv
import APIfunctions
import itertools
from consts import *

arg_searchterm = "infection"
arg_country = "us"
arg_language = "en"

# Using consts may seem redundant, but this allows one output to be applied differently where necessary
# This way there is room for the addition of other languages without adding too much work
androidResults = APIfunctions.android_search(arg_searchterm, arg_country, android_language_codes[arg_language])
appleResults = APIfunctions.apple_search(arg_searchterm, arg_country, apple_language_codes[arg_language])


with open('test.csv', 'w') as f:
	f.write("app_title;store;bundleid;description;dev_name;dev_id;fullprice;versionnumber;osreq;latest_patch;content_rating\n")
	for app in itertools.chain(androidResults, appleResults):
		f.write("%s;" % (app.app_title))
		f.write("%s;" % (app.store))
		f.write("%s;" % (app.bundleid))
		f.write("%s;" % (app.description))
		f.write("%s;" % (app.dev_name))
		f.write("%s;" % (app.dev_id))
		f.write("%s;" % (app.fullprice))
		f.write("%s;" % (app.versionnumber))
		f.write("%s;" % (app.osreq))
		f.write("%s;" % (app.latest_patch))
		f.write("%s" % (app.content_rating))
		f.write("\n")
