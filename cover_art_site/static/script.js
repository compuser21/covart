$(document).ready(function () {
    $('#upload-mp3').submit(function (e) { 
        e.preventDefault();

        var formData = new FormData(this);

        $.ajax({
            type: "POST",
            url: "/upload-mp3",
            data: formData,
            processData: false,
            contentType: false,
            success: function (response) {
                $('#mp3-file-status').text('MP3 Uploaded');
            },
            error: function() {
                $('#mp3-file-status').text('Error uploading MP3 file.');
            }
        });
    });
    $('#upload-image').submit(function (e) { 
        e.preventDefault();

        var formData = new FormData(this);

        $.ajax({
            type: "POST",
            url: "/upload-image",
            data: formData,
            processData: false,
            contentType: false,
            success: function (response) {
                $('#image-file-status').text('Image Uploaded');
            },
            error: function() {
                $('#image-file-status').text('Error uploading image file.');
            }
        });
    });
});