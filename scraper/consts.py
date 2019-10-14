# Key lists as they are represente in the play and apple API
apple_key_list = ['trackName', 'bundleId', 'description', 'artistName', 'artistId', 'price', 'version', 'minimumOsVersion', 'currentVersionReleaseDate', 'trackContentRating']
android_key_list = ['title', 'android', 'app_id', 'description', 'developer', 'developer_id', 'price', 'current_version', 'required_android_version', 'updated', 'content_rating']

# Illegal symbols that might corrupt the CSV output file
illegal_price = ['$', '£', '€', ' ', '.', ',']
illegal_desc = [('\r', ''), ('\n', ''), (';', ',')]
