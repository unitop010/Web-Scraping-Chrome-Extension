document.addEventListener('DOMContentLoaded', function() {
  document.getElementById('scrapeButton').addEventListener('click', scrapePage);
});

function scrapePage() {
  chrome.runtime.sendMessage({action: "scrape"}, function(response) {
    document.getElementById('results').innerText = JSON.stringify(response);
  });
}
