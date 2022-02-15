
// Check if URL is malicious by calling the backend server API
function IsURLMalicious(URL) {
  // for now backend has hardcoded response for http://notreal.test to be a malicious website
  const serverUrl = "http://127.0.0.1:5000/check?url="
  const encodedUrl = encodeURIComponent(URL);
  try {
    var rawResponse = httpGet(serverUrl + encodedUrl)
  } catch (err) {
    // TODO display error message to user
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

// Function called befor a request is made by the browser
const callback = function (requestDetails) {
  const url = requestDetails.url;//should use something like encodeURIComponent()
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

