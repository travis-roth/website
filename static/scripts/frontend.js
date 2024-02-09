// Function to track custom events, including screen information
function trackEvent(eventName, eventData) {
    var userId = getCookie('user_id'); // Get the user ID from the cookie
    if (!userId) {
        // Generate a new user ID if it doesn't exist
        userId = Math.random().toString(36).substring(2, 15) + Math.random().toString(36).substring(2, 15);
        setCookie('user_id', userId, 30); // Set the user ID as a cookie (valid for 30 days)
    }

    // Include screen dimensions and orientation in the event data
    eventData.screenWidth = window.screen.width;
    eventData.screenHeight = window.screen.height;
    eventData.screenOrientation = window.screen.orientation.type;

    // Send a request to log the custom event
    fetch('/log/event', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            eventType: eventName,
            eventData: {
                userId: userId,
                ...eventData
            },
            timestamp: new Date().toISOString()
        })
    })
    .then(response => {
        if (!response.ok) {
            console.error('Failed to log event:', response.statusText);
        }
    })
    .catch(error => {
        console.error('Error logging event:', error);
    });
}

// Event delegation to handle all events dynamically
document.addEventListener('click', function(event) {
    var target = event.target;

    // Example: Track button clicks
    if (target.tagName === 'BUTTON') {
        // Track the button click event
        trackEvent('button_click', {
            htmlId: target.id,
            buttonText: target.innerText
        });
    }

    // Example: Track input changes
    if (target.tagName === 'INPUT') {
        // Track the input change event
        trackEvent('input_change', {
            htmlId: target.id,
            inputValue: target.value
        });
    }

    // Add more event handling logic as needed for other types of events
});

// Example: Track page views when the page loads
window.addEventListener('load', function() {
    // Track the page view event
    trackEvent('page_view', {
        url: window.location.href,
        referrer: document.referrer
    });
});
