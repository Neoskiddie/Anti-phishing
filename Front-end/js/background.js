var is_enabled = true // this variable is responsible for keeping whether the URLs are checked for phishing, corresponds to "enabled" storage variable
var whitelist = []// also local variable corresponding to storage "whitelist" with list of whitelisted websites.

// filter all url types and only the main frame (a document that is loaded for a top-level frame) - https://stackoverflow.com/questions/36207557/chrome-webrequest-listening-to-only-user-entered-urls
const filter = { urls: ["http://*/*", "https://*/*"], types: ['main_frame'] };
const opt_extraInfoSpec = ["blocking"];


/**
 * Check if URL is malicious by calling the backend server API
 * The method returns false whenever error hapens to avoid
 * blocking browsign experience. 
 */
function IsURLMalicious(URL) {
    // backend has a hardcoded response for http://notreal.test to be a malicious website
    const serverUrl = "http://127.0.0.1:5000/check?url=" // TODO: Move API to the remote server. 
    const encodedUrl = encodeURIComponent(URL);
    try {
        var rawResponse = httpGet(serverUrl + encodedUrl)
    } catch (err) {
        let confirmAction = confirm("The anti-phishing server is unavailable.\nWould you like to disable the extension?");
        if (confirmAction) {
            const enabled = false
            chrome.storage.local.set({ enabled });
            alert("Extension disabled. You can enable it again in the extension settings.");
        } else {
          alert("Action canceled");
        }
        console.log(err);
        return false;
    }
    if (rawResponse.status === 200) {
        console.log(rawResponse.responseText)
        const response = JSON.parse(rawResponse.responseText);
        // convert string from the json response to boolean
        return response.answer === 'true';
    } else {
        console.log("Error", rawResponse.statusText);
        return false;
    }
}

/** 
 * From: https://stackoverflow.com/questions/247483/http-get-request-in-javascript
 * Using deprecated synchronous request. However, for the purpose of anti-phishing
 * it makes sens to block main thread and wait for the response from the serve.
 */
function httpGet(url) {
    const xmlHttpRequest = new XMLHttpRequest();
    xmlHttpRequest.open("GET", url, false); // true for asynchronous, false for synchronous
    xmlHttpRequest.send(null);
    return xmlHttpRequest;
}

/**
 * Function called befor a request is made by the browser
 * Calls the IsURLMalicious and depending on resonse
 * redirects to the warning page.
 */
const callback = function (requestDetails) {
    const url = requestDetails.url;
    const hostname = new URL(url).hostname;

    let isHostnameWhitelisted = false;


    if (Array.isArray(whitelist) && whitelist.find(domain => hostname.includes(domain))) {
        isHostnameWhitelisted = true;
    }
    console.log('isEnabled is: ' + is_enabled)
    console.log('is hostname whitelisted: ' + isHostnameWhitelisted)

    if (!is_enabled || isHostnameWhitelisted) {
        return;
    }

    const isMalicious = IsURLMalicious(url);
    if (isMalicious) {
        let warningUrl = chrome.extension.getURL("../html/warning.html")
        warningUrl = warningUrl + "?originalurl=" + url
        return { redirectUrl: warningUrl }
    }
}

/**
 * Method fired when the extension is installed.
 * Sets the whitelist to my website and enables the checking of the URLs. 
 */
chrome.runtime.onInstalled.addListener(function () {
    chrome.storage.local.get(["whitelist", "enabled"], function (local) {
        if (!Array.isArray(local.whitelist)) {
            chrome.storage.local.set({ whitelist: ["gbronka.com"] });
        }

        if (typeof local.enabled !== "boolean") {
            chrome.storage.local.set({ enabled: true });
        }
    });
});

/**
 * Called whenever change is made to storage values
 * It logs the values to console and also passes the values to local variables
 */
chrome.storage.onChanged.addListener(function (changes) {
  for (let [key, { newValue }] of Object.entries(changes)) {
    console.log("New value for key " + key + " is: " + newValue);
    if (key === "enabled"){
            is_enabled = newValue
       }
       if (key === "whitelist") {
        whitelist = newValue
       }
  }
});

// callback and filter must be specified
// If the optional opt_extraInfoSpec array contains the string 'blocking', the callback function is handled synchronously.
// In case of anti-phishing extension this is desired bahaviour to process this synchronously.
chrome.webRequest.onBeforeRequest.addListener(callback, filter, opt_extraInfoSpec);