from database.models import *
from utils import LocalSQL, err_handler

sql_cur = LocalSQL()


def get_index_data(top_n: int) -> IndexData:
    # return the data for rendering index page
    sql_albums = f'''
        SELECT a.AlbumID, a.AlbumTitle, ar.ArtistName
        FROM Album a
        JOIN RateAlbum ra ON a.AlbumID = ra.AlbumID
        JOIN artistalbum a2 ON a.AlbumID = a2.AlbumID
        JOIN artist ar ON a2.ArtistID = ar.ArtistID
        GROUP BY a.AlbumID, a.AlbumTitle, ar.ArtistName
        ORDER BY AVG(ra.Rating) DESC
        LIMIT %s
    '''

    top_albums = sql_cur.execute(sql_albums, (top_n,))

    sql = f'''
        SELECT 
            Artist.ArtistID,
            Artist.ArtistName
        FROM Artist
        JOIN ArtistAlbum ON Artist.ArtistID = ArtistAlbum.ArtistID
        JOIN Album ON ArtistAlbum.AlbumID = Album.AlbumID
        JOIN Track ON Album.AlbumID = Track.AlbumID
        JOIN RateTrack ON Track.TrackID = RateTrack.TrackID
        GROUP BY Artist.ArtistID, Artist.ArtistName
        ORDER BY AVG(RateTrack.Rating) DESC
        LIMIT %s;
    '''

    top_artists = sql_cur.execute(sql, (top_n,))

    print(top_albums)
    print(top_artists)

    album_covers = [AlbumCover(AlbumID=album['AlbumID'], AlbumTitle=album['AlbumTitle'], ArtistName=album['ArtistName'])
                    for album in top_albums]
    artist_covers = [ArtistCover(ArtistID=artist['ArtistID'], ArtistName=artist['ArtistName']) for artist in
                     top_artists]

    return IndexData(TopAlbum=album_covers,
                     TopArtists=artist_covers)


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
    return rows


@err_handler
def get_userinfo(user_name: str) -> Optional[UserInfo]:
    sql = '''
    SELECT *
        FROM User
        WHERE UserName = %s;
    '''

    rows = sql_cur.execute(sql, (user_name,))
    if len(rows) == 0:
        return None

    return UserInfo(
        UserID=rows[0]['UserID'],
        UserName=rows[0]['UserName'],
        Password=rows[0]['Password']
    )


@err_handler
def search_album(query: str) -> List[AlbumCover]:
    sql = '''
    SELECT * FROM Album a
    JOIN artistalbum a2 ON a.AlbumID = a2.AlbumID
    JOIN artist ar ON a2.ArtistID = ar.ArtistID

    WHERE AlbumTitle LIKE %s
    LIMIT 20;
    '''
    search_pattern = f'%{query}%'

    rows = sql_cur.execute(sql, (search_pattern,))

    album_covers = [AlbumCover(AlbumID=album['AlbumID'], AlbumTitle=album['AlbumTitle'], ArtistName=album['ArtistName'])
                    for album in rows]

    return album_covers


@err_handler
def rateAlbum(user_id: int, album_id: int, rating: int):
    try:
        # Call the rateAlbum stored procedure with the provided parameters
        sql_cur.callproc("rateAlbum", (user_id, album_id, rating,))
        # Commit the transaction
        sql_cur.commit()
    except Exception as e:
        # Rollback transaction in case of an error
        sql_cur.rollback()
        raise e


@err_handler
def get_rate_by_userid(user_id: int) -> List[UserAlbumRate]:
    sql = '''
        SELECT RateAlbum.AlbumID, Album.AlbumTitle, RateAlbum.Rating
        FROM RateAlbum
        JOIN Album ON RateAlbum.AlbumID = Album.AlbumID
        WHERE RateAlbum.UserID = %s;
    '''

    rows = sql_cur.execute(sql, (user_id,))

    return [UserAlbumRate(AlbumID=i['AlbumID'], AlbumTitle=i['AlbumTitle'], Rating=i['Rating']) for i in rows]


@err_handler
def get_follower_by_userid(user_id: int) -> List[int]:
    sql = '''
        SELECT UserID
        FROM UserFollow
        WHERE FollowID = %s;
    '''
    rows = sql_cur.execute(sql, (user_id,))
    return [row['UserID'] for row in rows]


@err_handler
def get_following_by_userid(user_id: int) -> List[int]:
    sql = '''
        SELECT FollowID
        FROM UserFollow
        WHERE UserID = %s;
    '''
    rows = sql_cur.execute(sql, (user_id,))
    return [row['FollowID'] for row in rows]


@err_handler
def unfollow_userid(follower_id: int, followee_id: int) -> None:
    sql = '''
        DELETE FROM UserFollow
        WHERE UserID = %s AND FollowID = %s;
    '''
    try:
        sql_cur.execute(sql, (follower_id, followee_id))
        sql_cur.commit()
    except Exception as e:
        sql_cur.rollback()
        raise e


@err_handler
def get_user_playlist(user_id: int) -> List[str]:
    sql = '''
        SELECT PlayListName
        FROM PlayList
        WHERE UserID = %s;
    '''
    rows = sql_cur.execute(sql, (user_id,))
    return [row['PlayListName'] for row in rows]
