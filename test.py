import pandas as pd

mvps = pd.read_csv("mvp.csv")

mvps = mvps[['Player', 'Year', "Pts Won", "Pts Max", "Share"]]

players = pd.read_csv("players.csv")
del players['Unnamed: 0']
del players['Rk']  # Deletes first two useless columns

players["Player"] = players["Player"].str.replace("*", "", regex=False)  # Removes asterisks from names

players.groupby(["Player", "Year"])

def single_row(df):
    if df.shape[0] == 1:
        return df
    else:
        row = df[df["Tm"] == "TOT"]
        row["Tm"] = df.iloc[-1, :]["Tm"]
        return row

players = players.groupby(["Player", "Year"]).apply(single_row)
players.index = players.index.droplevel()
players.index = players.index.droplevel()

combined = players.merge(mvps, how="outer", on=["Player", "Year"])
combined[["Pts Won", "Pts Max", "Share"]] = combined[["Pts Won", "Pts Max", "Share"]].fillna(0)

teams = pd.read_csv("teams.csv")
teams = teams[~teams["W"].str.contains("Division")]
teams["Team"] = teams["Team"].str.replace("*", "", regex=False)

nicknames = {}
with open("nicknames.csv", "r") as f:
    lines = f.readlines()
    for line in lines[1:]:
        abbrev, name = line.replace("\n", "").split(",")
        nicknames[abbrev] = name

combined["Team"] = combined["Tm"].map(nicknames)

stats = combined.merge(teams, how="outer", on=["Team", "Year"])
stats["GB"] = stats["GB"].str.replace("—", "0", regex=False)
stats = stats.apply(pd.to_numeric, errors='ignore')

# Modify the code to calculate average stats only in the past 3 years
dfs = []
current_year = 2023
past_years = [current_year - i for i in range(3)]

for player_name in stats["Player"].unique():
    player_stats = stats[stats["Player"] == player_name]
    player_stats_past_years = player_stats[player_stats["Year"].isin(past_years)]
    if player_stats_past_years.shape[0] == 0:
        continue
    average_stats = player_stats_past_years.groupby("Player").mean()
    average_stats = average_stats[["PTS", "AST", "TRB", "STL", "BLK"]]
    dfs.append(average_stats)

average_stats_df = pd.concat(dfs, axis=0)
average_stats_df.reset_index(inplace=True)
average_stats_df.to_csv("average_stats.csv", index=False)
