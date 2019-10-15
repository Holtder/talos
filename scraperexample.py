from talos.appstore import search_appstores, export_csv

# Some Constants
SEARCHTERM = "infection prevention"
COUNTRY = "us"  # us, uk, nl

app_results = search_appstores(SEARCHTERM, COUNTRY)

export_csv(app_results, "output")
