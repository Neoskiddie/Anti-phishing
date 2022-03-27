const textarea = document.getElementById("textarea");
const save = document.getElementById("save");
const checkbox = document.getElementById("checkbox");

save.addEventListener("click", () => {
  const whitelist = textarea.value.split("\n").map(s => s.trim()).filter(Boolean);
  chrome.storage.local.set({ whitelist });
});

checkbox.addEventListener("change", (event) => {
  const enabled = event.target.checked;
  chrome.storage.local.set({ enabled });
});

window.addEventListener("DOMContentLoaded", () => {
  chrome.storage.local.get(["whitelist", "enabled"], function (local) {
    const { whitelist, enabled } = local;
    if (Array.isArray(whitelist)) {
      textarea.value = whitelist.join("\n");
      checkbox.checked = enabled;
    }
  });
});
