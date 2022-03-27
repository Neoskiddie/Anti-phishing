var is_enabled = true // this variable is responsible for keeping whether the URLs are checked for phishing, corresponds to "enabled" storage variable
var whitelist // also local variable corresponding to storage "whitelist" with list of whitelisted websites.

chrome.runtime.onInstalled.addListener(function () {
    chrome.storage.local.get(["whitelist", "enabled"], function (local) {
        if (!Array.isArray(local.whitelist)) {
            chrome.storage.local.set({ whitelist: [] });
        }

        if (typeof local.enabled !== "boolean") {
            chrome.storage.local.set({ enabled: true });
        }
    });
});

// Check if URL is malicious by calling the backend server API
function IsURLMalicious(URL) {
    // backend has a hardcoded response for http://notreal.test to be a malicious website
    console.log('IsURLMalicious')
    const serverUrl = "http://127.0.0.1:5000/check?url="
    const encodedUrl = encodeURIComponent(URL);
    try {
        var rawResponse = httpGet(serverUrl + encodedUrl)
    } catch (err) {
        alert('The extension server is unavailable!')
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

/*
 From: https://stackoverflow.com/questions/247483/http-get-request-in-javascript
 For now using deprecated synchronous request. However, for the purpose of anti-phishing
 it makes sens to block main thread and wait for the response from the serve.
 */
function httpGet(url) {
    const xmlHttpRequest = new XMLHttpRequest();
    xmlHttpRequest.open("GET", url, false); // true for asynchronous, false for synchronous
    xmlHttpRequest.send(null);
    return xmlHttpRequest;
}
// this method is to get the storage asynchronously
// I didn't understand why I coudn't get the storage and this was a reason.
// So this method solves that by allowing to await the method
// It was found https://stackoverflow.com/questions/59440008/how-to-wait-for-asynchronous-chrome-storage-local-get-to-finish-before-continu
 const readLocalStorage = async (key) => {
    return new Promise((resolve, reject) => {
      chrome.storage.local.get([key], function (result) {
        if (result[key] === undefined) {
          reject();
        } else {
          resolve(result[key]);
        }
      });
    });
  };
// fuction called whenever change is made to storage values
// It logs the values to console and also passes the values to local variables
chrome.storage.onChanged.addListener(function (changes, namespace) {
  for (let [key, { oldValue, newValue }] of Object.entries(changes)) {
    console.log(
      `Storage key "${key}" in namespace "${namespace}" changed.`,
      `Old value was "${oldValue}", new value is "${newValue}".`
    );
    if (key === "enabled"){
            is_enabled = newValue
       }
       if (key === "whitelist") {
        whitelist = newValue
       }
  }
});

// Function called befor a request is made by the browser
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
    //chrome.storage.local.get(["whitelist", "enabled"], function (local) {
    //    const { whitelist, enabled } = local;
    //    isEnabled = enabled;



    const isMalicious = IsURLMalicious(url);
    if (isMalicious) {
        let warningUrl = chrome.extension.getURL("../html/warning.html")
        warningUrl = warningUrl + "?originalurl=" + url
        return { redirectUrl: warningUrl }
    }
}
// filter all url types and only the main frame (a document that is loaded for a top-level frame) - https://stackoverflow.com/questions/36207557/chrome-webrequest-listening-to-only-user-entered-urls
const filter = { urls: ["http://*/*", "https://*/*"], types: ['main_frame'] };

const opt_extraInfoSpec = ["blocking"];

// callback and filter must be specified
// If the optional opt_extraInfoSpec array contains the string 'blocking', the callback function is handled synchronously.
chrome.webRequest.onBeforeRequest.addListener(callback, filter, opt_extraInfoSpec);