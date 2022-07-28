import matplotlib.pyplot as plt 
import numpy as np 
import seaborn as sb 
from scipy.stats import norm 
from stats import * 

# TODO--plot win probability as function of percent done (segment it (50, 100, 150, 200, 250%), then take line-of-best-fit)

# method to plot win rates of different characters as bar graph 
def plot_win_percentages(win_dict):            # key is character, value is list (win percentage is first index in list)
    characters = win_dict.keys()
    list = win_dict.values()                   # list of all dict values (which are also lists) 
    percentages = [] 
    for emnt in list: 
        percentages.append(emnt[0])

    plt.bar(characters, percentages)
    plt.title('Win Percentages by Character') 
    plt.xlabel('Character') 
    plt.ylabel('Win Percentage')
    plt.show() 

# method to plot pregame win probabilities of different characters
def plot_pregame_win_prob(char_dict):
    characters = char_dict.keys()
    list = char_dict.values()
    probs = [] 
    for emnt in list:
        probs.append(emnt[1])               # pregame win prob is second element in list 
    
    plt.bar(characters, probs)
    plt.title('Pregame Win Probabilities') 
    plt.xlabel('Character')
    plt.ylabel('Win Probability') 
    plt.show() 

# method to plot average, win, and loss efficiencies for each character
def plot_efficiencies(char_dict):
    characters = char_dict.keys() 
    list = char_dict.values() 
    avg = [] 
    wins = [] 
    losses = [] 

    # aggregate efficiencies into the right list
    for emnt in list: 
        avg.append(emnt[2])
        wins.append(emnt[3])
        losses.append(emnt[4])

    x = np.arange(len(characters))       # label locations
    width = 0.3                          # bar width 

    # plot the three bars
    fig, ax = plt.subplots() 
    rect1 = ax.bar(x - width, avg, width, label = 'Average')
    rect2 = ax.bar(x, wins, width, label = 'Wins') 
    rect3 = ax.bar(x + width, losses, width, label = 'Losses') 

    # labels and titles 
    ax.set_ylabel('Efficiencies')
    ax.set_xlabel('Characters') 
    ax.set_title('Character Efficiencies by Wins and Losses') 
    ax.set_xticks(x, characters) 
    ax.legend() 

    ax.bar_label(rect1, padding=3)
    ax.bar_label(rect2, padding=3)
    ax.bar_label(rect3, padding=3) 

    fig.tight_layout() 

    plt.show() 

# method to plot normal distribution of stocks taken 
def plot_stocks_taken(char_dict):
    data = np.arange(0,6,0.01)

    # accumulate all the means and sd values so we can make subplots
    means = [] 
    sds = [] 
    for key in char_dict.keys():
        means.append(char_dict[key][5])
        sds.append(char_dict[key][6])
    
    # define the distributions for each character
    s_list = [] 
    for i in range (0,len(means)):
        s = norm.pdf(data, means[i], sds[i])
        s_list.append(s)                      # create list of all normal distributions 

    # now generate the plots (2 subplots per figure) 
    plt.figure(1) 
    total = len(s_list)
    for i in range(0,total):
        plt.subplot(i+11+total*100)
        plt.plot(data, s_list[i])
        plt.title(''+list(char_dict.keys())[i] + ' Expected Stocks Taken') 
        plt.xlabel('Stocks Taken') 
        plt.ylabel('Probability Density') 
        plt.show() 

# method to plot expected stocks taken vs. efficiency
def plot_stocks_vs_efficiency(all_players):                   # in format of the all_players dict--need to calculate efficiency using percent and stocks taken
    efficiency_dict = {}                                   # to store {character: efficiency} 

    # calculate efficiency for all characters and store them in list of tuples (in efficiency_dict)
    for key in all_players.keys():
        stats_dict = all_players[key] 
        efficiencies = [] 
        stocks = [] 
        for key2 in stats_dict.keys():                               # key2 is name of opponent
            efficiencies.append(stats_dict[key2][0] / stats_dict[key2][2])   # percent/stocks
            stocks.append(stats_dict[key2][2]) 
        # add tuple_list for that character to dict
        efficiency_dict[key] = (efficiencies, stocks) 

    # for each character, plot all the individual points and find line of best fit
    plt.figure(1) 
    total = len(list(efficiency_dict.keys()))                   # to determine number of subplots
    for key in efficiency_dict:
        # define efficiencies and stocks as arrays 
        x_efficiencies = np.array(efficiency_dict[key][0])       # convert to np array so we can plot it 
        y_stocks = efficiency_dict[key][1]

        # find line of best fit
        a, b = np.polyfit(x_efficiencies, y_stocks, 1)

        # add individual points and line of best fit to plot
        curr = list(efficiency_dict.keys()).index(key)
        plt.subplot(curr+11+total*100) 
        plt.scatter(x_efficiencies, y_stocks)
        plt.plot(x_efficiencies, a*x_efficiencies+b)
        plt.title(key + ' Expected Stocks Taken as Function of Efficiency') 
        plt.xlabel('Percent Dealt') 
        plt.ylabel('Stocks Taken') 
        plt.show() 

# method to plot percent done vs. percent dealt
def plot_done_vs_dealt(all_players):
    percent_dict = {} 
    # for each character, get the percent done and dealt for each game
    for key in all_players.keys():
        player_dict = all_players[key]
        done = [] 
        dealt = [] 
        for key2 in player_dict:
            done.append(player_dict[key2][0])
            dealt.append(player_dict[key2][1])
        percent_dict[key] = (dealt, done) 

    # plot the individual points and find line of best fit 
    plt.figure(1) 
    total = len(list(percent_dict.keys()))                          # to determine number of subplots
    for key in percent_dict:
        x_dealt = np.array(percent_dict[key][0])
        y_done = percent_dict[key][1]

        # find line of best fit 
        a, b = np.polyfit(x_dealt, y_done, 1)

        # add individual points and line of best fit to plot
        curr = list(percent_dict.keys()).index(key)
        plt.subplot(curr+11+total*100)
        plt.scatter(x_dealt, y_done) 
        plt.plot(x_dealt, a*x_dealt+b)
        plt.title(key + ' Percent Done as Function of Percent Dealt') 
        plt.xlabel('Percent Dealt') 
        plt.ylabel('Percent Done') 
        plt.show() 

# method to plot our efficiency vs. opponent efficiency 
def plot_efficiency_comparisons(all_players):
    efficiency_dict = {} 
    # for each character, get efficiency and opponent efficiency 
    for key in all_players.keys():
        player_dict = all_players[key]
        our = [] 
        opponent = [] 
        for key2 in player_dict:
            our.append(player_dict[key2][0]/player_dict[key2][2])
            opponent.append(player_dict[key2][1]/player_dict[key2][3])
        efficiency_dict[key] = (opponent, our)

    # plot the individual points and find line of best fit 
    plt.figure(1) 
    total = len(list(efficiency_dict.keys()))
    for key in efficiency_dict:
        x_opponent = np.array(efficiency_dict[key][0])
        y_our = efficiency_dict[key][1]

        # find line of best fit 
        a, b = np.polyfit(x_opponent, y_our, 1)

        # add individual points and line of best fit to plot
        curr = list(efficiency_dict.keys()).index(key)
        plt.subplot(curr+11+total*100) 
        plt.scatter(x_opponent, y_our) 
        plt.plot(x_opponent, a*x_opponent+b)
        plt.title(key + ' Our Efficiency as Function of Opponent Efficiency') 
        plt.xlabel('Opponent Efficiency') 
        plt.ylabel('Our Efficiency') 
        plt.show() 

# method to plot win probability as function of percent done 
def plot_win_prob_vs_percent(all_players, percents):                  # pass in all_players dict and list of percents done
    win_probs = {} 
    # calculate win probabilies for each character and percents done 
    for key in all_players.keys():
        player_dict = all_players[key]
        individual_probs = [] 
        for percent in percents:
            individual_probs.append(get_win_percentage_by_percent(player_dict, percent))
        win_probs[key] = individual_probs

    # plot individual points and find line of best fit 
    plt.figure(1)
    total = len(list(win_probs.keys()))
    for key in win_probs:
        x_percent = np.array(percents) 
        y_win_prob = win_probs[key]

        # find line of best fit 
        a, b = np.polyfit(x_percent, y_win_prob, 1)

        # add individual points and line of best fit to plot
        curr = list(win_probs.keys()).index(key)
        plt.subplot(curr+11+total*100)
        plt.scatter(x_percent, y_win_prob)
        plt.plot(x_percent, a*x_percent+b)
        plt.title(key + ' Win Probability as Function of Percent Done') 
        plt.xlabel('Percent Done') 
        plt.ylabel('Win Probability') 
        plt.show() 

    
# {'Character': [win%, win_prob, avg_eff, win_eff, loss_eff, avg_stocks, sd_stocks]}
test = {'Rob': [0.75,0.5, 100, 99, 150, 2.5, 1.0], 'Chrom': [0.67,0.5, 110, 87, 125, 2.8, 1.2], 'Bowser': [0.7,0.5, 120, 75, 200, 2.6, 0.5], 'Roy': [0.65, 0.5, 105, 8, 165, 2.4, 1.0]}
# {'Character': {'Opponent': [done, dealt, taken, lost, result]}}
test2 = {'Rob': {'Zelda': [350, 187, 3, 2, 'won'], 'King K Rool': [248, 321, 1, 3, 'lost'], 'Snake': [452, 289, 3, 2, 'won']}, 'Chrom': {'Zelda': [310, 197, 3, 2, 'won'], 'Palutena': [207, 275, 2, 3, 'lost'], 'Captain Falcon': [256, 224, 3, 2, 'won']}, 'Bowser': {'Zelda': [310, 197, 3, 2, 'won'], 'Palutena': [267, 235, 3, 2, 'won'], 'Captain Falcon': [256, 224, 3, 2, 'won']}}
percents = [50, 100, 150, 200, 250, 300, 350, 400]
#plot_win_percentages(test)
#plot_pregame_win_prob(test) 
#plot_efficiencies(test) 
#plot_stocks_taken(test)
#plot_stocks_vs_efficiency(test2) 
#plot_done_vs_dealt(test2) 
#plot_efficiency_comparisons(test2)
#plot_win_prob_vs_percent(test2, percents)
