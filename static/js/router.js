const route = (event) => {
    event = event || window.event;
    event.preventDefault();
    window.history.pushState({}, "", event.target.closest("a").href);
    handleLocation();
};

const routes = {
    404: { html: "/pages/404.html", js: null, css: [], jsr: [] },
    "/": { html: "/pages/index.html", js: "/js/index.js", css: [], jsr: [] },
};

const loadedCSS = {};
const loadedJS = {};

const handleLocation = async () => {
    // cleanup the previous page renderer
    if (window.currentCleanup) {
        const cleaner_name = window.currentCleanup();
        window.currentCleanup = null;
        console.log("clean: " + cleaner_name)
    }

    const path = window.location.pathname;
    let route = routes[path] || routes[404];

    const html = await fetch(route.html).then((data) => data.text());

    // Load CSS
    route.css.forEach(url => {
        if (!loadedCSS[url]) {
            const link = document.createElement('link');
            link.href = url;
            link.type = 'text/css';
            link.rel = 'stylesheet';
            document.head.appendChild(link);

            loadedCSS[url] = true;
            console.log(`load css: ${url}`);
        }
    });

    // Set page content
    document.getElementById("page-content").innerHTML = html;

    // Remove old script
    const oldScript = document.querySelector('.route-script');
    if (oldScript) {
        oldScript.parentNode.removeChild(oldScript);
    }

    // Load JSR files
    await Promise.all(route.jsr.map(url => {
        return new Promise((resolve, reject) => {
            if (!loadedJS[url]) {
                const script = document.createElement("script");
                script.src = url;
                script.onload = resolve;
                script.onerror = reject;
                document.body.appendChild(script);

                loadedJS[url] = true;
                console.log(`load jsr: ${url}`);
            } else {
                resolve(); // If already loaded, resolve immediately
            }
        });
    }));

    // Load JS file after JSR
    if (route.js) {
        console.log("load js: " + route.js);
        const script = document.createElement("script");
        script.src = route.js;
        script.className = 'route-script';
        document.body.appendChild(script);
    }
};

function navigateTo(page) {
    window.history.pushState({}, '', page);
    handleLocation(); 
}

handleLocation();