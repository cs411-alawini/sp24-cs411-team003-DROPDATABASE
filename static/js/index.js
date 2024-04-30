/*
    The module to rendering the index page
    block when loading html

*/

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

function trend_album_render(AlbumInfo) {
    let content = '';
    for (let n = 1; n <= 4; n++) {
        // Append HTML for each artist card with dynamic image and album info
        content += `
      <div class="col-md-3 col-sm-6">
        <div class="card">
          <img src="/static/img/card${n}.jpeg" class="card-img-top" alt="Baby Gravy Mix">
          <a href="/album/${AlbumInfo[n - 1]['AlbumID']}">
          <div class="card-body">
            <h5 class="card-title">${AlbumInfo[n - 1]['AlbumTitle']}</h5>
            <p class="card-text">${AlbumInfo[n - 1]['ArtistName']}</p>
          </div>
          </a>
        </div>
      </div>
    `;
    }

    return content;
}

function rec_album_render(AlbumRecommendationList) {
  let content = '';
  for (let n = 1; n <= 4; n++) {
      // Append HTML for each artist card with dynamic image and album info
      content += `
    <div class="col-md-3 col-sm-6">
      <div class="card">
        <img src="/static/img/card${n}.jpeg" class="card-img-top" alt="Baby Gravy Mix">
        <div class="card-body">
          <h5 class="card-title">${AlbumRecommendationList[n - 1]['AlbumTitle']}</h5>
          <p class="card-text">${AlbumRecommendationList[n - 1]['ArtistName']}</p>
        </div>
        </a>
      </div>
    </div>
  `;
  }

  return content;
}




// END RENDERING HELPERS
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

const t = getCookie("token");
const username = t.split("|")[0];
const user_id = fetchUserID(username)
  .then(user_id => {
  fetchDataWithCache('http://localhost:8000/api/recommend/' + user_id, "recommend")
    .then(data => {
        const renderPromises = [
            renderWrapper(document.getElementById('top-album-container'), trend_artist_render(data))
        ];

        return Promise.all(renderPromises)
    })
    .catch(error => {
        console.error('There was a problem with your fetch operation:', error);
        navigateTo("/404");
    });
  });


// Cleanup function
window.currentCleanup = function () {
    return "do nothing";
}