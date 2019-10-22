# Key lists as they are represente in the play and apple API
COUNTRY_ABBREV = [('us', 'United States'), ('gb', 'Great Britain'), ('nl', 'The Netherlands')]
illegal_price = ['$', '£', '€', ' ', '.', ',']

keysDict = [
    # Android keys dictionary
    {
        'title': 'app_title',
        'app_id': 'bundleid',
        'store': 'store',
        'description': 'description',
        'developer': 'dev_name',
        'developer_id': 'dev_id',
        'price': 'fullprice',
        'current_version': 'versionnumber',
        'required_android_version': 'osreq',
        'updated': 'latest_patch',
        'content_rating': 'content_rating'
    },
    # Apple keys dictionary
    {
        'trackName': 'app_title',
        'bundleId': 'bundleid',
        'store': 'store',
        'description': 'description',
        'artistName': 'dev_name',
        'artistId': 'dev_id',
        'price': 'fullprice',
        'version': 'versionnumber',
        'minimumOsVersion': 'osreq',
        'currentVersionReleaseDate': 'latest_patch',
        'trackContentRating': 'content_rating'
    },
    # Database keys dictionary
    {
        'app_title': 'app_title',
        'bundleid': 'bundleid',
        'store': 'store',
        'description': 'description',
        'dev_name': 'dev_name',
        'dev_id': 'dev_id',
        'fullprice': 'fullprice',
        'versionnumber': 'versionnumber',
        'osreq': 'osreq',
        'latest_patch': 'latest_patch',
        'content_rating': 'content_rating'
    }
]
