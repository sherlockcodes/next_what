import os
from datetime import datetime
from cleaner.movie_name_cleaner import MovieCleaner
from imdb.imdb_parser import IMDBParser

class RecommendationBuilder:
	def __init__(self, movie_path, preferred_genres = [], exclude_genres = [], prefer_latest_movies = False):
		self.movie_path = movie_path
		self.preferred_genres = preferred_genres
		self.prefer_latest_movie = prefer_latest_movies
		self.exclude_genres = exclude_genres

	def get_reco_score(self, movie_info):
		total_score = 0
		release_year = movie_info.get("Year",0)
		if release_year is not None:
			total_score += release_year
		total_score += movie_info.get("imdbRating",0)
		total_score += movie_info.get("Metascore",0) / 10
		genre = movie_info.get("Genre",[])
		if self.prefer_latest_movie and release_year is not None:
			total_score += release_year - datetime.now().year
		if len(self.exclude_genres):
			if set(genre).isdisjoint(set(self.exclude_genres)) is False:
				return 0 # which means user choosen to exclude.
		if len(self.preferred_genres):
			common_genres_count = len(set(genre).intersection(set(self.preferred_genres))) 
			if common_genres_count:
				total_score += common_genres_count * 10
			else:
				total_score = 0
		return total_score

	def get_top_movies(self, top_count=5):
		final_list = sorted(self.movie_list.items(), key=lambda a: a[1]['next_what_score'], reverse=True)
		return final_list[0:top_count]

	def generate_reco(self, movies):
		self.movie_list = {}
		for movie in movies:
			score = self.get_reco_score(movie)
			if score:
				movie["next_what_score"] = score
				self.movie_list[movie["imdbID"]] = movie
		
	def build_reco(self):
		movies = os.listdir(self.movie_path)
		imdb = IMDBParser()
		cleaner = MovieCleaner()
		movies_list = []
		for movie_name in movies:
			movie_name = cleaner.decrapify_name(movie_name)
			response = imdb.get_movie_info(movie_name)
			if response is not None and 'Response' in response and response['Response'] != 'False':
				movies_list.append(response)
		self.generate_reco(movies_list)
		


