'use strict';
// add styles.css file
import './styles.css';

function get_urls(content) {
    // Get all anchor elements (links) from the webpage
    var links = document.getElementsByTagName('a');
    // Check if in a class there is also ping attribute
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

function closest(element) {
    var parent = element.parentNode;
    if (parent.tagName !== "nav" || parent.tagName !== "header" || parent.tagName !== "footer" ){
        return parent;
    } // No div parent found
}

function scrape() {
    console.log("Scraping...")
    const content = document.body.innerHTML;
    var results = get_urls(content)
    var data = {"urls": results};

    fetch('http://localhost:9092/your-endpoint', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(results)
      })
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(data => {
        console.log('Success:', data);
      })
      .catch(error => {
        console.error('Error:', error);
      });

    var json_dict = {};
    results.forEach(function(string) {
        json_dict[string] = Math.random() < 0.5; // Adjust the threshold as needed
    });

    predict(json_dict);
}

function predict(json_dict) {
    console.log("Predicting...")
    var count = 0;

    for (var key in json_dict) {
        if (json_dict.hasOwnProperty(key)) {
            // Find the corresponding anchor element in the HTML document based on the key
            var anchorElement = document.querySelector('a[href="' + key + '"]');
            // Apply blur to the anchor element if it exists
            if (anchorElement) {
                anchorElement.removeAttribute('href');
                anchorElement.style.color = 'grey'; // Change color to indicate it's disabled (optional)
                parent = closest(anchorElement)
                if(parent){
                    parent.classList.add("tooltip");
                    parent.dataset.tooltip = '!'; // Add tooltip text
                    console.log("Element removed: ", key);
                }
            }
        }
    }
    console.log("Count: " + count);
}

chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
    // Check if the message is from the background script
    if (message.from === 'process') {
        console.log('Message received from background script:', message.data);
        scrape();
    }
});

chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
    // Your existing listener logic
    if (message.from === 'process') {
        scrape(); // Call scrape function
    }
});




