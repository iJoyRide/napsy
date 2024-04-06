'use strict';
// add styles.css file
import './styles.css';

function get_urls(content) {
    // Get all anchor elements (links) from the webpage
    var links = document.getElementsByTagName('a');
    var base = window.location.origin;  // Base URL for converting relative to absolute URLs

    // Initialize a Set to store unique URLs
    var urls = new Set();

    // Iterate over each link, extract its href attribute, and add to the Set
    for (var i = 0; i < links.length; i++) {
        var url = links[i].href.trim();

        // Convert relative URLs to absolute and add to the Set if not empty
        if (url.startsWith('/')) {
            url = base + url;
        }

        if (url && url.startsWith('http')) {  // Filter to include only HTTP/HTTPS URLs
            urls.add(url);
        }
    }

    // Convert Set to Array for easier processing or transmission
    var uniqueUrls = Array.from(urls);
    return uniqueUrls;
}

function scrape() {
    console.log("Scraping...")
    const content = document.body.innerHTML;
    var results = get_urls(content);

    var json_dict = {};
    results.forEach(function(string) {
        json_dict[string] = Math.random() < 0.5; // Adjust the threshold as needed
    });

    predict(json_dict);
}

function predict(json_dict) {
    console.log("Predicting...")

    for (var key in json_dict) {
        if (json_dict.hasOwnProperty(key)) {
            // Find the corresponding anchor element in the HTML document based on the key
            var anchorElement = document.querySelector('a[href="' + key + '"]');
            // Apply blur to the anchor element if it exists
            if (anchorElement) {
                anchorElement.removeAttribute('href');
                // anchorElement.style.pointerEvents = 'none'; // Disable pointer events
                anchorElement.style.color = 'grey'; // Change color to indicate it's disabled (optional)
                // Add hover tooltip that link is unsafe and cannot be interacted
                // anchorElement.title = 'This link is unsafe and cannot be interacted';
                anchorElement.classList.add("tooltip");
                anchorElement.dataset.tooltip = 'This link is disabled'; // Add tooltip text
                console.log("Element removed: ", key);
            }
        }
    }
}

chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
    // Check if the message is from the background script
    if (message.from === 'process') {
        console.log('Message received from background script:', message.data);
        scrape();
    }
});




