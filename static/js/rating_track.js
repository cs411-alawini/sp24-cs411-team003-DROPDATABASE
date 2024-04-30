function getCookie(name) {
    let value = "; " + document.cookie;
    let parts = value.split("; " + name + "=");
    if (parts.length === 2) return parts.pop().split(";").shift();
}

function fetchUserID(username) {
    return fetch(`/api/get_userid/${username}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to fetch user ID');
            }
            return response.json();
        });
}

function submitTrackRating() {
    const trackRating = document.getElementById('trackRating').value;
    const trackId = window.location.pathname.split('/')[3];
    const username = getCookie("token").split("|")[0];
    
    fetchUserID(username)
        .then(userId => {
            return fetch(`/api/rate/track/${trackId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ user_id: userId, rating: trackRating })
            });
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to submit rating');
            }
            return response.json();
        })
        .then(data => {
            alert(data.message || 'Rating submitted successfully');
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error: ' + error.message);
        });
}
