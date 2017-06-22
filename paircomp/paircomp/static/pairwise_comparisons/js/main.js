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
//
//$(function() {
//
//    var bar = $('.bar');
//    var percent = $('.percent');
//    var status = $('#status');
//
//    $('form').ajaxForm({
//        beforeSend: function() {
//            status.empty();
//            var percentVal = '0%';
//            bar.width(percentVal);
//            percent.html(percentVal);
//        },
//        uploadProgress: function(event, position, total, percentComplete) {
//            var percentVal = percentComplete + '%';
//            bar.width(percentVal);
//            percent.html(percentVal);
//        },
//        complete: function(xhr) {
//            status.html(xhr.responseText);
//        }
//    });
//});