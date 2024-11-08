const baseEndpoint = 'http://127.0.0.1:8000/api'

// Handle Login
const loginForm = document.getElementById('login-form');
loginForm.addEventListener('submit', handleLogin)

function handleLogin(event) {
    event.preventDefault();
    const loginEndpoint = `${baseEndpoint}/token/`; // JWT token endpoint

    let loginFormData = new FormData(loginForm); // alternatively to the method below, we can attach individual id's to all inout html elements
    let loginObjectData = Object.fromEntries(loginFormData); // but current approach is easily scalabale and more universal

    const options = {
        method: "POST",
        headers: {
            "content-type": "application/json",
        },
        body: JSON.stringify(loginObjectData),
    };

    fetch(loginEndpoint, options) // analogue of requests.post, .then are async Promise handlers
    .then(response => {
        return response.json();
    })
    .then(authData => {
        handleAuthData(authData, getProductList);
    })
    .catch(err => {
        console.log('Error: ', err);
    })
}

function handleAuthData(authData, callback) {
    localStorage.setItem('access', authData.access);
    localStorage.setItem('refresh', authData.refresh);
    if (callback) {
        callback();
    }
}  


// Fetch a list of Products
const contentContainer = document.getElementById('content-container');

function writeToContainer(data) {
    if (contentContainer) {
        contentContainer.innerHTML = "<pre>" + JSON.stringify(data, null, 4) + "</pre>"
    }
}

async function isTokenNotValid(jsonData) {
    if (jsonData.code && jsonData.code === "token_not_valid") {
        const isRefreshed = await refreshJWTToken();  // Wait for refreshJWTToken to complete
        if (isRefreshed) {
            // Return the updated data with the new access token
            return {
                access: localStorage.getItem('access')
            };
        } else {
            localStorage.removeItem('access');
            localStorage.removeItem('refresh');
            alert("Please login again");
            return null;  // Indicate failure to refresh
        }
    }
    return jsonData;  // If token is valid, return the original data
}

function refreshJWTToken() {
    const endpoint = `${baseEndpoint}/token/refresh/`;
    const options = {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            refresh: localStorage.getItem('refresh')
        })
    };
    return fetch(endpoint, options)
        .then(response => {
            if (!response.ok) {
                throw new Error("Failed to refresh token");
            }
            return response.json();
        })
        .then(data => {
            console.log(data);
            localStorage.setItem('access', data.access);  
            return true; // Indicates success
        })
        .catch(error => {
            console.error("Token refresh error:", error);
            return false; // Indicates failure
        });
}

async function getProductList() {
    const lookupEndpoint = `${baseEndpoint}/products/`;

    const options = {
        method: "GET",
        headers: {
            "content-type": "application/json",
            "authorization": `Bearer ${localStorage.getItem('access')}`,
        },
    };

    try {
        const response = await fetch(lookupEndpoint, options);
        const data = await response.json();

        // const validData = await isTokenNotValid(data);  // Await the result of isTokenNotValid
        // if (validData) {
        //     writeToContainer(validData);  // Use the refreshed data if available
        // }

        writeToContainer(data);
    } catch (err) {
        console.log('Error: ', err);
    }
}
 
function handleProductListData(data) {
    console.log(data); // This should handle the fetched product list data
}

// Search with algolia
const searchForm = document.getElementById('search-form');
searchForm.addEventListener('submit', handleSearch);

function handleSearch(event) {
    event.preventDefault();

    let searchFormData = new FormData(searchForm); 
    let searchObjectData = Object.fromEntries(searchFormData); 
    let searchParams = new URLSearchParams(searchObjectData);

    const searchEndpoint = `${baseEndpoint}/search/?${searchParams}`; 

    const headers = {
        "content-type": "application/json",

    };
    const authToken = localStorage.getItem('access');
    if (authToken) {
        headers['Authorization'] = `Bearer ${authToken}`;
    }

    const options = {
        method: "GET",
        headers: headers
    };

    fetch(searchEndpoint, options) // analogue of requests.post, .then are async Promise handlers
    .then(response => {
        return response.json();
    })
    .then(data => {
        writeToContainer(data);
    })
    .catch(err => {
        console.log('Error: ', err);
    })
}

function validateJWTToken() {
    // fetch
    const endpoint = `${baseEndpoint}/token/verify/`
    const options = {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            token: localStorage.getItem('access')
        })
    }
    fetch(endpoint, options)
    .then(response=>response.json())
    .then(x=> {
        isTokenNotValid(x);
    })
}

validateJWTToken();
getProductList();

function getAlgoliaTokens() {
    const endpoint = `${baseEndpoint}/algolia/tokens/`;
    const options = {
        method: "GET",
        headers: {
            "Content-Type": "application/json"
        },
    }

    fetch(endpoint, options)
    .then(response => response.json())
    .then(x => {
        localStorage.setItem('algoliaAppId', x.AppID);
        localStorage.setItem('algoliaApiKey', x.ApiKey);
    })
}

const algoliaAppId = localStorage.getItem('algoliaAppId');
const algoliaApiKey = localStorage.getItem('algoliaApiKey');
const searchClient = algoliasearch(algoliaAppId, algoliaApiKey);

const search = instantsearch({
  indexName: 'drf_Product',
  searchClient,
});

search.addWidgets([
    instantsearch.widgets.searchBox({
      container: '#searchbox',
    }),
  
      instantsearch.widgets.clearRefinements({
      container: "#clear-refinements"
      }),
  
  
    instantsearch.widgets.refinementList({
        container: "#user-list",
        attribute: 'user'
    }),
    instantsearch.widgets.refinementList({
      container: "#public-list",
      attribute: 'public'
  }),
  
  
    instantsearch.widgets.hits({
        container: '#hits',
        templates: {
            item: `
                <div>
                    <div>{{#helpers.highlight}}{ "attribute": "title" }{{/helpers.highlight}}</div>
                    <div>{{#helpers.highlight}}{ "attribute": "body" }{{/helpers.highlight}}</div>
                    
                    <p>{{ user }}</p><p>\${{ price }}
                
                
                </div>`
        }
    })
  ]);  

search.start();

getAlgoliaTokens();
