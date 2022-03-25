document.getElementById('a_options').onclick = openOps;
function openOps() {
    chrome.runtime.openOptionsPage()
    //closeAndReloadPopup();
};