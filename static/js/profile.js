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

const token = getCookie("token");
const username = token.split("|")[0];
console.log("Username from cookie:", username);

document.querySelector('.username').textContent += `${username}`;

// Fetch the userID based on the username and then fetch other details
fetchUserID(username)
    .then(userID => {
        fetchData(userID, '/followers', 'followers', 'followers-count');
        fetchData(userID, '/following', 'following', 'following-count');
        fetchData(userID, '/playlists', 'playlists');
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
        document.getElementById('friend-user-id').value = '';
    })
    .catch(error => {
        console.error('Error adding friend:', error);
        alert(error);
    });
});
    });
    // .catch(error => {
    //     console.error('Error fetching user ID:', error);
    // });


