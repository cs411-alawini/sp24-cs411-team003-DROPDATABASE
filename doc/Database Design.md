## Conceptual Design

We choose  to use Entity-Relationship Diagram for out conceptual design, you can find the diagram in [ER_diagram.md](./ER_diagram.md)

## Assumption

####  Entities:

- **User**: The assumption is that each individual will have a unique account with attributes that are personal and require privacy, such as email and password. A User entity is necessary because users will interact with the system in complex ways, such as creating playlists, following other users, and rating albums or tracks.
- **Album**: An Album is a collection of tracks, and it's more than just an attribute of a track because it has its own set of attributes like title and release date. Albums are linked to artists, but they are separate entities because an artist can have multiple albums, and albums can feature multiple artists.
- **Track**: A Track represents an individual song or piece of music. It's a separate entity from Album because while a track is part of an album, it also has independent attributes such as its title and duration. Additionally, a track could be released as a single or be part of multiple albums in the case of compilations or re-releases.
- **Artist**: An Artist could be an individual or a group that performs or creates music. This entity is separate from Track and Album because artists are not attributes of music but creators that can be linked to multiple works across various albums and tracks.
- **Genre**: Genre is used to categorize music and is an entity because it applies to both albums and tracks. It is not an attribute of either since a genre does not define a track or an album, but rather groups them into a wider music classification system.
- **Playlist**: A Playlist is a user-created list of tracks. It is an entity because it represents a collection with properties such as a name and potentially a description. It also has a many-to-many relationship with tracks since a playlist can contain multiple tracks, and a track can be in multiple playlists.
- **Album_Rating**: The assumption is that users may provide a numerical rating for any album they listen to. An Album_Rating entity is needed to store this information. Each record in this entity represents a unique instance of a user providing a rating for an album, and therefore it has a composite primary key consisting of both the user's ID and the album's ID.
- **Track_Rating**: Track_rating assumed that users may want to rate individual tracks. The Track_Rating entity captures these ratings. As with album ratings, each track rating is a unique occurrence of a user assigning a rating to a track. The primary key for this entity is also composite, made up of the user's ID and the track's ID.
#### Relationships:

- **User -> Album_Rating**: The relationship is many-to-many, implemented through an Album_Rating junction table, as users can rate multiple albums, and albums can have ratings from multiple users.
- **User -> Playlist**: A one-to-many relationship exists here because a user can create several playlists, but each playlist is uniquely associated with one user.
- **Album -> Track**: This is a one-to-many relationship because an album contains multiple tracks, but each track is associated with only one album.
- **Track -> Artist**: A many-to-many relationship is assumed here because a track may have multiple artists, and artists can contribute to multiple tracks.
- **Album -> Genre**: Also many-to-many, since albums often fall into multiple genres, and a genre encompasses many albums.
- **User -> Track_Rating**: This is another many-to-many relationship facilitated by a Track_Rating junction table, allowing users to rate many tracks and tracks to receive ratings from many users.
- **Playlist -> Track**: This relationship is many-to-many since playlists consist of multiple tracks, and a single track can appear in several different user-created playlists.

These assumptions stem from the understanding that users have complex interactions with music data, and the entities need to reflect the multifaceted nature of these interactions within the system. Each entity is modeled to capture a unique aspect of the music domain that cannot be reduced to mere attributes of another entity, ensuring the database is normalized and scalable.

##  Database Normalization

The schema adheres to 3NF across all tables. Each table ensures that:

- All attributes contain only atomic values.
- There is a full functional dependency of non-key attributes on the primary key.
- There are no transitive dependencies of non-key attributes on any other non-key attributes.

Given this analysis, there seems to be no need to apply BCNF, as all functional dependencies already have their left-hand side as a superkey, which complies with the BCNF requirements. 

## Logical Design

- User(UserID: INT [PK], Username: VARCHAR(50), Password: VARCHAR(100))
- Album(AlbumID: INT [PK], Title: VARCHAR(100), ArtistID: INT [FK to Artist.ArtistID], ReleaseDate: DATE)
- Track(TrackID: INT [PK], AlbumID: INT [FK to Album.AlbumID], Title: VARCHAR(100), Duration: DECIMAL)
- Artist(ArtistID: INT [PK], Name: VARCHAR(100))
- Genre(GenreID: INT [PK], Name: VARCHAR(50))
- Playlist(PlaylistID: INT [PK], UserID: INT [FK to User.UserID], Name: VARCHAR(100))
- Album_Rating(UserID: INT [FK to User.UserID], AlbumID: INT [FK to Album.AlbumID], Rating: INT)
- Track_Rating(UserID: INT [FK to User.UserID], TrackID: INT [FK to Track.TrackID], Rating: INT)
