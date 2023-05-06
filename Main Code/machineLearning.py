import pandas as pd
from sklearn.linear_model import Ridge
stats = pd.read_csv("CSV/fixed_player_mvp_stats.csv")
stats = stats.fillna(0)

# print(stats[pd.isnull(stats["3P%"])][["Player", "Year", "FTA"]])
# print(stats[pd.isnull(stats["3P%"])][["Player", "Year", "3P%"]])

# print(stats[pd.isnull(stats["3P%"])][["Player", "Year", "3P%"]])

predictors = ['Age','G', 'GS', 'MP', 'FG', 'FGA', 'FG%', '3P',
       '3PA', '3P%', '2P', '2PA', '2P%', 'eFG%', 'FT', 'FTA', 'FT%', 'ORB',
       'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS', 'Year',
        'W', 'L', 'W/L%', 'GB', 'PS/G',
       'PA/G', 'SRS']

train = stats[stats["Year"] < 2023]
test = stats[stats["Year"] == 2023]


reg = Ridge(alpha=0.1)

reg.fit(train[predictors], train["Share"])
Ridge(alpha=0.1)

predictions = reg.predict(test[predictors])

predictions = pd.DataFrame(predictions, columns = ["Predictions"], index=test.index)

combination = pd.concat([test[["Player", "Share"]], predictions], axis=1)

# print(combination.sort_values("Share", ascending=False).head(10))

from sklearn.metrics import mean_squared_error
# print(mean_squared_error(combination["Share"], combination["Predictions"]))
combination = combination.sort_values("Share", ascending=False)
combination["Rank"] = list(range(1,combination.shape[0]+1))
combination = combination.sort_values("Predictions", ascending=False)
combination["Predicted Rank"] = list(range(1,combination.shape[0]+1))
# print(combination.head(10))
combination.sort_values("Share", ascending=False).head(10)
# print(combination.sort_values("Share", ascending=False).head(10))
def find_ap(combination):
       actual = combination.sort_values("Share", ascending=False).head(5)
       predicted = combination.sort_values("Predictions", ascending=False)
       ps = []
       found = 0
       seen = 1
       for index,row in predicted.iterrows():
              if row["Player"] in actual["Player"].values:
                     found += 1
                     ps.append(found/seen)
              seen += 1
       return sum(ps)/len(ps)#ERROR METRIC TO PREDICT TOP 5 PLAYERS
# print(find_ap(combination))

years = list(range(2012,2024))
aps = []
all_predictions = []
for year in years[5:]:
       train = stats[stats["Year"] < year]
       test = stats[stats["Year"] == year]
       reg.fit(train[predictors], train["Share"])
       
       predictions = reg.predict(test[predictors])
       predictions = pd.DataFrame(predictions, columns = ["Predictions"], index=test.index)
       combination = pd.concat([test[["Player", "Share"]], predictions], axis=1)
       all_predictions.append(combination)
       aps.append(find_ap(combination))
# print(sum(aps)/len(aps))
def add_ranks(combination):
       combination = combination.sort_values("Share", ascending=False)
       combination["Rank"] = list(range(1,combination.shape[0]+1))
       combination = combination.sort_values("Predictions", ascending=False)
       combination["Predicted Rank"] = list(range(1,combination.shape[0]+1))
       combination["Difference"] = combination["Rank"] - combination["Predicted Rank"]
       return combination
ranking = add_ranks(all_predictions[1])
# print(ranking[ranking["Rank"]<6].sort_values("Difference", ascending=False))
def backtest(stats, model, year, predictors):
       aps = []
       all_predictions = []
       for  year in years[5:]:
              train = stats[stats["Year"] < year]
              test = stats[stats["Year"] == year]
              model.fit(train[predictors], train["Share"])
              
              predictions = reg.predict(test[predictors])
              predictions = pd.DataFrame(predictions, columns = ["Predictions"], index=test.index)
              combination = pd.concat([test[["Player", "Share"]], predictions], axis=1)
              combination = add_ranks(combination)
              all_predictions.append(combination)
              aps.append(find_ap(combination))
       return sum(aps)/len(aps), aps, pd.concat(all_predictions)    
mean_ap, aps, all_predictions = backtest(stats, reg, years[5:], predictors)

# print(all_predictions[all_predictions["Rank"]<6].sort_values("Difference", ascending=False).head(10))
# important_coefficient = pd.concat([pd.Series(reg.coef_), pd.Series(predictors)], axis=1).sort_values(0, ascending=False)
# print(important_coefficient)

stats_ratios = stats[["PTS", "AST", "STL", "BLK", "3P", "Year"]].groupby("Year").apply(lambda x: x/x.mean())
stats[["PTS_T", "AST_R", "STL_R", "BLK_R", "3P_R"]] = stats_ratios[["PTS", "AST", "STL", "BLK", "3P"]]


predictors+=["PTS_T", "AST_R", "STL_R", "BLK_R", "3P_R"]
mean_ap, aps, all_predictions = backtest(stats, reg, years[5:], predictors)

stats["NPos"] = stats["Pos"].astype("category").cat.codes
stats["NTm"] = stats["Tm"].astype("category").cat.codes

from sklearn.ensemble import RandomForestRegressor
rf = RandomForestRegressor(n_estimators=100, random_state=1, min_samples_split=5)
mean_ap, aps, all_predictions = backtest(stats, rf, years[5:], predictors)


