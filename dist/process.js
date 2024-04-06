import { scrape } from "./scrape";

// Define an asynchronous functon to handle the page scraping
async function handlePageScraping() {
  // Retrieve the isActive value from local storage
  const isActive = await new Promise((resolve) => {
    chrome.storage.local.get(["isActive"], function (result) {
      // Default to false if isActive is not present in local storage
      const isActive = result.isActive || false;
      console.log("isActive:", isActive);
      resolve(isActive);
    });
  });

  // Check if isActive is true
  if (isActive) {
    console.log("Processing page");
    // Call the scrape function when isActive is true
    scrape();
  } else {
    console.log("Not processing...");
  }
}

// Add a listener to the tabs.onUpdated event
chrome.tabs.onUpdated.addListener(function (tabId, changeInfo, tab) {
  // Check if the tab update is complete
  if (changeInfo.status === "complete") {
    // Execute the handlePageScraping function
    handlePageScraping();
  }
});
