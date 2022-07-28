from pyxll import xl_func, plot 
from plots import * 

# Plot all the data from plots.py, but this time export those plots to an Excel file

@xl_func 
def plot_win_percentages_excel(win_dict):
    fig = plot_win_percentages(win_dict)
    plot(fig) 

@xl_func 
def plot_pregame_win_prob_excel(char_dict):
    fig = plot_pregame_win_prob(char_dict)
    plot(fig) 

@xl_func 
def plot_efficiencies_excel(char_dict):
    fig = plot_efficiencies(char_dict)
    plot(fig) 

@xl_func 
def plot_stocks_taken_excel(char_dict):
    fig = plot_stocks_taken(char_dict)
    plot(fig) 

@xl_func 
def plot_stocks_vs_efficiency_excel(all_players):
    fig = plot_stocks_vs_efficiency(all_players)
    plot(fig) 

@xl_func 
def plot_done_vs_dealt_excel(all_players):
    fig = plot_done_vs_dealt(all_players)
    plot(fig) 

@xl_func 
def plot_efficiency_comparisons_excel(all_players):
    fig = plot_efficiency_comparisons(all_players)
    plot(fig) 

@xl_func 
def plot_win_prob_vs_percent(all_players, percents):
    fig = plot_win_prob_vs_percent(all_players, percents)
    plot(fig) 

@xl_func
def simple_plot():
    # Data for plotting
    t = np.arange(0.0, 2.0, 0.01)
    s = 1 + np.sin(2 * np.pi * t)

    # Create the figure and plot the data
    fig, ax = plt.subplots()
    ax.plot(t, s)

    ax.set(xlabel='time (s)', ylabel='voltage (mV)',
           title='About as simple as it gets, folks')
    ax.grid()

    # Display the figure in Excel
    plot(fig)



test = {'Rob': [0.75,0.5, 100, 99, 150, 2.5, 1.0], 'Chrom': [0.67,0.5, 110, 87, 125, 2.8, 1.2], 'Bowser': [0.7,0.5, 120, 75, 200, 2.6, 0.5], 'Roy': [0.65, 0.5, 105, 8, 165, 2.4, 1.0]}
#plot_win_percentages_excel(test) 
#plot_stocks_taken_excel(test) 
#simple_plot() 