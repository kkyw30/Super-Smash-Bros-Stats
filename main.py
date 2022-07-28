import xlrd                  # for reading in data from an excel file (spreadsheet) 
import pandas as pd 
import openpyxl              # have to import this to actually read in data from the excel file 
from stats import *
from plots import * 

# get all the sheet names
excel_file = 'SmashStats.xlsx'
f = pd.ExcelFile(excel_file) 
names = f.sheet_names

# read in data from each sheet
all_players = {} 
all_player_stats = {}          # key is character name, value is list (with all the other stats)
for name in names:
    data = pd.read_excel(excel_file, sheet_name=name)
    dimensions = data.shape
    all_stats = get_player_stats(dimensions[0], data)
    all_players[name.upper()] = all_stats 

    # calculate some statistics from all_stats dict 
    stats = [] 

    # calculate win percentage
    win_percent = get_win_percentage(all_stats)
    print(win_percent)
    stats.append(win_percent)
    
    # calculate pre-game win probability 
    mean = player_average_and_SD(all_stats)[2]
    sd = player_average_and_SD(all_stats)[3]
    pregame = pregame_win_probability(mean, sd)
    stats.append(pregame)

    # calculate efficiencies and append to list
    avg_eff = get_efficiency(all_stats)[0]
    win_eff = get_efficiency(all_stats)[1]
    lose_eff = get_efficiency(all_stats)[2]
    stats.append(avg_eff)
    stats.append(win_eff)
    stats.append(lose_eff)
    stats.append(mean)
    stats.append(sd) 

    all_player_stats[name.upper()] = stats 

# Generate plots based on calculated and extracted info
plot_win_percentages(all_player_stats)
plot_pregame_win_prob(all_player_stats)
plot_efficiencies(all_player_stats)
plot_stocks_taken(all_player_stats)
plot_stocks_vs_efficiency(all_players) 
plot_done_vs_dealt(all_players) 
plot_efficiency_comparisons(all_players) 
percents = [50, 100, 150, 200, 250, 300, 350, 400, 450]
plot_win_prob_vs_percent(all_players, percents) 


