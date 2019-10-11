import APIfunctions

arg_searchterm = "chrome"
arg_country = "us"  # us, uk, nl
app_results = APIfunctions.search_both_stores(
    arg_searchterm, arg_country)

APIfunctions.export_csv(app_results, "output")


# Other option: pull from either app-store and concatenate the results
# app_results += APIfunctions.android_search(arg_searchterm, arg_country, android_language_codes[arg_language], 1)
# app_results += APIfunctions.apple_search(arg_searchterm, arg_country, apple_language_codes[arg_language])
