/*
    The module to rendering the index page
    block when loading html

*/

function sampleRender() {
  return `
    <a target="_blank" href="https://picnicss.com/documentation">Picnic document</a>
    `
}

// END RENDERING HELPERS
// fetchDataWithCache('http://localhost:3000/index', "index")
//   .then(data => {
//     const renderPromises = [
//       renderWrapper(document.getElementById('cover-article-container'), sampleRender()),
//     ];

//     return Promise.all(renderPromises)
//   })
//   .catch(error => {
//     console.error('There was a problem with your fetch operation:', error);
//     navigateTo("/404");
//   });

renderWrapper(document.getElementById('sample-block'), sampleRender())

// Cleanup function
window.currentCleanup = function () {
  return "do nothing";
}