import scraper

# Some Constants
SEARCHTERM = "infection prevention"
COUNTRY = "us"  # us, uk, nl

app_results = scraper.search_appstores(SEARCHTERM, COUNTRY)

scraper.export_csv(app_results, "output")
