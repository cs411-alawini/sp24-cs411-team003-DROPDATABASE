from database.models import *
from utils import LocalSQL, err_handler

sql_cur = LocalSQL()


@err_handler
def get_top5_album_by_genre(genre: str) -> list[AlbumRating]:
    # This query returns the top 5 rated albums within a specific genre, using joins, aggregation, and sub queries.

    sql = '''
    SELECT a.AlbumTitle, AVG(ra.Rating) as AvgRating
        FROM Album a
        JOIN AlbumGenre ag ON a.AlbumID = ag.AlbumID
        JOIN RateAlbum ra ON a.AlbumID = ra.AlbumID
        WHERE ag.GenreName = %s
        GROUP BY a.AlbumID
        ORDER BY AvgRating DESC
        LIMIT 5
    '''

    rows = sql_cur.execute(sql, (genre,))
    return rows


@err_handler
def get_user_recommendations_by_artist(user_id: int) -> AlbumRecommendationList:
    # This query finds albums by artists that a user has highly rated but hasn't rated yet, using joins and
    # sub queries. It assumes a user rates an album they like.

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


def get_most_popular_tracks() -> PopularTracksResponse:
    # This query aggregates data to find the most popular tracks across all genres, based on the average rating,
    # using joins and group by.

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


@err_handler
def get_recommend_album_by_follow(user_id: int) -> list[AlbumRating]:
    # This query recommends new music (albums) to a user based on the albums rated by the users they follow,
    # employing joins and sub queries.

    sql = '''
    SELECT a.AlbumTitle, AVG(ra.Rating) AS AvgRating
        FROM RateAlbum ra
        JOIN Album a ON ra.AlbumID = a.AlbumID
        WHERE ra.UserID IN (
            SELECT FollowID FROM UserFollow WHERE UserID = %s
        )
        GROUP BY ra.AlbumID
        ORDER BY AvgRating DESC, COUNT(ra.UserID) DESC
        LIMIT 10;
    '''

    rows = sql_cur.execute(sql, (user_id,))
    print(rows)
    return rows
