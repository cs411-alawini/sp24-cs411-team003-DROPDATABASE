/*
    universal js functionality cross the whole blog,
    will defer loading

*/

function renderWrapper(elementDOM, newHTML) {
    return new Promise((resolve) => {
        setTimeout(() => {
            elementDOM.classList.add('fade-in');
            setTimeout(() => {
                elementDOM.innerHTML = newHTML;
                elementDOM.classList.add('visible');
                resolve();
            }, 230);
        }, 150);
    });
}

AbortSignal.timeout ??= function timeout(ms) {
    const ctrl = new AbortController()
    setTimeout(() => ctrl.abort(), ms)
    return ctrl.signal
}

function cacheData(key, data, exp_hour) {
    const now = new Date().getTime();
    const item = {
        data: data,
        expiry: now + exp_hour * 60 * 60 * 1000,
    };
    localStorage.setItem(key, JSON.stringify(item));
}

function getCachedData(key) {
    const itemStr = localStorage.getItem(key);
    if (!itemStr) {
        return null;
    }
    const item = JSON.parse(itemStr);
    const now = new Date().getTime();
    if (now > item.expiry) {
        localStorage.removeItem(key);
        return null;
    }
    return item.data;
}

async function fetchDataWithCache(url, name, exp_hour = 1) {
    const cachedData = getCachedData(url);
    if (cachedData) {
        return Promise.resolve(cachedData);
    } else {
        console.log(`load data: ${name}`)
        return fetch(url, { signal: AbortSignal.timeout(5000) })
            .then(response => {
                if (!response.ok) {
                    if (response.status === 404) {
                        navigateTo("/404");
                    }
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                cacheData(url, data, exp_hour);
                return data;
            });
    }
}
