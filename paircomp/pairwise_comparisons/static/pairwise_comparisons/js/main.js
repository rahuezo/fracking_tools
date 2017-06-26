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
