var whoNow = 'X'
$(document).ready(function () {
    namespace = '/test';
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port + namespace);

    for (let i = 0; i < 9; ++i) {
        var classNameToLighten = '.' + i;
        $(classNameToLighten).addClass('clue');
    }

    socket.on('respondToReceivedMessage', function (msg) {
        $("#chat").append('<li>' + msg + '</li>')
    });
    socket.on('actualizeView', function (data) {
        boardId = parseInt(data.id / 10);
        document.getElementById(data.id).innerHTML = data.inHtml;
        for (let i = 0; i < 9; ++i) {
            var classNameToRemoveLighten = '.' + i;
            $(classNameToRemoveLighten).removeClass('clue');
        }
        for (let i = 0; i < data.toLighten.length; ++i) {
            var classNameToLighten = '.' + data.toLighten[i];
            $(classNameToLighten).addClass('clue');
        }
        if (data.localGameEnded) {
            $('.' + boardId).hide();
            $('#' + boardId).addClass('finishedLocal');
            document.getElementById(boardId).innerHTML = data.localBoardWinner;
        }
    });

    $(".field").click(function () {
        inHtml = $(this).html();
        id = $(this).attr('id');
        var data = {
            id: id,
            inHtml: inHtml,
            toLighten: [],
            localGameEnded: false,
            localBoardWinner: ''
        };
        socket.emit('clickedField', data);
    });

    $("#sender").click(function () {
        console.log($("#textfield").val())
        socket.emit('msgSent', $("#textfield").val());
        $("#textfield").val('');
    });
});
