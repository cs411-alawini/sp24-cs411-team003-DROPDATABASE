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
    });
    // .catch(error => {
    //     console.error('Error fetching user ID:', error);
    // });