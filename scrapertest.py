import talos

# Some Constants
SEARCHTERM = "infection prevention"
COUNTRY = "us"  # us, uk, nl

app_results = talos.search_appstores(SEARCHTERM, COUNTRY)

talos.export_csv(app_results, "output")
