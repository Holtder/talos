import requests
import play_scraper
import os
import csv
from datetime import datetime
from talos.consts import illegal_desc, illegal_price, android_key_list, apple_key_list

class appresult:
    # Each instance of this object represents one result from the app-store queries
    # Both APIs return a range of data but the variables used here are the ones that are returned by both
    def __init__(self, app_title, store, bundleid, description, dev_name, dev_id, fullprice, versionnumber, osreq, latest_patch, content_rating):
        self.app_title = app_title
        self.store = store
        self.bundleid = bundleid
        self.dev_id = str(dev_id)
        self.versionnumber = versionnumber
        self.osreq = osreq
        self.content_rating = content_rating

        # Dev name formatting: in some languages there is no dev name, only an ID
        # In that case, it gets defaulted to 'Google Commerce Ltd', which will be converted to n/a
        # But only if the dev ID is not google's
        self.dev_name = dev_name
        if (self.dev_id != "5700313618786177705") and (self.dev_name == 'Google Commerce Ltd'):
            self.dev_name = "N/A"

        # Description formatting
        self.description = description
        if self.description is None:
            self.description = ''
        for c, v in illegal_desc:
            self.description = self.description.replace(c, v)

        # Price formatting to cents
        self.fullprice = str(fullprice)
        if (self.fullprice is None) or (self.fullprice == "") or str(self.fullprice) == "0":
            self.fullprice = "00"
        for c in illegal_price:
            self.fullprice = self.fullprice.replace(c, '')
        self.fullprice = self.fullprice.strip()

        # Formatting the date of the most recent patch
        self.latest_patch = latest_patch
        if self.latest_patch is not None:
            if self.store == "android":
                # Example: June 3, 2019 to 2019-06-03
                self.latest_patch = datetime.strptime(self.latest_patch, "%B %d, %Y")
            elif self.store == "apple":
                # Example: 2014-07-15T15:08:56Z to 2014-07-15
                self.latest_patch = datetime.strptime(self.latest_patch[0:10], "%Y-%m-%d")
        else:
            self.latest_patch = datetime.strptime("1808-08-08", "%Y-%m-%d")


def android_search(searchquery, country_code='nl', pagerange=13):
    # Android Search Query, using the play-scraper package
    results = []
    total = 0

    # As the play-scraper search functions per page, iteration (with a max of 13) is required
    for i in range(0, pagerange):
        response = play_scraper.search(
            searchquery, i, True, 'en', country_code)

        # If the size of the page is 0, ergo when it is empty, break off the loop
        if not len(response) == 0:
            for memb in response:
                for keymemb in android_key_list:
                    if keymemb not in memb:
                        memb[keymemb] = ''
                newapp = appresult(memb['title'], 'android', memb['app_id'], memb['description'], memb['developer'], memb['developer_id'],
                                   memb['price'], memb['current_version'], memb['required_android_version'], memb['updated'], memb['content_rating'])
                total += 1
                results.append(newapp)

        else:
            break

    print('Android total: %s' % total)
    return results


def apple_search(searchquery, country_code='nl'):
    # Apple Search Query, using the official iTunes API
    results = []
    total = 0
    i = 0

    # Two variables nessecary in the construction of the final request-URL
    url_endpoint = 'http://ax.itunes.apple.com/WebObjects/MZStoreServices.woa/wa/wsSearch'
    search_params = {'country': country_code, 'lang': 'en-US',
                     'media': 'software', 'limit': 200, 'offset': 0, 'term': searchquery}

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
            for keymemb in apple_key_list:
                if keymemb not in memb:
                    memb[keymemb] = ''

            newapp = appresult(memb['trackName'], 'apple', memb['bundleId'], memb['description'], memb['artistName'], memb['artistId'],
                               memb['price'], memb['version'], memb['minimumOsVersion'], memb['currentVersionReleaseDate'], memb['trackContentRating'])
            total += 1
            results.append(newapp)

    print('Apple total:%s' % total)
    return results

def search_appstores(arg_searchterm, arg_country):
    # Using consts may seem redundant, but this allows one output to be applied differently where necessary
    # This way there is room for the addition of other languages without adding too much work

    results = android_search(arg_searchterm, arg_country, 1)
    results += apple_search(arg_searchterm, arg_country)
    return results


# Function that exports a collection of appresult instances and allows for optional name specification
def export_csv(app_list, filename="output"):
    dirName = 'talos/static/output/'

    # Create target directory if doesn't exist yet
    if not os.path.exists(dirName):
        os.makedirs(dirName)
        print("Directory ", dirName, " Created ")
    else:
        print("Directory ", dirName, " already exists")

    # Actual exportation, overwrites the file if it exists
    with open(f'{dirName}/{filename}.csv', 'w') as f:
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
            f.write("%s;" % (app.latest_patch.date()))
            f.write("%s" % (app.content_rating))
            f.write("\n")
