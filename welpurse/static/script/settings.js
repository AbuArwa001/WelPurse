$(document).ready(function() {
    $('#profile-pic-upload').change(function(event) {
        const reader = new FileReader();
        reader.onload = function() {
            $('#profile-pic').attr('src', reader.result);
        };
        reader.readAsDataURL(event.target.files[0]);
    });
});