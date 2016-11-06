import requests
import os
movie_path = '/media/hari/My Passport/MyStuff/movies/watched'
from cleaner.movie_name_cleaner import MovieCleaner
cleaner = MovieCleaner()
movies = os.listdir(movie_path)
from recommendation.recommendation import RecommendationBuilder
from imdb.imdb_parser import IMDBParser
movie_list = []
failed_names = []
for movie_name in movies:
	movie_name = cleaner.decrapify_name(movie_name)
	print 'looking for ', movie_name
	imdb = IMDBParser()
	response = imdb.get_movie_info(movie_name)
	if 'Response' in response and response['Response'] == 'False':
		print movie_name
		failed_names.append(movie_name)
	else:
		movie_list.append(response)

print 'top five movies'
reco = RecommendationBuilder()
reco.generate_reco(movie_list)
top_movies = reco.get_top_movies()
for movie in top_movies:
	print movie[1]['Title']

print 'top five romance movies'
reco = RecommendationBuilder(['Romance'],True) #latest romance 
reco.generate_reco(movie_list)
top_movies = reco.get_top_movies()
for movie in top_movies:
	print movie[1]['Title']

print 'top five action movies'
reco = RecommendationBuilder(['Action'],True) #latest Action 
reco.generate_reco(movie_list)
top_movies = reco.get_top_movies()
for movie in top_movies:
	print movie[1]['Title']

