from bs4 import BeautifulSoup
import urllib2
import json
import urllib
import re

class IMDBParser:
    '''
       class to get movie details like genre, release year, ratings, meta score, and related movies 
       from given movie id.
    '''
    
    def __init__(self):
        self.movie_info = {}

    def get_movie_from_imdb(self, id):
        try:
            response = urllib2.urlopen("http://www.imdb.com/title/" + id)
            status_code = response.getcode()
            if status_code == 200:
                response = response.read()
                return BeautifulSoup(response, "html.parser")
        except Exception as e:
            print '[ALARM] IMDBParser::get_movie_id, exception', e
            return None

    def get_movie_info(self, name, release_year=None):
        try:
            params = {"t":name, "plot":"full", "r":"json"}
            if release_year is not None:
                params["y"] = release_year
            url_params = urllib.urlencode(params)
            response = urllib2.urlopen("http://www.omdbapi.com/?" + url_params)
            status_code = response.getcode()
            if status_code == 200:
                response = json.loads(response.read())
                self.movie_info = response
                self.post_process_response()
                return self.movie_info
        except Exception as e:
            print '[ALARM] IMDBParser::get_movie_id, exception', e
            return None

    def get_movie_by_name(self, name):
        movie_id = self.get_movie_info(name)
        self.get_movie_by_id(movie_id)
        return self.soup

    def get_movie_rating(self):
        return float(self.movie_info.get("imdbRating",0))
 
    def get_release_year(self):
        release_year = self.movie_info.get("Year",0)
        if release_year == "N/A":
            return None
        return int(release_year)

    def get_movie_genre(self):
        return map(str.strip,str(self.movie_info.get("Genre","")).split(","))

    def get_movie_meta_score(self):
        meta_score = self.movie_info.get("Metascore",0)
        if meta_score == "N/A":
            meta_score = 0
        return int(meta_score)

    def get_movie_language(self,name):
        pass

    def get_trailer_link(self, movie_id):
        soup = get_movie_from_imdb(movie_id)
        link_tags = soup.find("div",attrs={"class":"slate"}).find_all("a")
        trailer_link = ""
        for link_tag in link_tags:
            trailer_link = "http://www.imdb.com" + link_tag["href"]
            break
        return trailer_link

    def get_related_movies(self, id):
        pass

    def post_process_response(self):
        self.movie_info["Genre"] = self.get_movie_genre()
        self.movie_info["Metascore"] = self.get_movie_meta_score()
        self.movie_info["imdbRating"] = self.get_movie_rating()
        self.movie_info["Year"] = self.get_release_year()




    
