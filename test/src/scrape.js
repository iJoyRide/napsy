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

// function applyModifications(imgElement) {
//     console.log("Apply modifications...")
//     // const images = document.querySelectorAll('img');
//     // console.log(images);

//     // let delay = 0;
//     // const delayIncrement = 50; 

//     // images.forEach(img => {
//     //     setTimeout(() => {
//     //         img.style.filter = 'blur(10px)';
//     //     }, delay);
//     //     delay += delayIncrement;
//     // });

//     // images.forEach(img => {
//     //     img.addEventListener('click', function(event) {
//     //         event.preventDefault();
//     //         event.stopPropagation();
            
//     //         // Blur the image
//     //         img.style.filter = 'blur(5px)'; // Apply blur effect
//     //         // img.style.opacity = '0.5'; // Change opacity to indicate it's disabled  (optional)
        
//     //     }, true);
//     // });
//     // images.forEach(img => {
//     //     // img.style.filter = 'blur(10px)';
//     //     event.stopPropagation();
//     // });
//     // event.preventDefault();
//     // event.stopPropagation();
//     // imgElement.addEventListener('click', function(event) {
//     //     event.stopPropagation();
//     //     event.preventDefault();
//     // });
//     // imgElement.style.filter = 'blur(10px)';
// }

// function observeChanges() {
//     // Create a MutationObserver to observe changes in the DOM
//     const observer = new MutationObserver(mutations => {
//         mutations.forEach(mutation => {
//             if (mutation.type === 'childList') {
//                 // Call function to apply modifications whenever new nodes are added
//                 applyModifications();
//             }
//         });
//     });

//     // Start observing the body for added nodes
//     observer.observe(document.body, { childList: true, subtree: true });
// }

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
    var count = 0;

    for (var key in json_dict) {
        if (json_dict.hasOwnProperty(key)) {
            // Find the corresponding anchor element in the HTML document based on the key
            var anchorElement = document.querySelector('a[href="' + key + '"]');
            // Apply blur to the anchor element if it exists
            if (anchorElement) {
                // if (anchorElement.querySelector('img')) {
                //     console.log(anchorElement.querySelector('img'))
                //     applyModifications(anchorElement.querySelector('img'));
                // }
                anchorElement.removeAttribute('href');
                // anchorElement.style.pointerEvents = 'none'; // Disable pointer events
                anchorElement.style.color = 'grey'; // Change color to indicate it's disabled (optional)
                // Add hover tooltip that link is unsafe and cannot be interacted
                // anchorElement.title = 'This link is unsafe and cannot be interacted';
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
        observeChanges(); // Start observing changes when message received
        scrape(); // Call scrape function
    }
});




