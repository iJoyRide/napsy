// Define an asynchronous functon to handle the page scraping
async function handlePageScraping() {
  // Retrieve the isActive value from local storage
  const isActive = await new Promise((resolve) => {
    chrome.storage.local.get(['isActive'], function (result) {
      // Default to false if isActive is not present in local storage
      const isActive = result.isActive || false;
      console.log('isActive:', isActive);
      resolve(isActive);
    });
  });

  // Check if isActive is true
  if (isActive) {
    console.log('Processing page');
    // Call the scrape function when isActive is true
    chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
      // Ensure that there's at least one active tab
      if (tabs.length > 0) {
          // Get the ID of the active tab
          const tabId = tabs[0].id;
          // Send a message to the content script of the active tab
          console.log(tabId)
          chrome.tabs.sendMessage(tabId, {from: 'process', data: 'Start processing...' });
      }
    });
  } else {
    console.log('Not processing...');
  }
}

// Add a listener to the tabs.onUpdated event
chrome.tabs.onUpdated.addListener(function (tabId, changeInfo, tab) {
  // Check if the tab update is complete
  if (changeInfo.status === 'complete') {
    // Execute the handlePageScraping function
    handlePageScraping();
  }
});
