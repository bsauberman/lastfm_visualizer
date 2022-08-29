from matplotlib import animation
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import seaborn as sns
import numpy as np
import pandas as pd
import csv
from collections import OrderedDict


PRE_PRUNE_PATH = "bsauberman.csv"
POST_PRUNE_PATH = 'bsauberman_pruned.csv'

curr_row = 0
df = pd.read_csv(POST_PRUNE_PATH)

def update_counts(curr_row):
    curr_day = df['DateTime'][curr_row]

    day = df['DateTime'][curr_row]
    artist = df['Artist'][curr_row]

    while artist and day and curr_day == day:
        if artist not in artists.keys():
            artists[artist] = 0
            #print(artist + ' added to keys with count of 0')
        artists[artist] = artists[artist] + 1
        #print(artist + ' count is now ' + str(artists[artist]))

        curr_row = curr_row + 1
        if curr_row < len(df):
            day = df['DateTime'][curr_row]
            artist = df['Artist'][curr_row]
        else: break

    return curr_row, artists

def prune_csv():
    csvreader = csv.reader(open(PRE_PRUNE_PATH))
    csvwriter = csv.writer(open(POST_PRUNE_PATH, "w"))

    # Deal with the header
    header = next(csvreader)
    header.append('Passed')
    csvwriter.writerow(header)
    prev_row = next(csvreader)
    # Process data rows
    for row in csvreader:
        if row[3]: row[3] = str(row[3])
        if row[0]: row[0] = str(row[0])
        if not row[3]: row[3] = prev_row[3]
        if not row[0]: row[0] = prev_row[1]
        prev_row = row

        csvwriter.writerow(row)    
        

def get_top_artists(data, n=10, order=True):

    top_artists = sorted(data.items(), key=lambda x: x[1], reverse=True)[:n]
    if order:
        return OrderedDict(top_artists)
    return dict(top_artists)

def get_data():
    for curr_row in range(len(df)-1, 0, -1):
        print(curr_row)
        if curr_row < 0:
            break
        curr_row = update_counts(curr_row)
        top_artists = get_top_artists(artists, 10, True)
    
        #create_image(top_artists)

def newanimate():

    # Initialize the matplotlib figure
    f, ax = plt.subplots(figsize=(6, 15))

    # Plot the total crashes
    sns.set_color_codes("pastel")
    keys = list(artists.keys())
    # get values in the same order as keys, and parse percentage values
    vals = [float(artists[k][:-1]) for k in keys]
    sns_plot = sns.barplot(x=keys, y=vals)

    #sns.barplot(x=artists.values(), y=artists.keys(), data=artists,
                #label="Total", color="b")


    # Add a legend and informative axis label
    ax.legend(ncol=2, loc="lower right", frameon=True)
    ax.set(xlim=(0, 24), ylabel="",
        xlabel="Automobile collisions per billion miles")
    sns.despine(left=True, bottom=True)
    fig = sns_plot.get_figure()
    fig.savefig("/images.output.png")



artists = {}
print("here we go!!")
#prune_csv()
#get_data()
#create_visualizer()


import matplotlib.pyplot as plt
from matplotlib import animation

fig=plt.figure()
axes = fig.add_subplot(1,1,1)
axes.set_xlim(0, 500)
plt.style.use("seaborn")
axes.set_xlabel("Plays")

n=100 #Number of frames
x= get_top_artists(artists, 10, True).keys()
barcollection = plt.bar(x, get_top_artists(artists, 10, True).values())

def animate(i):
    global curr_row
    curr_row, artists = update_counts(curr_row)
    top_artists = get_top_artists(artists, 10, True)
    plt.bar(top_artists.keys(), top_artists.values())

anim=animation.FuncAnimation(fig, animate, repeat=False, blit=False,
                             interval=10)
plt.show()

f = "lastfm_visualizr.gif" 
writergif = animation.PillowWriter(fps=30) 
anim.save(f, writer=writergif)




# import imageio
# images = []
# for filename in filenames:
#     images.append(imageio.imread(filename))
# imageio.mimsave('lastfm_visualizer.gif', images)



