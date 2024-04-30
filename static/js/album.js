const path = window.location.pathname;
const regex = /^\/album\/(.+)$/;

// Test the current path against the regex
const match = path.match(regex);
var query;

if (match) {
    query = match[1];
} else {
    query = match[0];
}

console.log("query is" + query)

function render_album_cover(AlbumInfo) {
    return `
        <img src="${AlbumInfo['AlbumCover']}" class="img-fluid rounded-start" alt="Album Cover">
    `
}

function render_album_info(AlbumInfo) {
    return `
        <h5 class="card-title">${AlbumInfo['AlbumTitle']}</h5>
        <p class="card-text"><strong>Artist: </strong>${AlbumInfo['ArtistName']}</p>
        <p class="card-text"><strong>Rating: </strong>${AlbumInfo['Rating'] === null ? '2.5' : AlbumInfo['Rating']}/5</p>
        <p class="card-text"><small class="text-muted">Album ID: ${AlbumInfo['AlbumID']}</small></p>
        <p class="card-text"><small class="text-muted">Artist ID: ${AlbumInfo['ArtistID']}</small></p>    
    `
}

function render_track_info(TrackInfo) {
    console.log(TrackInfo)
    let content = '';
    for (let n = 0; n < TrackInfo.length; n++) {
        content  += `
            <li class="list-group-item d-flex justify-content-between align-items-center">
                ${TrackInfo[n]['TrackName']}
                <span class="badge bg-primary rounded-pill">${TrackInfo[n]['Rating'] === null ? 'no rating' : TrackInfo[n]['Rating']}</span>
            </li>
        `
    }
    return content
}

fetchDataWithCache(`http://localhost:8000/api/album/${query}`, "album")
    .then(data => {
        const renderPromises = [
            renderWrapper(document.getElementById('album-cover'), render_album_cover(data['AlbumInfo'])),
            renderWrapper(document.getElementById('album-info'), render_album_info(data['AlbumInfo'])),
            renderWrapper(document.getElementById('track-info'), render_track_info(data['Tracks'])),
        ];

        return Promise.all(renderPromises)
    })



// Cleanup function
window.currentCleanup = function () {
    return "do nothing";
}