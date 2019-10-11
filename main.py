import APIfunctions

# Some Constants
SEARCHTERM = "help"
COUNTRY = "us"  # us, uk, nl

app_results = APIfunctions.search_both_stores(SEARCHTERM, COUNTRY)
APIfunctions.export_csv(app_results, "output")