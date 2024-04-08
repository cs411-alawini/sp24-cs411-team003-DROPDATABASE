from utils import Config, LocalSQL
import os
import pandas as pd

config = Config().config
db = LocalSQL()

directory = config['data']['dir']

tables_order = [
    'User', 'Artist', 'Album', 'Genre', 'Track',
    'PlayList', 'ArtistAlbum', 'AlbumGenre', 'RateTrack',
    'RateAlbum', 'UserFollow', 'ContainTracks'
]

try:
    for table_name in tables_order:
        filename = f"{table_name}.csv"
        file_path = os.path.join(directory, filename)
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            df.fillna("missing", inplace=True)
            records = df.to_dict(orient='records')

            columns = ', '.join(records[0].keys())
            placeholders = ', '.join(['%s'] * len(records[0]))
            insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

            for record in records:
                db.execute(insert_query, list(record.values()))
            db.commit()
            print(f"Data from {filename} inserted into {table_name}.")
        else:
            print(f"No CSV file found for {table_name}, skipping.")


except Exception as e:
    print(f"An error occurred: {e}")
    db.rollback()
finally:
    db.close()