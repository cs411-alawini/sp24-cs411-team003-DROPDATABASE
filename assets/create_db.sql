CREATE TABLE Artist (
    ArtistID INTEGER AUTO_INCREMENT,
    ArtistName VARCHAR(256),
    PRIMARY KEY (ArtistID)
);

CREATE TABLE Album (
    AlbumID INTEGER AUTO_INCREMENT,
    AlbumTitle VARCHAR(256),
    ReleaseDate DATETIME,
    PRIMARY KEY (AlbumID)
);

CREATE TABLE Genre (
    GenreName VARCHAR(32) PRIMARY KEY
);

CREATE TABLE ArtistAlbum (
    ArtistID INTEGER,
    AlbumID INTEGER,
    FOREIGN KEY (ArtistID) REFERENCES Artist(ArtistID) ON DELETE CASCADE,
    FOREIGN KEY (AlbumID) REFERENCES Album(AlbumID) ON DELETE CASCADE,
    PRIMARY KEY (ArtistID, AlbumID)
);

CREATE TABLE AlbumGenre (
    AlbumID INTEGER,
    GenreName VARCHAR(32),
    FOREIGN KEY (AlbumID) REFERENCES Album(AlbumID) ON DELETE CASCADE,
    FOREIGN KEY (GenreName) REFERENCES Genre(GenreName) ON DELETE CASCADE,
    PRIMARY KEY (AlbumID, GenreName)
);

CREATE TABLE Track (
    TrackID INTEGER AUTO_INCREMENT,
    TrackName VARCHAR(512),
    AlbumID INTEGER,
    FOREIGN KEY (AlbumID) REFERENCES Album(AlbumID) ON DELETE CASCADE,
    PRIMARY KEY (TrackID)
);

CREATE TABLE User (
    UserID INTEGER AUTO_INCREMENT,
    UserName VARCHAR(32),
    Password VARCHAR(32),
    PRIMARY KEY (UserID)
);

CREATE TABLE RateTrack (
    TrackID INTEGER,
    UserID INTEGER,
    Rating INTEGER, 
    FOREIGN KEY (TrackID) REFERENCES Track(TrackID) ON DELETE CASCADE,
    FOREIGN KEY (UserID) REFERENCES User(UserID) ON DELETE CASCADE,
    PRIMARY KEY (TrackID, UserID)
);

CREATE TABLE RateAlbum (
    AlbumID INTEGER,
    UserID INTEGER,
    Rating INTEGER, 
    FOREIGN KEY (AlbumID) REFERENCES Album(AlbumID) ON DELETE CASCADE,
    FOREIGN KEY (UserID) REFERENCES User(UserID) ON DELETE CASCADE,
    PRIMARY KEY (AlbumID, UserID)
);

CREATE TABLE UserFollow (
    UserID INTEGER,
    FollowID INTEGER,
    FOREIGN KEY (UserID) REFERENCES User(UserID) ON DELETE CASCADE,
    FOREIGN KEY (FollowID) REFERENCES User(UserID) ON DELETE CASCADE,
    PRIMARY KEY (UserID, FollowID)
);

CREATE TABLE PlayList (
    PlayListID INTEGER AUTO_INCREMENT,
    PlayListName VARCHAR(256),
    UserID INTEGER,
    FOREIGN KEY (UserID) REFERENCES User(UserID) ON DELETE CASCADE,
    PRIMARY KEY (PlayListID),
    CONSTRAINT CHK_PlayListName CHECK (PlayListName NOT REGEXP 'DROPDATABASE')
);


CREATE TABLE ContainTracks (
    PlayListID INTEGER,
    TrackID INTEGER,
    FOREIGN KEY (PlayListID) REFERENCES PlayList(PlayListID) ON DELETE CASCADE,
    FOREIGN KEY (TrackID) REFERENCES Track(TrackID) ON DELETE CASCADE,
    PRIMARY KEY (PlayListID, TrackID)
);


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

CREATE TRIGGER round_rating_up
BEFORE UPDATE ON RateTrack
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

CREATE TRIGGER round_rating_album_up
BEFORE UPDATE ON RateAlbum
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
