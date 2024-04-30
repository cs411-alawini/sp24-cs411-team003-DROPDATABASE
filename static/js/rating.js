function submitRating() {
    const albumRating = document.getElementById('albumRating').value;
    const albumId = window.location.pathname.split('/')[3]; 
    const username = getCookie("token").split("|")[0];
    fetchUserID(username)
        .then(userId => {
            fetch(`/api/rate/album/${albumId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ user_id: userId, rating: albumRating })
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
                console.error('Error rating album:', error);
                alert('Error rating album: ' + error.message);
            });
        })
        .catch(error => {
            console.error('Error fetching user ID:', error);
            alert('Error fetching user ID: ' + error.message);
        });
}