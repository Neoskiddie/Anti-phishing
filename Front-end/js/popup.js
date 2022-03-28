document.getElementById('options').onclick = openOps;
document.getElementById('about').onclick = openAbout;
var checkbox = document.getElementById("myonoffswitch");

/**
 * Open default option page.
 * Same as right clicking extension icon and selecting options. 
 */
function openOps() {
    chrome.runtime.openOptionsPage()
};

/**
 * Open about page in new tab. 
 */
function openAbout() {
    chrome.tabs.create({ url: 'https://gbronka.com/honours' });
};

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
 * Loads "enabled" from storage and set the checkbox to it's value
 */
window.onload = async () => {
  let enabled = await readLocalStorage('enabled');
  checkbox.checked = enabled;
};

/**
 * Sets the "enabled" in storage when the checbox was changed
 */
checkbox.addEventListener("change", (event) => {
  const enabled = event.target.checked;
  chrome.storage.local.set({ enabled });
});