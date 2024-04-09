from database.crud import *
from devtools import pprint

pprint(get_most_popular_tracks())

pprint(get_top5_album_by_genre("Jazz"))

pprint(get_recommend_album_by_follow(400))

pprint(get_user_recommendations_by_artist(349))