import seaborn as sns
pal = sns.color_palette("rocket", 10000, as_cmap=True)
print(len(pal.colors))
