document.getElementById('options').onclick = openOps;
document.getElementById('about').onclick = openAbout;
const checkbox = document.getElementById("checkbox");
function openOps() {
    chrome.runtime.openOptionsPage()
};

function openAbout() {
    chrome.tabs.create({ url: 'https://gbronka.com/honours' });
};
