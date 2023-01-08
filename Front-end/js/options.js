const textarea = document.getElementById("textarea");
const save = document.getElementById("save");
const checkbox = document.getElementById("myonoffswitch");

/**
 * Sets the whiteliste when the save button was pressed 
 */
save.addEventListener("click", () => {
  const whitelist = textarea.value.split("\n").map(s => s.trim()).filter(Boolean);
  chrome.storage.local.set({ whitelist });
});

/**
 * Sets the "enabled" in storage when the checbox was changed
 */
checkbox.addEventListener("change", (event) => {
  const enabled = event.target.checked;
  chrome.storage.local.set({ enabled });
});

/**
 * Updated textarea and checkbox on page load 
 */
window.addEventListener("DOMContentLoaded", () => {
  chrome.storage.local.get(["whitelist", "enabled"], function (local) {
    const { whitelist, enabled } = local;
    if (Array.isArray(whitelist)) {
      textarea.value = whitelist.join("\n");
      checkbox.checked = enabled;
    }
  });
});

/**
 * Listens for changes in the storage 
 * and updates the checkbox and textarea if the 
 * corresponding storage changed
 */
chrome.storage.onChanged.addListener((changes) => {
  for (let [key, { newValue }] of Object.entries(changes)) {
    console.log("New value for key " + key + " is: " + newValue);
    if (key === "enabled") {
      checkbox.checked = newValue;
    }
    if (key === "whitelist") {
      textarea.value = newValue
    }
  }
});