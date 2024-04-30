function getCookie(name) {
    let value = "; " + document.cookie;
    let parts = value.split("; " + name + "=");
    if (parts.length === 2) return parts.pop().split(";").shift();
}

async function fetchUserID(username) {
    const response = await fetch(`/api/get_userid/${username}`);
    if (!response.ok) {
        throw new Error('Failed to fetch user ID');
    }
    return await response.json();
}

async function postRating(url, body) {
    const response = await fetch(url, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(body)
    });
    if (!response.ok) {
        throw new Error('Failed to submit rating');
    }
    return await response.json();
}


async function submitRating(entity, entityId, ratingId) {
    try {
        const rating = document.getElementById(ratingId).value;
        const entityIdValue = window.location.pathname.split('/')[3];
        const token = getCookie("token")
        if (token === undefined) {
            showAlert('login before rating', 'alert-danger')
        } else {
            const username = token.split("|")[0];
            const userId = await fetchUserID(username);

            console.log(`/api/rate/${entity}/${entityIdValue}`)
            const result = await postRating(`/api/rate/${entity}/${entityIdValue}`, {
                user_id: userId, rating: rating
            });

            showAlert(result.message || 'Rating submitted successfully', 'alert-success');

            // Wait for 2 seconds before redirecting
            setTimeout(async function () {
                if (entity === 'album')
                    window.location.href = `/${entity}/${entityIdValue}`;
                else if (entity === 'track') {
                    const response = await fetch(`/api/aid/${entityIdValue}`, {method: "POST"});
                    const data = await response.json();
                    if (response.ok && data != null) {
                        console.log(`redirect to album ${data}`)
                        window.location.href = `/album/${data}`;
                    }
                }
            }, 2000);
        }
    } catch (error) {
        console.error('Error:', error);
        showAlert('Error: ' + error.message, 'alert-danger');
    }
}

const entityVal = window.location.pathname.split('/')[2];

if (entityVal === 'album') {
    console.log("rate album")
    document.getElementById('submitAlbumRating').addEventListener('click', () => submitRating('album', 'albumId', 'albumRating'));
} else if (entityVal === 'track') {
    console.log('rate track')
    document.getElementById('submitTrackRating').addEventListener('click', () => submitRating('track', 'trackId', 'trackRating'));
} else {
    console.log(entityVal)
}
