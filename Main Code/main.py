years = list(range(2012,2024))
url_start = "https://www.basketball-reference.com/awards/awards_{}.html"
import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
# for year in years:
#   
#     url = url_start.format(year)
#     data = requests.get(url)
    
#     # print(data.text)
#     with open("mvp/{}.html".format(year), "w+", encoding="utf-8") as f:
#         f.write(data.text)
#         time.sleep(5)
dfs= []
for year in years:
    with open("mvp/{}.html".format(year), "r", encoding="utf-8") as f:
        page = f.read()

    soup = BeautifulSoup(page, "html.parser")
    soup.find('tr', class_ = "over_header").decompose()#removes header of table
    mvp_table = soup.find(id = "mvp")
    mvp = pd.read_html(str(mvp_table))[0]
    mvp["Year"] = year
    dfs.append(mvp)
    
mvps = pd.concat(dfs)
# mvps.to_csv("mvp.csv", index = False)

# ----------------------------------------------
# THIS CODE BELOW GRABS PLAYER STATS ONLY RUN WHEN NEEDED TO AVOID WEBSITE BAN
# ----------------------------------------------

# player_stats_url = "https://www.basketball-reference.com/leagues/NBA_{}_per_game.html"
# for year in years:
#     url = player_stats_url.format(year)
#     data = requests.get(url)
#     with open ("player/{}.html".format(year), "w+", encoding="utf-8") as f:
#         f.write(data.text)
#     time.sleep(3)
#  ----------------------------------------------
    
    
df = []
for year in years:
    with open ("player/{}.html".format(year), "r", encoding="utf-8") as f:
        page = f.read()
    soup = BeautifulSoup(page, "html.parser")
    soup.find('tr', class_ = "thead").decompose()#removes header of table
    player_table = soup.find(id = "per_game_stats")
    player = pd.read_html(str(player_table))[0]
    player["Year"] = year
    df.append(player)
    print(player["Player"])
players = pd.concat(df)
# players.to_csv("players.csv")