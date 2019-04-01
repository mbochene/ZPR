var generateLocalBoard = function (id) {
    if (id % 3 == 0) {
        $('#globalBoard').append('<tr id="row' + parseInt(id / 3) + '"></tr>');
    }
    $('#row' + parseInt(id / 3)).append('<td id="' + id + '"></td>');
    $('#' + id).append('<table id="table' + id + '" class="localBoard"></table>');
    for (let row = 0; row < 3; ++row) {
        $('#table' + id).append('<tr id="row' + id + row + '"></tr>')
        for (let col = 0; col < 3; ++col) {
            var localId = row * 3 + col;
            $('#row' + id + row).append('<td id="' + id + localId + '" class="clue field bordered ' + id + '"></td>')
        }
    }
}

var recoverInitialBoard = function () {
    var globalBoard = document.getElementById('globalBoard');
            while (globalBoard.firstChild) {
                globalBoard.removeChild(globalBoard.firstChild);
            }
            for (let i = 0; i < 9; ++i) {
                generateLocalBoard(i);
            }
}

var addClickHandler = function(socket) {
    $(".field").click(function () {
        console.log("addClickHandler");
        inHtml = $(this).html();
        id = $(this).attr('id');
        var data = {
            id: id,
            inHtml: inHtml,
            toLighten: [],
            localGameEnded: false,
            localBoardWinner: '',
            globalGameEnded: false
        };
        socket.emit('clickedField', data);
    });
}

$(document).ready(function () {
    namespace = '/test';
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port + namespace);

    for (let i = 0; i < 9; ++i) {
        generateLocalBoard(i);
    }

    $("#globalBoard").hide();
    $("#welcomeInfo").show();

    socket.on('startGame', function () {
        console.log('gamestart');
        $("#welcomeInfo").hide();
        $("#globalBoard").show();
    });

    socket.on('stopGame', function () {
        console.log('gamestop');
        $("#globalBoard").hide();
        recoverInitialBoard();
        addClickHandler(socket);
        $("#welcomeInfo").show();
    });

    socket.on('disconnect', function () {
        console.log('disconnect');
        socket.disconnect();
    });

    for (let i = 0; i < 9; ++i) {
        $('.' + i).addClass('clue');
    }

    socket.on('respondToReceivedMessage', function (msg) {
        $("#chat").append('<li>' + msg + '</li>')
    });
    socket.on('actualizeView', function (data) {
        boardId = parseInt(data.id / 10);
        document.getElementById(data.id).innerHTML = data.inHtml;
        if (data.inHtml == 'X') {
            $('#' + data.id).addClass('takenByX');
        } else {
            $('#' + data.id).addClass('takenByY');
        }
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
            if (data.localBoardWinner == 'X') {
                $('#' + boardId).addClass('takenByX');
            } else {
                $('#' + boardId).addClass('takenByY');
            }
            console.log(document.getElementById(boardId).innerHTML);
            if(data.globalGameEnded)
            {
                recoverInitialBoard();
                addClickHandler(socket);
            }
        }
    });

    addClickHandler(socket);

    $("#sender").click(function () {
        console.log($("#textfield").val())
        socket.emit('msgSent', $("#textfield").val());
        $("#textfield").val('');
    });
});