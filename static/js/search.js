

const path = window.location.pathname;
const regex = /^\/search\/(.+)$/;

// Test the current path against the regex
const match = path.match(regex);
var query;

if (match) {
    query = match[1];
} else {
    query = match[0];
}

console.log("query is" + query)

document.getElementById("search-hint").innerText = `Result for Album like '${query}'`


function album_renderer(AlbumInfo) {
    let content = '';
    for (let n = 0; n < AlbumInfo.length; n++) {
        // Append HTML for each artist card with dynamic image and album info
        content += `
      <div class="col-md-3 col-sm-6">
        <div class="card">
          <img src="${AlbumInfo[n]['AlbumCover'] + '?rand=' + Math.random().toString()}" class="card-img-top" alt="Baby Gravy Mix">
          <a href="/album/${AlbumInfo[n]['AlbumID']}">
          <div class="card-body">
            <h5 class="card-title">${AlbumInfo[n]['AlbumTitle']}</h5>
            <p class="card-text">${AlbumInfo[n]['ArtistName']}</p>
          </div>
          </a>
        </div>
      </div>
    `;
    }

    return content;
}


fetchDataWithCache(`http://localhost:8000/api/search/${query}`, "search")
    .then(data => {

        const renderPromises = [
            renderWrapper(document.getElementById('top-album-container'), album_renderer(data)),
        ];

        return Promise.all(renderPromises)
    })


// Cleanup function
window.currentCleanup = function () {
    return "do nothing";
}