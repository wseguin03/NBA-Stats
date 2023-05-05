import pandas as pd

mvps = pd.read_csv("mvp.csv")

mvps = mvps[['Player', 'Year', "Pts Won", "Pts Max", "Share"]]

players = pd.read_csv("players.csv") 
del players['Unnamed: 0']
del players['Rk']#Deletes first two useless columns

players["Player"] = players["Player"].str.replace("*", "", regex=False)#Removes asterisks from names
# print(players["Player"].head(50))
players.groupby(["Player", "Year"])

def single_row(df):
    if df.shape[0] ==1:
        return df
    else:
        row = df[df["Tm"] == "TOT"]
        row["Tm"] = df.iloc[-1,:]["Tm"]
        return row
players = players.groupby(["Player", "Year"]).apply(single_row)
players.index = players.index.droplevel()
players.index = players.index.droplevel()
combined = players.merge(mvps, how="outer" ,on=["Player", "Year"])
combined [["Pts Won", "Pts Max", "Share"]] = combined[["Pts Won", "Pts Max", "Share"]].fillna(0)

teams = pd.read_csv("teams.csv")
teams = teams[~teams["W"].str.contains("Division")]
teams["Team"] = teams["Team"].str.replace("*", "", regex=False)
nicknames = {}
with open("nicknames.csv", "r") as f:
    lines = f.readlines()
    for line in lines[1:]:
        abbrev,name = line.replace("\n", "").split(",")
        nicknames[abbrev] = name
combined["Team"] = combined["Tm"].map(nicknames)


stats = combined.merge(teams, how="outer", on=["Team", "Year"])
stats["GB"] = stats["GB"].str.replace("—", "0", regex=False)
stats = stats.apply(pd.to_numeric, errors='ignore')

# Modify the code to calculate average stats only in the past 3 years
dfs = []
current_year = 2023
for year in range(2020, current_year):
# past_years = [current_year - i for i in range(3)]
    player_name = input("Enter a player's name: ")
    player_stats = stats[stats["Player"] == player_name]
    player_stats_past_years = player_stats[player_stats["Year"].isin(past_years)]
    average_stats = player_stats_past_years.groupby("Player").mean()
    average_stats = average_stats[["PTS", "AST", "TRB", "STL", "BLK"]]
    print(average_stats)














# # Prompt the user to enter a value for the given columns to see the probability of them scoring over that number
# prompt_pts = input("Enter a value for PTS: ")
# # prompt_ast = input("Enter a value for AST: ")
# # prompt_trb = input("Enter a value for TRB: ")
# # prompt_stl = input("Enter a value for STL: ")
# # prompt_blk = input("Enter a value for BLK: ")
# probability_pts = (player_stats_past_years["PTS"] > float(prompt_pts)).sum() / len(player_stats_past_years)
# # probability_ast = (player_stats_past_years["AST"] > float(prompt_ast)).sum() / len(player_stats_past_years)
# # probability_trb = (player_stats_past_years["TRB"] > float(prompt_trb)).sum() / len(player_stats_past_years)
# # probability_stl = (player_stats_past_years["STL"] > float(prompt_stl)).sum() / len(player_stats_past_years)
# # probability_blk = (player_stats_past_years["BLK"] > float(prompt_blk)).
# print(probability_pts)
