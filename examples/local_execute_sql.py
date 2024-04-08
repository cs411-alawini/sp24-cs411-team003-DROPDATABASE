from utils import LocalSQL


def test_insert_album(db_manager, album_title, release_date):
    try:
        insert_query = "INSERT INTO album (AlbumTitle, ReleaseDate) VALUES (%s, %s)"
        db_manager.execute(insert_query, (album_title, release_date))
        db_manager.commit()
        print("Insert successful and committed.")
    except Exception as e:
        print(f"Insert failed with error: {e}")
        db_manager.rollback()
        print("Rollback successful.")


def test_failed_insert(db_manager, album_title, release_date):
    try:
        # Intentionally using a wrong column name to force an error
        insert_query = "INSERT INTO album (WrongColumnName, ReleaseDate) VALUES (%s, %s)"
        db_manager.execute(insert_query, (album_title, release_date))
        db_manager.commit()
    except Exception as e:
        print(f"Insert failed with error: {e}")
        db_manager.rollback()
        print("Rollback successful.")


# Create an instance of the DatabaseManager
db_manager = LocalSQL()

# Test case: Successful insert
test_insert_album(db_manager, "Test Album", "2024-01-01")

# Test case: Failed insert and rollback
test_failed_insert(db_manager, "Test Album", "2024-01-01")
