import statistics 
import scipy 
from scipy.stats import norm 

# method for getting all stats from the rows in a given sheet 
def get_player_stats(rows, data):
    stats = {} 
    for i in range(0,rows):
        opponent_stats = [] 
        opponent = data.at[i,'opponent']
        done = data.at[i,'damage done']
        dealt = data.at[i,'damage dealt']
        taken = data.at[i,'stocks taken']
        #lost = data.at[i,'stocks lost']
        lost = data.at[i,'lost']
        result = data.at[i,'result']
        #opponent_stats.append(opponent)
        opponent_stats.append(done)
        opponent_stats.append(dealt)
        opponent_stats.append(taken)
        #opponent_stats.append(lost) 
        opponent_stats.append(lost) 
        opponent_stats.append(result) 
        stats[opponent] = opponent_stats
        #print(stats) 
    
    return stats

# method for determining win percentage for a given character
def get_win_percentage(char_dict):               # pass in dict in format of all_stats dict (for just one character) 
    wins = 0
    total = 0
    for key in char_dict.keys():
        total += 1
        if 'won' in char_dict[key][4]:
            wins += 1
    return wins/total

# method for determining the best character based on win percentage 
def get_best(win_dict):                          # dict where key is character name, value is win percentage
    highest = 0                      # placeholder max value
    best = ''                        # placeholder best character
    for key in win_dict:
        if win_dict[key] > highest:
            highest = win_dict[key]
            best = key 
    return best, highest 


# method for determining character efficiency (percent/kill ratio)--the lower the ratio, the better 
def get_efficiency(char_dict):
    # average, when we win, and when we lose 
    percent = 0
    kills = 0
    win_percent = 0
    win_kills = 0
    lose_percent = 0
    lose_kills = 0
    for key in char_dict.keys():
        percent += char_dict[key][0]
        kills += char_dict[key][2]
        # check for wins
        if 'won' in char_dict[key][4]:
            win_percent += char_dict[key][0]
            win_kills += char_dict[key][2]
        # check for losses
        elif 'lost' in char_dict[key][4]:
            lose_percent += char_dict[key][0]
            lose_kills += char_dict[key][2]
    return percent/kills, win_percent/win_kills, lose_percent/lose_kills

# method to get average opponent efficiency
def get_opponent_efficiency(char_dict):
    opp_percent = 0
    opp_kills = 0
    for key in char_dict.keys():
        opp_percent += char_dict[key][1]
        opp_kills += char_dict[key][3]
    return opp_percent/opp_kills

# method to determine win percentage when we deal above a certain percent
def get_win_percentage_by_percent(char_dict, percent):       # percent is min threshold percent we're interested in (e.g. > 200%)
    total = 0
    wins = 0
    for key in char_dict.keys():
        if char_dict[key][0] >= percent:
            total += 1 
            if 'won' in char_dict[key][4]:
                wins += 1
    if total != 0:
        return wins/total
    return 0

# method to determine losing percentage when we're dealt above a certain percent 
def get_lose_percentage_by_percent(char_dict, percent):       # percent is min threshold percent dealt
    total = 0
    losses = 0
    for key in char_dict.keys():
        if char_dict[key][1] >= percent:
            total += 1
            if 'lost' in char_dict[key][4]:
                losses += 1
    return losses/total 

# method to return a character's average and SD values for percent dealt and stocks taken
def player_average_and_SD(char_dict):
    percent_list = [] 
    stock_list = [] 
    for key in char_dict.keys():
        percent_list.append(char_dict[key][0])
        stock_list.append(char_dict[key][2])
    
    # calculate mean and SD
    mean_percent = statistics.mean(percent_list)
    mean_stocks = statistics.mean(stock_list)
    sd_percent = statistics.stdev(percent_list)
    sd_stocks = statistics.stdev(stock_list)

    return mean_percent, sd_percent, mean_stocks, sd_stocks         # eventually plot these as a normal distribution

# method to find win probability based on player's average and SD of stocks taken 
def pregame_win_probability(mean, sd):
    zscore = (3-mean)/sd 
    win_prob = 1 - norm(loc = mean, scale = sd).cdf(3)       # if we get to 3 stocks, we win, so above 3 on normal distribution 
    return win_prob 

# method to calculate win probability at all points during a game (may be fun to eventually plot this)
# pwin is function of stock difference, percent difference, and time remaining
def ingame_win_probability(stock_diff, percent_diff, time_left):
    # take care of all the base cases first 
    if time_left == 420:
        return 0.5
    elif time_left == 0 and stock_diff > 0:
        return 1
    elif time_left == 0 and stock_diff < 0:
        return 0

    # standard ingame case--formula based on basketball in-game predictions
    pwin = (stock_diff * time_left / 420) + (percent_diff * time_left / 420)
    if pwin > 1:
        pwin = 1
    elif pwin < 0: 
        pwin = 0
    return pwin 


test = {'Zelda': [350, 187, 3, 2, 'won'], 'King K Rool': [248, 321, 1, 3, 'lost'], 'Snake': [452, 289, 3, 2, 'won '], 'Wolf': [275, 165, 3, 1, 'won ']}
test2 = {'ROB': 0.75, 'CHROM': 0.67}
#print(get_win_percentage(test))
#print(get_efficiency(test))
#print(get_best(test2))
#print(get_win_percentage_by_percent(test, 200))
#print(get_lose_percentage_by_percent(test, 200))
print(player_average_and_SD(test))
#print(pregame_win_probability(2.5, 1.0)) 
#print(get_opponent_efficiency(test))