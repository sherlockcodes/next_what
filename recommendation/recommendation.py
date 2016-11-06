from datetime import datetime

class RecommendationBuilder:
	def __init__(self, preferred_genres = [], prefer_latest_movie = False):
		self.preferred_genres = preferred_genres
		self.prefer_latest_movie = prefer_latest_movie

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
			movie["next_what_score"] = score
			self.movie_list[movie["imdbID"]] = movie
		




