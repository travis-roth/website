window.addEventListener('scroll', function() {
    var header = document.getElementById('hero-name');
    var scrollPosition = window.scrollY;
    var maxScroll = document.body.clientHeight - window.innerHeight -2200;
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
    const weatherSection = document.querySelector('.weather');
    const weatherStatus = weatherSection.dataset.status;

    const rainAnimation = document.querySelector('.rain');
    const sunAnimation = document.querySelector('.sun');
    const cloudsAnimation = document.querySelector('.clouds');

    rainAnimation.style.display = 'none';
    sunAnimation.style.display = 'none';
    cloudsAnimation.style.display = 'none';

    if (weatherStatus.toLowerCase().includes('rain')) {
        rainAnimation.style.display = 'block';
    } else if (weatherStatus.toLowerCase().includes('clear')) {
        sunAnimation.style.display = 'block';
    } else if (weatherStatus.toLowerCase().includes('clouds')) {
        cloudsAnimation.style.display = 'block';
    }

});

$(document).ready(function() {
    $('.burger-menu').click(function() {
      $('.nav-links').toggleClass('active');
    });
  });