from database.models import *
from utils import LocalSQL, err_handler

sql_cur = LocalSQL()

def test_trigger():

    sql = '''
    SELECT t.TrackName, AVG(rt.Rating) AS AvgRating
        FROM Track t
        JOIN RateTrack rt ON t.TrackID = rt.TrackID
        JOIN AlbumGenre ag ON t.AlbumID = ag.AlbumID
        GROUP BY t.TrackID
        ORDER BY AvgRating DESC
        LIMIT 5;
    '''
    tracks = sql_cur.execute(sql)
    return PopularTracksResponse(tracks=tracks)
