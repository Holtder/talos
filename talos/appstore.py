import requests
import play_scraper
import enum
from datetime import datetime
from .consts import illegal_desc, illegal_price, android_key_list, apple_key_list, keysDict


class appresult:
    class Source(enum.Enum):
        Android = 0
        Apple = 1
        Database = 2
    """ Each instance of this object represents one result from the app-store queries
    Both APIs return a range of data but the variables used here are the ones that are returned by both
    """
    def __init__(self, source, **kwargs):
        """
        Because the list of given arguments is variable, this code crossreferences the arguments
        With a list of appstore-specific arguments. Based on that, a non-specific key is assigned to the value.
        That way the rest of the code can run universally.
        i represents the appstore (0: android, 1: apple)
        """
        i = 0
        kwargDict = {}
        if source == self.Source.Android:
            self.store = 'android'
            i = 0
        elif source == self.Source.Apple:
            self.store = 'apple'
            i = 1
        elif source == self.Source.Database:
            i = 2

        for key, value in kwargs.items():
            if key in keysDict[i]:
                kwargDict[keysDict[i][key]] = value

        if i == 2:
            self.store = kwargDict['store']

        self.app_title = kwargDict['app_title']
        self.bundleid = kwargDict['bundleid']
        self.dev_id = str(kwargDict['dev_id'])
        self.versionnumber = kwargDict['versionnumber']
        self.osreq = kwargDict['osreq']
        self.content_rating = kwargDict['content_rating']

        """
        Dev name formatting: in some languages there is no dev name, only an ID
        In that case, it gets defaulted to 'Google Commerce Ltd', which will be converted to n/a
        But only if the dev ID is not google's
        """
        self.dev_name = kwargDict['dev_name']
        if (self.dev_id != "5700313618786177705") and (self.dev_name == 'Google Commerce Ltd'):
            self.dev_name = "N/A"

        # Description formatting
        self.description = kwargDict['description']
        if self.description is None:
            self.description = ''
        for c, v in illegal_desc:
            self.description = self.description.replace(c, v)

        # Price formatting to cents
        self.fullprice = str(kwargDict['fullprice'])
        if (self.fullprice is None) or (self.fullprice == "") or str(self.fullprice) == "0":
            self.fullprice = "00"
        for c in illegal_price:
            self.fullprice = self.fullprice.replace(c, '')
        self.fullprice = self.fullprice.strip()

        self.latest_patch = kwargDict['latest_patch']
        if source != self.Source.Database:
            if self.latest_patch is not None:
                if self.store == "android":
                    # Example: June 3, 2019 to 2019-06-03
                    self.latest_patch = datetime.strptime(self.latest_patch, "%B %d, %Y")
                elif self.store == "apple":
                    # Example: 2014-07-15T15:08:56Z to 2014-07-15
                    self.latest_patch = datetime.strptime(self.latest_patch[0:10], "%Y-%m-%d")
            else:
                self.latest_patch = datetime.strptime("1808-08-08", "%Y-%m-%d")

    def dict(self):
        resultsDict = {
            'app_title': self.app_title,
            'bundleid': self.bundleid,
            'store': self.store,
            'description': self.description,
            'dev_name': self.dev_name,
            'dev_id': self.dev_id,
            'fullprice': self.fullprice,
            'versionnumber': self.versionnumber,
            'osreq': self.osreq,
            'latest_patch': self.latest_patch,
            'content_rating': self.content_rating
        }
        return resultsDict


def android_search(searchquery, country_code='nl', pagerange=13):
    """ Android Search Query, using the play-scraper package """
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
                newapp = appresult(appresult.Source.Android, **memb)
                total += 1
                results.append(newapp)

        else:
            break

    print('Android total: %s' % total)
    return results


def apple_search(searchquery, country_code='nl'):
    """ Apple Search Query, using the official iTunes API """
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

            newapp = appresult(appresult.Source.Android, **memb)
            total += 1
            results.append(newapp)

    print('Apple total:%s' % total)
    return results


def search_appstores(arg_searchterm, arg_country):
    """ Using consts may seem redundant, but this allows one output to be applied differently where necessary
    This way there is room for the addition of other languages without adding too much work
    """

    results = android_search(arg_searchterm, arg_country, 1)
    results += apple_search(arg_searchterm, arg_country)
    return results
