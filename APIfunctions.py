# Due to an unfortunate incident with Sharepoint all comments were lost, Currently in the process of rewriting them
import play_scraper
import requests
import time
import os
import csv
import json
import consts

# Each instance of this object represents one result from the app-store queries
# Both APIs return a range of data but the variables used here are the ones that are returned by both
class appresult:
    def __init__(self, app_title, store, bundleid, description, dev_name, dev_id, fullprice, versionnumber, osreq, latest_patch, content_rating):
        self.app_title = app_title
        self.store = store
        self.bundleid = bundleid
        self.description = description
        self.dev_name = dev_name
        self.dev_id = dev_id
        self.fullprice = fullprice
        self.versionnumber = versionnumber
        self.osreq = osreq
        self.latest_patch = latest_patch
        self.content_rating = content_rating


# A cleanup function which creates any description if not already present
# Then it iterates over all functions to remove any illegal character which disrupt the CSV
def description_cleanup(results):
    for app in results:
        if app.description == None:
            app.description = ''
        app.description = app.description.replace('\r', '')
        app.description = app.description.replace('\n', '')
        app.description = app.description.replace(';', ',')
    return results

# Android Search Query, using the play-scraper package
def android_search(searchquery, country_code='nl', language_code='nl', pagerange=13):
    results = []
    total = 0

    # As the play-scraper search functions per page, iteration (with a max of 13) is required
    for i in range(0, pagerange):
        response = play_scraper.search(
            searchquery, i, True, language_code, country_code)

        # If the size of the page is 0, ergo when it is empty, break off the loop
        if not len(response) == 0:
            for memb in response:
                for keymemb in consts.android_key_list:
                    if keymemb not in memb:
                        memb[keymemb] = ''
                newapp = appresult(memb['title'], 'android', memb['app_id'], memb['description'], memb['developer'], memb['developer_id'],
                                   memb['price'], memb['current_version'], memb['required_android_version'], memb['updated'], memb['content_rating'])
                total += 1
                results.append(newapp)

        else:
            print('break')
            break

    print('Android total: %s' % total)
    results = description_cleanup(results)
    return results

# Apple Search Query, using the official iTunes API
def apple_search(searchquery, country_code='nl', language_code='nl_nl'):
    results = []
    total = 0
    i = 0

    # Two variables nessecary in the construction of the final request-URL
    url_endpoint = 'http://ax.itunes.apple.com/WebObjects/MZStoreServices.woa/wa/wsSearch'
    search_params = {'country': country_code,  'lang': language_code,
                     'media': 'software',  'limit': 200,  'offset': 0,  'term': searchquery}

    # The iTunes API functions with pages as well, the size of one 'page' is set using the limit
    # paramater in search_params. The offset is to set the starting position of the query
    # limit:200 and offset:0 => first 200 results, limit:200 and offset:200 => second set of results
    # limit has a max of 200
    while i > -1:
        search_params['offset'] = 200 * i
        response = requests.get(url_endpoint, params=search_params).json()
        # if the resultcount is less than 200, this is the last page
        i = -1 if response['resultCount'] < 200 else i + 1
        for memb in response['results']:
            for keymemb in consts.apple_key_list:
                if keymemb not in memb:
                    memb[keymemb] = ''

            newapp = appresult(memb['trackName'], 'apple', memb['bundleId'], memb['description'], memb['artistName'], memb['artistId'],
                               memb['price'], memb['version'], memb['minimumOsVersion'], memb['currentVersionReleaseDate'], memb['trackContentRating'])
            total += 1
            results.append(newapp)

    print('Apple total:%s' % total)
    results = description_cleanup(results)
    return results

def search_both_stores(arg_searchterm, arg_country, arg_language):
    # Using consts may seem redundant, but this allows one output to be applied differently where necessary
    # This way there is room for the addition of other languages without adding too much work

    results = android_search(arg_searchterm, arg_country, consts.android_language_codes[arg_language], 1)
    results += apple_search(arg_searchterm, arg_country, consts.apple_language_codes[arg_language])
    return results


# Function that exports a collection of appresult instances and allows for optional name specification
def export_csv(app_list, filename="output"):
    dirName = 'output'

    # Create target directory if doesn't exist yet
    if not os.path.exists(dirName):
        os.mkdir(dirName)
        print("Directory ", dirName,  " Created ")
    else:
        print("Directory ", dirName,  " already exists")

    # Actual exportation, overwrites the file if it exists
    with open('output/%s.csv' % (filename), 'w') as f:
        f.write("bundleid;store;app_title;description;dev_name;dev_id;fullprice;versionnumber;osreq;latest_patch;content_rating\n")
        for app in app_list:
            f.write("%s;" % (app.bundleid))
            f.write("%s;" % (app.store))
            f.write("%s;" % (app.app_title))
            f.write("%s;" % (app.description))
            f.write("%s;" % (app.dev_name))
            f.write("%s;" % (app.dev_id))
            f.write("%s;" % (app.fullprice))
            f.write("%s;" % (app.versionnumber))
            f.write("%s;" % (app.osreq))
            f.write("%s;" % (app.latest_patch))
            f.write("%s" % (app.content_rating))
            f.write("\n")
