chrome.runtime.onInstalled.addListener(function () {
    chrome.storage.local.get(["whitelist", "enabled"], function (local) {
        if (!Array.isArray(local.whitelist)) {
            chrome.storage.local.set({ whitelist: [] });
        }

        if (typeof local.enabled !== "boolean") {
            chrome.storage.local.set({ enabled: false });
        }
    });
});

//chrome.tabs.onUpdated.addListener(function (tabId, changeInfo) {
//    const url = changeInfo.pendingUrl || changeInfo.url;
//    if (!url || !url.startsWith("http")) {
//        return;
//    }
//
//    const hostname = new URL(url).hostname;
//
//    chrome.storage.local.get(["whitelist", "enabled"], function (local) {
//        const { whitelist, enabled } = local;
//        if (Array.isArray(whitelist) && enabled && whitelist.find(domain => hostname.includes(domain))) {
//            chrome.tabs.remove(tabId);
//        }
//    });
//});



// Check if URL is malicious by calling the backend server API
function IsURLMalicious(URL) {
    // for now backend has hardcoded response for http://notreal.test to be a malicious website
    console.log('IsURLMalicious')
    const serverUrl = "http://127.0.0.1:5000/check?url="
    const encodedUrl = encodeURIComponent(URL);
    try {
        var rawResponse = httpGet(serverUrl + encodedUrl)
    } catch (err) {
        // TODO display error message to user
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

// Function called befor a request is made by the browser
const callback = async function (requestDetails) {
    const url = requestDetails.url;
    const hostname = new URL(url).hostname;

    let isEnabled = await readLocalStorage('enabled');
    let whitelist = await readLocalStorage('whitelist');
    let isHostnameWhitelisted = false;


    if (Array.isArray(whitelist) && whitelist.find(domain => hostname.includes(domain))) {
        isHostnameWhitelisted = true;
    }
    console.log('isEnabled is: ' + isEnabled)
    console.log('is hostname whitelisted: ' + isHostnameWhitelisted)

    if (!isEnabled || isHostnameWhitelisted) {
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