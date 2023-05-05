import pandas as pd

mvps = pd.read_csv("CSV/mvp.csv")
mvps = mvps[['Player', 'Year', "Pts Won", "Pts Max", "Share"]]

players = pd.read_csv("CSV/players.csv") 
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

combined = players.merge(mvps, how="outer", on=["Player", "Year"])
combined = combined.dropna(subset=['Player']) # drop rows where "Player" column is null
combined [["Pts Won", "Pts Max", "Share"]] = combined[["Pts Won", "Pts Max", "Share"]].fillna(0)

teams = pd.read_csv("CSV/teams.csv")
teams = teams[~teams["W"].str.contains("Division")]
teams["Team"] = teams["Team"].str.replace("*", "", regex=False)

# print(teams)
nicknames = {}
with open("CSV/nicknames.csv", "r") as f:
    lines = f.readlines()
    for line in lines[1:]:
        abbrev,name = line.replace("\n", "").split(",")
        nicknames[abbrev] = name

combined["Team"] = combined["Tm"].map(nicknames)

stats = combined.merge(teams, how="outer", on=["Team", "Year"])
stats["GB"] = stats["GB"].str.replace("—", "0", regex=False)
stats = stats.dropna(subset=['Player']) # drop rows where "Player" column is null
stats = stats.apply(pd.to_numeric, errors='ignore')
# stats.to_csv("CSV/fixed_player_mvp_stats.csv", index=False)







highest_score = stats[stats["G"]>70].sort_values("PTS", ascending=False).head(10)
print(highest_score)
# # print(highest_score.plot.bar(x="Player", y="PTS", rot=0))
# top = stats.groupby("Year").apply(lambda x: x.sort_values("PTS", ascending=False).head(1))

# prompt = input("Enter a player's name: ")
# player_stats = stats[stats["Player"] == prompt]
# # Output the entered player's average stats from 2020-2023
# average_stats = player_stats.groupby("Player").mean()
# average_stats = average_stats[["PTS", "AST", "TRB", "STL", "BLK"]]
# print(average_stats)



