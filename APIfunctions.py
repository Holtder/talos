import play_scraper, requests, time, json
apple_key_list = ['trackName', 'bundleId', 'description', 'artistName', 'artistId', 'price', 'version', 'minimumOsVersion', 'currentVersionReleaseDate', 'trackContentRating']
android_key_list = ['title', 'android', 'app_id', 'description', 'developer', 'developer_id', 'price', 'current_version', 'required_android_version', 'updated', 'content_rating']

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


def description_cleanup(results):
    for app in results:
        if app.description == None:
            app.description = ''
        app.description = app.description.replace('\r', '')
        app.description = app.description.replace('\n', '')
        app.description = app.description.replace(';', ',')
    return results


def android_search(searchquery, country_code='nl', language_code='nl'):
    results = []
    total = 0
    for i in range(0, 1):
        resp = play_scraper.search(searchquery, i, True, language_code, country_code)
        if not len(resp) == 0:
            for memb in resp:
                for keymemb in android_key_list:
                    if keymemb not in memb:
                        memb[keymemb] = ''
                newapp = appresult(memb['title'], 'android', memb['app_id'], memb['description'], memb['developer'], memb['developer_id'], memb['price'], memb['current_version'], memb['required_android_version'], memb['updated'], memb['content_rating'])
                total += 1
                results.append(newapp)

        else:
            print('break')
            break

    print('Android total:%s' % total)
    results = description_cleanup(results)
    return results


def apple_search(searchquery, country_code='nl', language_code='nl_nl'):
    results = []
    total = 0
    i = 0
    url_endpoint = 'http://ax.itunes.apple.com/WebObjects/MZStoreServices.woa/wa/wsSearch'
    search_params = {'country':country_code,  'lang':language_code,  'media':'software',  'limit':200,  'offset':0,  'term':searchquery}
    while i > -1:
        search_params['offset'] = 200 * i
        resp = requests.get(url_endpoint, params=search_params).json()
        i = -1 if resp['resultCount'] < 200 else i + 1
        for memb in resp['results']:
            for keymemb in apple_key_list:
                if keymemb not in memb:
                    memb[keymemb] = ''

            newapp = appresult(memb['trackName'], 'apple', memb['bundleId'], memb['description'], memb['artistName'], memb['artistId'], memb['price'], memb['version'], memb['minimumOsVersion'], memb['currentVersionReleaseDate'], memb['trackContentRating'])
            total += 1
            results.append(newapp)

    print('Apple total:%s' % total)
    results = description_cleanup(results)
    return results