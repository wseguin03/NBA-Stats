import pandas as pd
stats = pd.read_csv("CSV/fixed_player_mvp_stats.csv")
# print(pd.isnull(stats).sum())
# print(stats[pd.isnull(stats["3P%"])][["Player", "Year", "FTA"]])
stats = stats.fillna(0)
# print(stats[pd.isnull(stats["3P%"])][["Player", "Year", "3P%"]])
print(stats.columns)
