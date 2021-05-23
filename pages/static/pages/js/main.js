// Keep current year at footer
const date = new Date();
document.querySelector('.year').innerHTML = date.getFullYear();

// Alerts fade out after 3 seconds
setTimeout(function () {
    $('#message').fadeOut('slow');
}, 3000);
