import requests
import play_scraper
import enum
from datetime import datetime
from .consts import android_key_list, apple_key_list, keysDict


"""TM
I would call this class AppResult or appResult, choose one and be consistent:
Currently, you also use dbJob and dbApp and DevelopmentConfig and ProductionConfig
"""
class appresult:
    """ 
    Each instance of this object represents one result from the app-store queries
    Both APIs return a range of data but the variables used here are the ones that are returned by both
    """

    class Source(enum.Enum):
        Android = 0
        Apple = 1
        Database = 2
    
    def __init__(self, source, **kwargs):
        """
        Because the list of given arguments is variable, this code crossreferences the arguments
        With a list of appstore-specific arguments. Based on that, a non-specific key is assigned to the value.
        That way the rest of the code can run universally.
        i represents the type of input (0: android search query, 1: apple search query, 2: database record)
        """

        """TM
        Why would you still use this i as a number? Use Source.Android, Source.Apple and 
        Source.Database everywhere. Magic numbers are not fun.

        You can use this to set this to the dict argument passed and if not set fall back to source.
        self.store = kwargsDict.get("store", source)


        Feeling like your constructor is too crowded? Use properties!

        def __init__(self, dev_id, dev_name):
            self.dev_id = dev_id
            self.dev_name = dev_name

        @property
        def dev_name(self):
            return self._dev_name
            
        @dev_name.setter
        def set_dev_name(self, value):
            if self.dev_id != "5700313618786177705" and value == 'Google Commerce Ltd'):
                self._dev_name = "N/A"
            else:
                self._dev_name = value
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
        
        """TM
        These escapes are not necessary, the csv and json module handle this for you
        """

        # for c, v in illegal_desc:
        #    self.description = self.description.replace(c, v)

        """TM
        The if statement below had some errors in it.

        case None:
        str(None) -> "None"
        if self.fullprice is None: will never occur

        There were also a bunch of braces that were not needed.
        I like the following way better (ask forgiveness, not permission, zen of python)

        try:
            price = int(kwargsDict["fullprice"])
            if price == 0:
                self.fullprice = "00"
            else:
                self.fullprice = str(price)
        except KeyError: # No fullprice specified
            self.fullprice = "00"
        except ValueError: # Faulty formatting
            self.fullprice = "00"

        This could be shortened to:

        try:
            self.fullprice = str(int(kwarsDict["fullprice"]) or "00")
        except KeyError, ValueError:
            self.fullprice = "00"

        but I'm not sure that is more readable. It (ab)uses the fact that
        int('0') -> False 
        and it falls through to the "00" in the or.
        """
        # Price formatting to cents
        self.fullprice = str(kwargDict.get("fullprice", "00")).strip()
        if self.fullprice is "None" or self.fullprice == "" or self.fullprice == "0":
            self.fullprice = "00"
        #for c in illegal_price:
        #    self.fullprice = self.fullprice.replace(c, '')
        self.fullprice = self.fullprice.strip()

        """TM
        I a key does not exist in a dictionary you will get a keyerror. By using .get() you get None or
        a default value if specified. Add your fallback date as default and overwrite, 
        this makes sure that you don't have to worry about which if-else chains you can get to 
        and which are unreachable.
        """
        self.latest_patch = kwargDict.get('latest_patch', datetime.strptime("1808-08-08", "%Y-%m-%d"))
        if source != self.Source.Database:
            if self.latest_patch is not None:
                if self.store == "android":
                    # Example: June 3, 2019 to 2019-06-03
                    self.latest_patch = datetime.strptime(self.latest_patch, "%B %d, %Y")
                elif self.store == "apple":
                    # Example: 2014-07-15T15:08:56Z to 2014-07-15
                    self.latest_patch = datetime.strptime(self.latest_patch[0:10], "%Y-%m-%d")
                
    
    """TM
    No need to store the return in a variable, just return the constructed object
    """
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


"""TM
Why would I put these in a static method? Because of the interface on the other side.
It's more of a personal preference, but look at these two examples:

from talos.appstore import AppResult, android_search

apps = android_search("query")

or

from talos.appstore import AppResult

apps = AppResult.query_playstore("query")


Because I use CamelCase it is clear this is a static method. By putting it in the class scope the
return type is clear from just the function call. This is helpful because often the imports 
at the top of the file and the place they are used are not on one screen. 
I almost never import functions only classes.
"""

def android_search(searchquery, country_code, pagerange=13):
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


def apple_search(searchquery, country_code):
    """ Apple Search Query, using the official iTunes API """
    results = []
    total = 0
    i = 0

    # Two variables nessecary in the construction of the final request-URL
    url_endpoint = 'http://ax.itunes.apple.com/WebObjects/MZStoreServices.woa/wa/wsSearch'
    search_params = {'country': country_code, 'lang': 'en-US',
                     'media': 'software', 'limit': 200, 'offset': 0, 'term': searchquery}

    """TM
    What is this horrific loop with i? Use a while True and a break. You can increase the
    offset simpy by doing search_params['offset'] += search_params['limit']. 
    Also, don't count a total, just use len(results). 
    Don't store newapp in a variable, just use
    results.append(
        appresult(
            appresult.Source.Apple,
            **memb
        )
    )
    """

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
            """TM
            Don't set missing results to empty string. Handle missing data in the
            apresult constructor. Then you can use sensible fallback values per
            key.
            """
            for keymemb in apple_key_list:
                if keymemb not in memb:
                    memb[keymemb] = ''

            newapp = appresult(appresult.Source.Apple, **memb)
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
