document.getElementById('options').onclick = openOps;
document.getElementById('about').onclick = openAbout;
var checkbox = document.getElementById("checkbox");
function openOps() {
    chrome.runtime.openOptionsPage()
};

function openAbout() {
    chrome.tabs.create({ url: 'https://gbronka.com/honours' });
};


// async method to get storage value
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

// load enabled from storage and set the checkbox to it's value
window.onload = async () => {
  let enabled = await readLocalStorage('enabled');
  checkbox.checked = enabled;
};

// set the checkbox value
checkbox.addEventListener("change", (event) => {
  const enabled = event.target.checked;
  chrome.storage.local.set({ enabled });
});