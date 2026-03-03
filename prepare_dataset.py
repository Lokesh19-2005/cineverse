import pandas as pd

print("Loading title.basics...")
titles = pd.read_csv("title.basics.tsv", sep="\t", low_memory=False)

print("Loading ratings...")
ratings = pd.read_csv("title.ratings.tsv", sep="\t")

print("Filtering only movies...")
titles = titles[titles['titleType'] == 'movie']

print("Removing missing data...")
titles = titles[titles['startYear'] != '\\N']
titles = titles[titles['genres'] != '\\N']

titles['startYear'] = titles['startYear'].astype(int)
titles = titles[titles['startYear'] >= 2000]

print("Merging ratings...")
data = titles.merge(ratings, on='tconst')

print("Keeping good rated movies...")
data = data[data['averageRating'] >= 7.0]
data = data[data['numVotes'] >= 1000]

data = data[['tconst','primaryTitle','genres','averageRating']]
data.columns = ['movie_id','title','genre','imdb']

print("Saving cleaned file...")
data.to_csv("movies_cleaned.csv", index=False)

print("DONE")
print("Final dataset size:", data.shape)