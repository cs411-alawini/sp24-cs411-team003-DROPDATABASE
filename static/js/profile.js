
function fetchUserProfile() {
  const userID = document.getElementById("username").value;

  fetchFollowers(userID);
  fetchFollowing(userID);
  // fetchPlaylists(userID);
}

function fetchFollowers(userID) {
  fetch(`http://127.0.0.1:8000/api/user/${userID}/followers`)
    .then(response => response.json())
    .then(data => {
      document.querySelector(".followers-count").innerText = data.length;
    })
    .catch(error => console.error('Error fetching followers:', error));
}

function fetchFollowing(userID) {
  fetch(`http://127.0.0.1:8000/api/user/${userID}/following`)
    .then(response => response.json())
    .then(data => {
      document.querySelector(".following-count").innerText = data.length;
    })
    .catch(error => console.error('Error fetching following:', error));
}

// function fetchPlaylists(userID) {
//   fetch(`http://127.0.0.1:8000/api/user/${userID}/playlists`)
//     .then(response => response.json())
//     .then(data => {
//       const playlistContainer = document.querySelector(".list-group");
//       playlistContainer.innerHTML = ''; // Clear existing playlists
//       data.forEach(playlist => {
//         const listItem = document.createElement('li');
//         listItem.className = 'list-group-item';
//         listItem.textContent = playlist.PlayListName;
//         playlistContainer.appendChild(listItem);
//       });
//     })
//     .catch(error => console.error('Error fetching playlists:', error));
// }

// Call this function when the profile page loads
document.addEventListener('DOMContentLoaded', fetchUserProfile);