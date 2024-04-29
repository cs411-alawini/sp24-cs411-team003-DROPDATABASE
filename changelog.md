# Changelog

29/04/2024: please execute the procedure/trigger/transaction sql define below to make corresponded backend functon worked


```sql
CREATE TRIGGER round_rating
BEFORE INSERT ON RateTrack
FOR EACH ROW
BEGIN
    IF NEW.Rating > 5 THEN
        SET NEW.Rating = 5;
    ELSEIF NEW.Rating < 1 THEN
        SET NEW.Rating = 1;
    END IF;
END;

CREATE TRIGGER round_rating_album
BEFORE INSERT ON RateAlbum
FOR EACH ROW
BEGIN
    IF NEW.Rating > 5 THEN
        SET NEW.Rating = 5;
    ELSEIF NEW.Rating < 1 THEN
        SET NEW.Rating = 1;
    END IF;
END;

# CALL AddAlbum('New Album', 1, NOW());

CREATE PROCEDURE rateAlbum(IN user_id INT, IN album_id INT, IN rating INT)
BEGIN
    DECLARE rating_count INT;

    -- Begin transaction
    START TRANSACTION;

    -- Check if the user has already rated the album
    SELECT COUNT(*)
    INTO rating_count
    FROM RateAlbum
    WHERE UserID = user_id AND AlbumID = album_id;

    IF rating_count > 0 THEN
        -- If the user has already rated the album, update the rating
        UPDATE RateAlbum
        SET Rating = rating
        WHERE UserID = user_id AND AlbumID = album_id;
    ELSE
        -- If the user hasn't rated the album before, insert a new rating
        INSERT INTO RateAlbum (UserID, AlbumID, Rating)
        VALUES (user_id, album_id, rating);
    END IF;

    -- Commit transaction
    COMMIT;
END;

```