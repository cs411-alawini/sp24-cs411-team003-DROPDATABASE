from database.models import *
from utils import LocalSQL, err_handler

sql_cur = LocalSQL()


@err_handler
def get_recommend_album_by_user_id(user_id: int) -> AlbumRecommendationList:
    # take the user id as input, return the AlbumRecommendationList

    # example start

    sql = '''
    SELECT DISTINCT a.AlbumTitle, ar.ArtistName
    FROM ArtistAlbum aa
    JOIN Album a ON aa.AlbumID = a.AlbumID
    JOIN Artist ar ON aa.ArtistID = ar.ArtistID
    WHERE ar.ArtistID IN (
        SELECT aa2.ArtistID
            FROM RateAlbum ra
            JOIN ArtistAlbum aa2 ON ra.AlbumID = aa2.AlbumID
            WHERE ra.UserID = %s AND ra.Rating >= 4
            GROUP BY aa2.ArtistID
    )
    AND a.AlbumID NOT IN (
        SELECT AlbumID FROM RateAlbum WHERE UserID = %s
    )
    LIMIT 10;
    '''

    rows = sql_cur.execute(sql, (user_id, user_id))
    return AlbumRecommendationList(recommendations=rows)

    # example end

