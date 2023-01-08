const queryString = window.location.search;
const urlParams = new URLSearchParams(queryString);
const maliciousUrl = urlParams.get("originalurl");
document.getElementById('maliciousUrl').innerText = maliciousUrl

/**
 * Navigate back in history.
 */
document.getElementById("backButton").onclick = function () {
  history.back()
}

/**
 * Asynchronous method to get value from storage key
 * from https://stackoverflow.com/questions/59440008/how-to-wait-for-asynchronous-chrome-storage-local-get-to-finish-before-continu
 */
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

/**
 * Fired when a button to visit the "malicous" website is pressed.
 * Adds the URL to the whitelist in storage and then navigates to the website.
 */
document.getElementById("visitButton").onclick = async () => {
  const hostname = new URL(maliciousUrl).hostname;
  let whitelist = await readLocalStorage('whitelist');
  whitelist.push(hostname)
  chrome.storage.local.set({ whitelist });
  location.href = maliciousUrl;
};
