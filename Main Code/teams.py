import requests
from bs4 import BeautifulSoup
import time
import pandas as pd

years = list(range(2012,2024))

# ----------------------------------------------
# THIS CODE BELOW GRABS PLAYER STATS ONLY RUN WHEN NEEDED TO AVOID WEBSITE BAN
# ----------------------------------------------

# for year in years:
#     team_stats_url = "https://www.basketball-reference.com/leagues/NBA_{}_standings.html"
#     url = team_stats_url.format(year)
#     data = requests.get(url)
#     with open ("team/{}.html".format(year), "w+", encoding="utf-8") as f:
#             f.write(data.text)
#     time.sleep(2)
   
#  ----------------------------------------------
df = []
for year in years:
    with open("team/{}.html".format(year), "r", encoding="utf-8") as f:
        page = f.read()
    soup = BeautifulSoup(page, "html.parser")
    soup.find('tr', class_ = "thead").decompose()#removes header of table
    team_table = soup.find(id = "divs_standings_E")
    team_east = pd.read_html(str(team_table))[0]
    team_east["Year"] = year
    team_east["Team"] = team_east["Eastern Conference"]
    del team_east["Eastern Conference"]

    soup = BeautifulSoup(page, "html.parser")
    soup.find('tr', class_ = "thead").decompose()#removes header of table
    team_table = soup.find(id = "divs_standings_W")
    team_west = pd.read_html(str(team_table))[0]
    team_west["Year"] = year
    team_west["Team"] = team_west["Western Conference"]
    del team_west["Western Conference"]
    
    df.append(team_east)
    df.append(team_west)

teams = pd.concat(df)
teams.to_csv("teamsGOOD.csv", index = False)
