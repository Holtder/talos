import requests
import play_scraper
import enum
from datetime import datetime
from .consts import keysDict, illegal_price


class appResult:
    """
    Each instance of this object represents one result from the app-store
    queries. Both APIs return a range of data but the variables used here
    are the ones that are returned by both.
    """

    class Source(enum.Enum):
        Android = 0
        Apple = 1
        Database = 2

    def __init__(self, source, **kwargs):
        """
        Because the list of given arguments is variable, this code
        crossreferences the arguments with a list of appstore-specific
        arguments. Based on that, a non-specific key is assigned to the value.
        That way the rest of the code can run universally.
        """

        kwargDict = {}
        for key, value in kwargs.items():
            if key in keysDict[source.value]:
                kwargDict[keysDict[source.value][key]] = value

        if source == self.Source.Android:
            self.store = 'android'
        elif source == self.Source.Apple:
            self.store = 'apple'
        elif source == self.Source.Database:
            self.store = kwargDict['store']

        self.app_title = kwargDict['app_title']
        self.bundleid = kwargDict['bundleid']
        self.dev_id = str(kwargDict['dev_id'])
        self.versionnumber = kwargDict['versionnumber']
        self.osreq = kwargDict['osreq']
        self.content_rating = kwargDict['content_rating']

        """
        Dev name formatting: in some languages there is no dev name, only
        an ID. In that case, it gets defaulted to 'Google Commerce Ltd',
        which will be converted to n/a. But only if the dev ID is not google's
        """
        self.dev_name = kwargDict['dev_name']
        if (self.dev_id != "5700313618786177705") and (self.dev_name == 'Google Commerce Ltd'):
            self.dev_name = "N/A"

        self.description = kwargDict.get('description', '')

        # Price formatting to cents
        price = str(kwargDict.get("fullprice", "00")).strip()
        if price == "" or price == "None" or price == "0":
            price = "00"
        for c in illegal_price:
            price = price.replace(c, '')
        self.fullprice = price.strip()

        self.latest_patch = kwargDict.get(
            'latest_patch', datetime.strptime("1808-08-08", "%Y-%m-%d"))
        if source != self.Source.Database:
            if self.latest_patch is not None:
                if self.store == "android":
                    # Example: June 3, 2019 to 2019-06-03
                    self.latest_patch = datetime.strptime(
                        self.latest_patch, "%B %d, %Y")
                elif self.store == "apple":
                    # Example: 2014-07-15T15:08:56Z to 2014-07-15
                    self.latest_patch = datetime.strptime(
                        self.latest_patch[0:10], "%Y-%m-%d")

    def dict(self):
        return {
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

    def keys():
        return [
            'app_title',
            'bundleid',
            'store',
            'description',
            'dev_name',
            'dev_id',
            'fullprice',
            'versionnumber',
            'osreq',
            'latest_patch',
            'content_rating'
        ]

    @staticmethod
    def android_search(searchquery, country_code):
        """ Android Search Query, using the play-scraper package """
        results = []
        total = 0

        # As the play-scraper search functions per page, iteration (with a max
        # of 13) is required
        for i in range(0, 13):
            response = play_scraper.search(
                searchquery, i, True, 'en', country_code)
            # If the size of the page is 0, ergo when it is empty, break off
            # the loop
            if not len(response) == 0:
                for memb in response:
                    newapp = appResult(appResult.Source.Android, **memb)
                    total += 1
                    results.append(newapp)

            else:
                break

        print('Android total: %s' % total)
        return results

    @staticmethod
    def apple_search(searchquery, country_code):
        """ Apple Search Query, using the official iTunes API """
        results = []
        total = 0

        # Two variables nessecary in the construction of the final request-URL
        url_endpoint = 'http://ax.itunes.apple.com/WebObjects/MZStoreServices.woa/wa/wsSearch'
        search_params = {
            'country': country_code,
            'lang': 'en-US',
            'media': 'software',
            'limit': 200,
            'offset': 0,
            'term': searchquery
            }

        """
        The iTunes API functions with pages as well, the size of one 'page'
        is set using the limit paramater in search_params. The offset is to
        set the starting position of the query limit:200 and offset:0 => first
        200 results, limit:200 and offset:200 => second set of results.
        Limit has a max of 200
        """
        while True:
            response = requests.get(url_endpoint, params=search_params).json()
            # if the resultcount is less than 200, this is the last page
            total += response['resultCount']
            for memb in response['results']:
                results.append(appResult(appResult.Source.Apple, **memb))
            if response['resultCount'] < 200:
                break
            search_params['offset'] += search_params['limit']
        print('Apple total:%s' % total)
        return results

    @classmethod
    def search_appstores(self, arg_searchterm, arg_country):
        """ Using consts may seem redundant, but this allows one output to
        be applied differently where necessary. This way there is room for
        the addition of other languages without adding too much work
        """

        results = self.android_search(arg_searchterm, arg_country)
        results += self.apple_search(arg_searchterm, arg_country)
        return results
