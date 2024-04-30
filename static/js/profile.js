
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

function fetchPlaylists(userID) {
  fetch(`http://127.0.0.1:8000/api/user/${userID}/playlists`)
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok ' + response.statusText);
      }
      return response.json();
    })
    .then(playlists => {
      const playlistContainer = document.querySelector(".list-group");
      playlistContainer.innerHTML = ''; // Clear existing playlists
      playlists.forEach(playlistName => {
        const listItem = document.createElement('li');
        listItem.className = 'list-group-item';
        listItem.textContent = playlistName;
        playlistContainer.appendChild(listItem);
      });
    })
    .catch(error => console.error('Error fetching playlists:', error));
}


document.addEventListener('DOMContentLoaded', () => {
  const userID = getUserIDFromCookie();
  if (userID) {
    fetchUserProfile();
  }
});
