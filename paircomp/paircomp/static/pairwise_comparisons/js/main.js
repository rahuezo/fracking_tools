$(document).on('mouseenter','#csv-help', function (event) {
    $("#example-csv").fadeIn(300);
}).on('mouseleave','#csv-help',  function(){
    $("#example-csv").fadeOut(300);
});


function showNumberOfSelectedFiles(element) {

    var files = element.files;

    $('#upload-comp-files-info').html(
        '<span id="comp-selected-files">' + files.length + ' Files Selected</span>'
    );
}

(function() {

    $('form > input').keyup(function() {

        var empty = false;
        $('form > input').each(function() {
            if ($(this).val() == '') {
                empty = true;
            }
        });

        if (empty) {
            $('#multi-file-btn').attr('disabled', 'disabled'); // updated according to http://stackoverflow.com/questions/7637790/how-to-remove-disabled-attribute-with-jquery-ie
        } else {
            $('#multi-file-btn').removeAttr('disabled'); // updated according to http://stackoverflow.com/questions/7637790/how-to-remove-disabled-attribute-with-jquery-ie
        }
    });
})()