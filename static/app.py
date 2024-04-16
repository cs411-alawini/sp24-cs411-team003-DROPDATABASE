from flask import Flask, jsonify, request
from database.crud import (
    get_top5_album_by_genre,
    get_user_recommendations_by_artist,
    get_most_popular_tracks,
    get_recommend_album_by_follow
)
from flask_cors import CORS

app = Flask(__name__)

@app.route('/top5_albums_by_genre/<genre>', methods=['GET'])
def top5_albums_by_genre(genre):
    try:
        albums = get_top5_album_by_genre(genre)
        return jsonify(albums), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/user_recommendations_by_artist/<int:user_id>', methods=['GET'])
def user_recommendations_by_artist(user_id):
    try:
        recommendations = get_user_recommendations_by_artist(user_id)
        return jsonify(recommendations), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/most_popular_tracks', methods=['GET'])
def most_popular_tracks():
    try:
        tracks = get_most_popular_tracks()
        return jsonify(tracks), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/recommend_album_by_follow/<int:user_id>', methods=['GET'])
def recommend_album_by_follow(user_id):
    try:
        recommendations = get_recommend_album_by_follow(user_id)
        return jsonify(recommendations), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
CORS(app)
if __name__ == '__main__':
    app.run(debug=True)
