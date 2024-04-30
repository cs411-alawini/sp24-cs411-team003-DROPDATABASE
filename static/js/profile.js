console.log("Profile script loaded");
function getCookie(name) {
        var matches = document.cookie.match(new RegExp(
            "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
        ));
        return matches ? decodeURIComponent(matches[1]) : undefined;
    }
function fetchUserID(username) {
    return fetch(`http://127.0.0.1:8000/api/get_userid/${encodeURIComponent(username)}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('User not found');
            }
            return response.json();
        });
}

function fetchData(userID, path, elementID, countElementID) {

    fetch(`http://127.0.0.1:8000/api/user/${userID}` + path)
        .then(response => response.json())
        .then(data => {
            const container = document.getElementById(elementID);
            container.innerHTML = ''; // Clear previous data
            data.forEach(item => {
                const listItem = document.createElement('li');
                listItem.className = 'list-group-item';
                listItem.textContent = item;
                container.appendChild(listItem);
            });
            if (countElementID) {
                // Update the count element
                console.log("length:", data.length);
                document.getElementById(countElementID).textContent = data.length;
            }
        })
        .catch(error => console.error('Error fetching data:', error));
}

function fetchRecommendations(userID) {
    fetch(`http://127.0.0.1:8000/api/recommendations/${userID}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to fetch recommendations');
            }
            return response.json();
        })
        .then(data => {
            const container = document.getElementById('recommendations');
            container.innerHTML = '';  // Clear previous recommendations
            console.log("Recommendations data: ", data);
            if (data.recommendations && data.recommendations.length) {
                data.recommendations.forEach(rec => {
                    console.log("Album ID: ", rec.AlbumID);
                    const listItem = document.createElement('li');
                    listItem.className = 'list-group-item';
                    // Create a link for each album
                    const link = document.createElement('a');
                    link.href = `http://127.0.0.1:8000/album/${rec.AlbumID}`;
                    link.textContent = `${rec.AlbumTitle} by ${rec.ArtistName}`;
                    link.target = "_blank";  // Optional: open in a new tab
                    listItem.appendChild(link);
                    container.appendChild(listItem);
                });
            } else {
                console.log('No recommendations found');
            }
        })
        .catch(error => console.error('Error fetching recommendations:', error));
}

const token = getCookie("token");
const username = token.split("|")[0];
console.log("Username from cookie:", username);

document.querySelector('.username').textContent += `${username}`;

// Fetch the userID based on the username and then fetch other details
fetchUserID(username)
    .then(userID => {
        fetchData(userID, '/followers', 'followers', 'followers-count');
        fetchData(userID, '/following', 'following', 'following-count');
        fetchData(userID, '/playlists', 'playlists', 'playlist-count');
        fetchRecommendations(userID);
        document.getElementById('add-friend-btn').addEventListener('click', function() {
            const friendUserID = document.getElementById('friend-user-id').value;
            const followerID = userID; // You need to obtain the logged-in user's ID
            console.log("I clicked");

            fetch(`http://127.0.0.1:8000/api/user/${followerID}/follow/${friendUserID}`, {
                method: 'POST'
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Failed to add friend');
                }
                return response.json();
            })
            .then(data => {
                alert('Friend added successfully!');
                // Clear input
                location.reload()
                document.getElementById('friend-user-id').value = '';
            })
            .catch(error => {
                console.error('Error adding friend:', error);
                alert(error);
            });
        });


        document.getElementById('create-playlist-btn').addEventListener('click', function() {
            const playlistName = document.getElementById('playlist-name').value;
            fetch(`http://127.0.0.1:8000/api/user/${userID}/playlist/add/${playlistName}`, {
                method: 'POST',
            })
            .then(data => {
                alert(`playlist ${playlistName} created`)
                location.reload()
            })
            .catch(error => {
                console.error('Error creating playlist:', error);
                alert(error);
            });
        });

        document.getElementById('delete-playlist-btn').addEventListener('click', function() {
            const playlistName = document.getElementById('playlist-name').value;
            fetch(`http://127.0.0.1:8000/api/user/${userID}/playlist/remove/${playlistName}`, {
                method: 'POST',

            })
            .then(response => {
                console.log(response); // Check the raw response
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                console.log(data); // Check the parsed data
                location.reload()
                alert(data.message || 'No message received');
            })
            .catch(error => {
                console.error('Error removing playlist:', error);
                alert(error);
            });
        });


    });




