window.addEventListener('scroll', function() {
    var header = document.getElementById('hero-name');
    var scrollPosition = window.scrollY;
    var maxScroll = document.body.clientHeight - window.innerHeight -700;
    var percentageScrolled = scrollPosition / maxScroll;

    // Define the colors you want to transition between
    var colorStart = [255, 255, 255]; // Start color (red in this example)
    var colorEnd = [233, 121, 17]; // End color (blue in this example)

    // Calculate the intermediate color
    var interpolatedColor = colorTransition(colorStart, colorEnd, percentageScrolled);

    // Set the color of the header
    header.style.color = 'rgb(' + interpolatedColor.join(',') + ')';
});

// Function to calculate intermediate color based on percentage
function colorTransition(startColor, endColor, percentage) {
    var result = [];
    for (var i = 0; i < 3; i++) {
        result.push(Math.round(startColor[i] + (endColor[i] - startColor[i]) * percentage));
    }
    return result;
}

document.addEventListener("DOMContentLoaded", function() {
    var trigger = document.querySelector('.trigger');
    var imageContainer = document.querySelector('.image-container');
    var scrollOffset = 2000; // Adjust this value based on how far down you want the image to appear

    window.addEventListener('scroll', function() {
        if (window.scrollY > (trigger.offsetTop + scrollOffset)) {
            imageContainer.style.display = 'flex';
        } else {
            imageContainer.style.display = 'none';
        }
    });
});
