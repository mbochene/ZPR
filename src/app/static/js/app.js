var whoNow = 'X'
$(document).ready(function () {
    namespace = '/test';
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port + namespace);

    socket.on('connect', function () {
    });


    socket.on('respondToClickedField', function (data) {
        document.getElementById(data.id).innerHTML = data.inHtml;
        var classNameToRemoveLighten = '.' + data.previouslyPlayed;
        var classNameToLighten = '.' + data.playNowHere;
        $(classNameToRemoveLighten).removeClass('clue');
        $(classNameToLighten).addClass('clue');
    });

    socket.on('respondToReceivedMessage', function (msg) {
        $("#chat").append('<li>' + msg + '</li>')
    });

    $("td").click(function () {
        inHtml = $(this).html();
        id = $(this).attr('id');
        var data = {
            id: id,
            inHtml: inHtml,
            playNowHere: '',
            previouslyPlayed: ''
        };
        socket.emit('clickedField', data);
    });

    $("#sender").click(function () {
        console.log($("#textfield").val())
        socket.emit('msgSent', $("#textfield").val());
        $("#textfield").val('');
    });
});
