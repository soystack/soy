$(document).ready(function() {
    function render(data) {
        $('#ret').text(JSON.stringify(data));
    };
    $('#get').click(function() {
        $.get('/get', function(data,stat) {
            render(data)
        });
    });
    $('#create').click(function() {
        var host = $('#chost').val();
        $.post('/create/'+host, function(data, stat) {
            $('#chost').val('');
            render(data);
        });
    });
    $('#delete').click(function() {
        var host = $('#dhost').val();
        $.get('/delete/'+host, function(data, stat) {
            $('#dhost').val('')
            render(data)
        });
    });
});
