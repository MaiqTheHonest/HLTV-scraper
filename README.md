# HLTV-scraper

Automated webscraper for team and player stats from [HLTV.org](https://www.hltv.org)

Based on Selenium and Undetected Chrome webdrivers, scraping done by BeautifulSoup 

Returns a pandas Dataframe `fdf` with individual stats of every player of every team's historical lineup from a list of teams in given input URL

Each lineup within the same team is returned as a standalone team

Input URL should link to a list of teams, not players -> [example](https://www.hltv.org/stats/teams?startDate=2024-03-20&endDate=2024-06-20)

If cookies popup appears in webdriver window, accept all



Not detected by cloudflare as of 19.06.2024
