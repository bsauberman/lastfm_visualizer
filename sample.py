import seaborn as sns
pal = sns.color_palette("rocket", 10000, as_cmap=True)
vals = ['The Strokes', 'The Beatles', 'Augustine', 'Caamp']
count = 0
for rank in range(len(vals)):
    hash = 0
    for char in range(len(vals[rank])):
        hash += ord(vals[rank][char]) 
        #print(hash)
    hash %= 256
    print(hash, pal.colors[hash])

#print(pal.colors)
