# HLTV-scraper

Automated webscraper for team and player stats from [HLTV.org](https://www.hltv.org)

Uses undetected-chrome webdriver.

Returns a pandas Dataframe `fdf` (and .csv) with individual stats of every player of every team's historical lineup from a list of teams in given input URL.

Each lineup (variation of a team) is presented as a standalone team

Input URL should link to a list of teams, not players -> [example](https://www.hltv.org/stats/teams?startDate=2024-03-20&endDate=2024-06-20)

~~If cookies popup appears in webdriver window, accept all~~



Not detected by cloudflare as of 06.06.2025

<br />

a snippet of scraped data (showing 8/25 variables):

![image](https://github.com/MaiqTheHonest/HLTV-scraper/assets/60844551/6fa839ab-b7c1-4523-86ee-bdadbd12b628)
