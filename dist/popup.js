// Use strict mode to enforce better coding practices
"use strict";

// Define an anonymous function that runs when the DOM content is fully loaded and parsed
document.addEventListener("DOMContentLoaded", function() {
    // Retrieve the checkbox element with the id "isActiveCheckbox"
    const isActiveCheckbox = document.getElementById("isActiveCheckbox");

    // Log a message indicating that the DOM is fully loaded and parsed
    console.log("DOM fully loaded and parsed");

    // Retrieve the value of "isActive" from local storage
    chrome.storage.local.get(["isActive"], function(result) {
        // If the checkbox element exists, update its checked property based on the value of "isActive"
        if (isActiveCheckbox) {
            isActiveCheckbox.checked = result.isActive || false;
        }
    });

    // Add an event listener to the checkbox element to detect changes in its state
    if (isActiveCheckbox) {
        isActiveCheckbox.addEventListener("change", function() {
            // Log a message indicating the change in the checkbox state
            console.log("isActiveCheckbox changed to:", isActiveCheckbox.checked);

            // Update the value of "isActive" in local storage based on the new state of the checkbox
            chrome.storage.local.set({ isActive: isActiveCheckbox.checked });
        });
    }
});
