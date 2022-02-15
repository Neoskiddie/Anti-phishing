const queryString = window.location.search;
console.log(queryString);
const urlParams = new URLSearchParams(queryString);
const maliciousUrl = urlParams.get("originalurl");
console.log(maliciousUrl);
document.getElementById('maliciousUrl').innerText = maliciousUrl

document.getElementById("backButton").onclick = function () {
  history.back()
}

document.getElementById("visitButton").onclick = function () {
  // TODO add it to whitelist
  location.href = maliciousUrl;
}
