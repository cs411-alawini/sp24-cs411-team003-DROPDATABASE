/*
    The module to rendering the album page
    block when loading html

*/

function trend_artist_render(name) {
    console.log(name)
    let content = '';
    content += name

    return content;
}

function render_album_card(title, artist_name) {
    let content =  `
      <div class="col-md-3 col-sm-6">
        <div class="card">
          <img src="/static/img/card1.jpeg" class="card-img-top" alt="Album Card">
          <div class="card-body">
            <h5 class="card-title">${title}</h5>
            <p class="card-text">${artist_name}</p>
          </div>
          </a>
        </div>
      </div>
    `;

    return content;
}



// END RENDERING HELPERS
function render_album(album_id) {
    rt = 'http://localhost:8000/api/album/' + album_id;
    console.log(route);
    fetchDataWithCache('http://localhost:8000/api/album/' + album_id, "album")
        .then(data => {
            const renderPromises = [
                renderWrapper(document.getElementById('album-card'), render_album_card(data['AlbumTitle'], data['ArtistName']))
            ];

            return Promise.all(renderPromises)
        })
        .catch(error => {
            console.error('There was a problem with your fetch operation:', error);
            navigateTo("/404");
        });
}

// Cleanup function
window.currentCleanup = function () {
    return "do nothing";
}