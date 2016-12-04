import os
import argparse

from recommendation.recommendation import RecommendationBuilder
from commons import consts

epilog_msg = "list of supported genres : " + ",".join(consts.KNOWN_GENRES)

def validate_args(args):
	validation_errors = []
	if args['i'] is not None and len(args['i'].split(',')):
		preferred_genres = args['i'].split(',')
		for genre in preferred_genres:
			if len(genre) and genre not in consts.KNOWN_GENRES:
				validation_errors.append('your preferred genre {} is not supported'.format(genre))
	if args['e'] is not None and len(args['e'].split(',')):
		genres_to_be_excluded = args['e'].split(',')
		for genre in genres_to_be_excluded:
			if len(genre) and genre not in consts.KNOWN_GENRES:
				validation_errors.append('your exclusion genre {} is not supported'.format(genre))
	if args['d'] is not None:
		is_dir_exists = os.path.exists(args['d'])
		if not is_dir_exists:
			validation_errors.append('given movie location {} is not found'.format(args['d']))
	return validation_errors

def get_parser():
	parser = argparse.ArgumentParser(
		description='Next what!!',
		epilog=epilog_msg)
	parser.add_argument('-d', help='Location of the movies folder', required=False)
	parser.add_argument('-i', help='Include movies from given genres only, comma separated',required=False)
	parser.add_argument('-e', help='Excludes movies from given genres', required=False)
	parser.add_argument('-r', nargs='?', const=0, type=int, help=' Prefer latest movies (default=0)')
	parser.add_argument('-t', nargs='?', const=5, type=int, help=' Get top movies (default=5)')
	return parser

def process_command_line():
	parser = get_parser()
	args = vars(parser.parse_args())
	errors = validate_args(args)
	if len(errors):
		print 'please fix below error(s):'
		for error in errors:
			print error
		parser.print_help()
	else:
		preferred_genres = []
		genres_to_be_excluded = []
		if args['i'] is not None:
			preferred_genres = args.get('i').split(',')
		if args['e'] is not None:
			genres_to_be_excluded = args.get('e','').split(',')			
		prefer_latest_movies = args.get('r')
		movie_path = args.get('d')
		top_count = args.get('t')
		if movie_path is None:
			movie_path = raw_input("Enter the movies folder location:")
			movie_path = movie_path.replace("\\", "\\\\")
			if not os.path.exists(str(movie_path)):
				print 'given movie location {} not exists'.format(movie_path)
				parser.print_help()
				exit()
		reco = RecommendationBuilder(movie_path=movie_path, preferred_genres=preferred_genres, exclude_genres= genres_to_be_excluded, prefer_latest_movies=prefer_latest_movies)
		reco.build_reco()
		top_movies = reco.get_top_movies(top_count)
		for movie in top_movies:
			print movie[1]['Title']

if __name__ == "__main__":
    process_command_line()