function trend_artist_render(ArtistInfo) {
    let content = '';
    content += ''
    for (let n = 1; n <= 7; n++) {
        // Append HTML for each artist card with dynamic image and album info
        content += `
      <div class="artist-card">
        <img src="/static/img/fig${n}.jpeg" alt="Artist Image ${n}">
        <a href="/artist/${ArtistInfo[n - 1]['ArtistID']}">
            <div class="artist-info">
                <h3>${ArtistInfo[n - 1]['ArtistName']}</h3>
            </div>
        </a>
      </div>
    `;
    }

    return content;
}

fetchDataWithCache('http://localhost:8000/api/index/10', "index")
    .then(data => {
        const renderPromises = [
            renderWrapper(document.getElementById('top-artists-container'), trend_artist_render(data['TopArtists'])),
            renderWrapper(document.getElementById('top-album-container'), trend_album_render(data['TopAlbum'])),
        ];

        return Promise.all(renderPromises)
    })
    .catch(error => {
        console.error('There was a problem with your fetch operation:', error);
        navigateTo("/404");
    });


// Cleanup function
window.currentCleanup = function () {
    return "do nothing";
}