$(document).ready(function() {
    console.log("TIMEOUT -ONE")
    setTimeout(function() {
        console.log("TIMEOUT")
        $('.alert').alert('close');
    }, 5000); // Flash message will disappear after 5 seconds
});
