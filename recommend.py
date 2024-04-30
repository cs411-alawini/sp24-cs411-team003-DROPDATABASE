from database.models import *
from utils import LocalSQL, err_handler
import numpy as np

sql_cur = LocalSQL()

def get_markov_chain():
    sql = '''
    SELECT UserID
    FROM User
    '''

    result = sql_cur.execute(sql)
    users = [result[i]['UserID'] for i in range(len(result))]

    sql = '''SELECT UserId, GROUP_CONCAT(AlbumId SEPARATOR ',') AS AlbumIds, GROUP_CONCAT(Rating SEPARATOR ',') AS Ratings
            FROM RateAlbum
            GROUP BY UserId;
            '''

    data = sql_cur.execute(sql)

    user_data = {}
    for d in data:
        album_ids = d['AlbumIds'].split(",")
        ratings = d['Ratings'].split(",")
        
        album_ids = [float(x) for x in album_ids]
        ratings = [float(x) for x in ratings]

        user_data[d['UserId']] = {album_ids[i]: ratings[i] for i in range(len(album_ids))}
    

    user_similarity = np.zeros((len(users), len(users)))
    for user_i in users:
        if (user_i in user_data.keys()):
            user_i_albums = user_data[user_i]
            #print(user_i_albums)
        
        for user_j in users:
            if (user_j in user_data.keys() and user_i != user_j):
                user_j_albums = user_data[user_j]
                #print(user_j_albums)

                dot = 0
                for album in user_i_albums.keys():
                    if (album in user_j_albums.keys()):
                        dot += user_i_albums[album] * user_j_albums[album]
                
                norm_prd = np.linalg.norm(list(user_i_albums.values())) * np.linalg.norm(list(user_j_albums.values()))
                sim = dot / max(norm_prd, 0.00000001)
                user_similarity[user_i-1][user_j-1] = sim

    user_similarity = np.array(user_similarity)
    norms = np.linalg.norm(user_similarity, axis=1, keepdims=True)
    norms[norms == 0] = 1

    user_similarity = user_similarity / norms
    return user_similarity

def next_state(states, transition_matrix, current_state):
        next_state_index = np.random.choice(len(states), transition_matrix[current_state])
        return states[next_state_index]

def predict_album_ids(transition_matrix, user_id):
    current_state = transition_matrix[user_id-1]
    num_steps = 10
    #trajectory = [current_state]

    for _ in range(num_steps):
        current_state = np.dot(current_state, transition_matrix)
        print(np.argsort(current_state))
    
    return np.argsort(current_state)


@err_handler
def get_recommend_album_by_user_id(user_id: int) -> AlbumRecommendationList:
    # take the user id as input, return the AlbumRecommendationList

    # example start
    transition_matrix = get_markov_chain()
    user_ids = list(predict_album_ids(transition_matrix, user_id))

    album_reccomendations = []
    i = 0
    while (len(album_reccomendations) < 10):
        sql = '''
        SELECT DISTINCT a.AlbumTitle, GROUP_CONCAT(ar.ArtistName SEPARATOR ',') AS ArtistName
        FROM ArtistAlbum aa
        JOIN Album a ON aa.AlbumID = a.AlbumID
        JOIN Artist ar ON aa.ArtistID = ar.ArtistID
        JOIN RateAlbum ra ON ra.AlbumID = a.AlbumID
        WHERE ra.UserID = %s AND ra.Rating >= 3
        GROUP BY a.AlbumTitle;
        '''

        rows = sql_cur.execute(sql, (int(user_ids[i]),))
        for row in rows:
            album_reccomendations.append(row)

        i += 1

    print(album_reccomendations)
    return AlbumRecommendationList(recommendations=rows)


get_recommend_album_by_user_id(4)