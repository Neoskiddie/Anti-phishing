const queryString = window.location.search;
console.log(queryString);
const urlParams = new URLSearchParams(queryString);
const maliciousUrl = urlParams.get("originalurl");
console.log(maliciousUrl);
document.getElementById('maliciousUrl').innerText = maliciousUrl

document.getElementById("backButton").onclick = function () {
  history.back()
}

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

document.getElementById("visitButton").onclick = async () => {
  const hostname = new URL(maliciousUrl).hostname;
  let whitelist = await readLocalStorage('whitelist');
  whitelist.push(hostname)
  chrome.storage.local.set({ whitelist });
  location.href = maliciousUrl;
};
