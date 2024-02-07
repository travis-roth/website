// Function to get a cookie by name
function getCookie(name) {
    var cookieName = name + "=";
    var decodedCookie = decodeURIComponent(document.cookie);
    var cookieArray = decodedCookie.split(';');
    for(var i = 0; i < cookieArray.length; i++) {
        var cookie = cookieArray[i].trim();
        if (cookie.indexOf(cookieName) === 0) {
            return cookie.substring(cookieName.length, cookie.length);
        }
    }
    return null;
}

// Function to set a cookie
function setCookie(name, value, days) {
    var expires = "";
    if (days) {
        var date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
        expires = "; expires=" + date.toUTCString();
    }
    document.cookie = name + "=" + (value || "") + expires + "; path=/";
}

// Function to track custom events
function trackEvent(eventName, eventData) {
    var userId = getCookie('user_id'); // Get the user ID from the cookie
    if (!userId) {
        // Generate a new user ID if it doesn't exist
        userId = Math.random().toString(36).substring(2, 15) + Math.random().toString(36).substring(2, 15);
        setCookie('user_id', userId, 30); // Set the user ID as a cookie (valid for 30 days)
    }

    // Send a request to log the custom event
    fetch('/log/event', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            eventType: eventName,
            eventData: {
                userId: userId, // Include the user ID in the event data
                // Add additional event data
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
            buttonId: target.id,
            buttonText: target.innerText
        });
    }

    // Example: Track input changes
    if (target.tagName === 'INPUT') {
        // Track the input change event
        trackEvent('input_change', {
            inputId: target.id,
            inputValue: target.value
        });
    }

    // Add more event handling logic as needed for other types of events
});

// Example: Track page views when the page loads
window.addEventListener('load', function() {
    // Track the page view event
    trackEvent('page_view', {
        url: window.location.href
    });
});