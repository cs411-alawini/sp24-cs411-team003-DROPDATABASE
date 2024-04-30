const path = window.location.pathname;
const regex = /^\/artist\/(.+)$/;

// Test the current path against the regex
const match = path.match(regex);
var query;

if (match) {
    query = match[1];
} else {
    query = match[0];
}

console.log("query is" + query)

function render_album_cover(ArtistInfo) {
    return `
        <img src="${ArtistInfo['ArtistCover']}" class="img-fluid rounded-start" alt="Artist Cover">
    `
}

function render_album_info(ArtistInfo) {
    return `
        <h5 class="card-title">${ArtistInfo['ArtistName']}</h5>
        <p class="card-text"><strong>Rating: </strong>${ArtistInfo['Rating'] === null ? '2.5' : AlbumInfo['Rating']}/5</p>
        <p class="card-text"><small class="text-muted">Artist ID: ${ArtistInfo['ArtistID']}</small></p>    
    `
}

fetchDataWithCache(`http://localhost:8000/api/artist/${query}`, "album")
    .then(data => {
        const renderPromises = [
            renderWrapper(document.getElementById('artist-cover'), render_album_cover(data)),
            renderWrapper(document.getElementById('artist-info'), render_album_info(data)),
        ];

        return Promise.all(renderPromises)
    })



// Cleanup function
window.currentCleanup = function () {
    return "do nothing";
}