import scraper

# Some Constants
SEARCHTERM = "infection prevention"
COUNTRY = "us"  # us, uk, nl

app_results = scraper.search_both_stores(SEARCHTERM, COUNTRY)

scraper.export_csv(app_results, "output")
