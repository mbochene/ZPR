var generateLocalBoard = function (id) {
    if (id % 3 == 0) {
        $('#globalboard').append('<tr id="row' + parseInt(id / 3) + '"></tr>');
    }
    $('#row' + parseInt(id / 3)).append('<td id="' + id + '"></td>');
    $('#' + id).append('<table id="table' + id + '" class="localboard"></table>');
    for (let row = 0; row < 3; ++row) {
        $('#table' + id).append('<tr id="row' + id + row + '"></tr>')
        for (let col = 0; col < 3; ++col) {
            var localId = row * 3 + col;
            $('#row' + id + row).append('<td id="' + id + localId + '" class="clue field ' + id + '"></td>')
        }
    }
}
var recoverInitialBoard = function () {
    var globalBoard = document.getElementById('globalboard');
    while (globalBoard.firstChild) {
        globalBoard.removeChild(globalBoard.firstChild);
    }
    for (let i = 0; i < 9; ++i) {
        generateLocalBoard(i);
    }
}
var clearChat = function () {
    var chat = document.querySelector('.chatlogs');
    while (chat.firstChild) {
        chat.removeChild(chat.firstChild);
    }
}
var addClickHandler = function (socket) {
    $(".field").click(function () {
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
var appendMessage = function (msg, sender) {
    var imgPath = '/static/img/user-512.png';
    if (sender == 'self') {
        imgPath = '/static/img/galeria-me.png';
    }
    $('.chatlogs:first').append('<div class="chat ' + sender + '"></div>');
    $('.chat:last').append('<div class="user-photo"></div>');
    $('.user-photo:last').append('<img src="' + imgPath + '">');
    $('.chat:last').append('<p class="chat-message">' + msg + '</p>');
    var chatlogs = document.getElementsByClassName('chatlogs')[0];
    chatlogs.scrollTop = chatlogs.scrollHeight - chatlogs.clientHeight;
}
var handleJoinClick = function (socket) {
    var data = {
        roomId: $('#room-id-input').val(),
        status: ''
    }
    $('#room-id-input').val('');
    socket.emit('joinRoom', data)
}
var onJoin = function (data) {
    console.log(data);
    if (data.status == 'JOINED_ROOM') {
        $('#out-of-room').hide();
        $('#in-room').show();
        $('#welcome-info').show();
        $('#game').hide();
    }
}
var onLeave = function () {
    $('#in-room').hide();
    $('#out-of-room').show();
    clearChat();
}
var handleCreateClick = function (socket) {
    socket.emit('createRoom');
}
handleLeaveClick = function (socket) {
    socket.emit('leaveRoom')
}
var onGameStop = function (socket) {
    console.log("stop");
    $('#game').hide();
    $('#welcome-info').show();
    recoverInitialBoard();
    resetScore();
    addClickHandler(socket);
}
var onGameStart = function () {
    $('#game').show();
    $('#welcome-info').hide();
    console.log("start");

}
var onDisconnect = function (socket) {
    $('#game').hide();
    $('#welcome-info').show();
    socket.disconnect();
}
var resetScore = function () {
    $('.score-x:first').html(0);
    $('.score-o:first').html(0);
}
$(document).ready(function () {
    namespace = '/';
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port + namespace);
    recoverInitialBoard();
    addClickHandler(socket);
    $('#out-of-room').show();
    $('#in-room').hide();
    socket.on('startGame', function () { onGameStart(); });
    socket.on('stopGame', function () { onGameStop(socket); });
    socket.on('disconnect', function () { onDisconnect(socket); });
    socket.on('receivedMessage', function (data) { appendMessage(data.msg, data.who); });
    socket.on('actualizeView', function (data) {
        boardId = parseInt(data.id / 10);
        $('#' + data.id).append('<img src="/static/img/' + data.inHtml + '.png">');
        for (let i = 0; i < 9; ++i) {
            $('.' + i).removeClass('clue');
        }
        for (let i = 0; i < data.toLighten.length; ++i) {
            $('.' + data.toLighten[i]).addClass('clue');
        }
        if (data.localGameEnded) {
            $('.' + boardId).hide();
            $('#' + boardId).addClass('finishedlocal');
            var localBoard = document.getElementById(boardId);
            while (localBoard.firstChild) {
                localBoard.removeChild(localBoard.firstChild);
            }
            $('#' + boardId).append('<img src="/static/img/' + data.localBoardWinner + '.png">');
            if (data.globalGameEnded) {
                var score = parseInt($('.score-' + data.localBoardWinner.toLowerCase() + ':first').html()) + 1;
                $('.score-' + data.localBoardWinner.toLowerCase() + ':first').html(score);
                recoverInitialBoard();
                addClickHandler(socket);
            }
        }
    });
    socket.on('joinRoom', function (data) { onJoin(data); });
    socket.on('leaveRoom', function () { onLeave(); })
    $('#create-room-button').click(function () { handleCreateClick(socket); });
    $('#join-room-button').click(function () { handleJoinClick(socket); });
    $('#leave-room-button').click(function () { handleLeaveClick(socket); });
    $('#textfield').keypress(function (event) {
        if (event.which == 13) {
            event.preventDefault();
            $('#sender').click();
        }
    });
    $('#sender').click(function () {
        var message = $('#textfield').val();
        if (message.trim() == "") {
            return;
        }
        $("#textfield").val('');
        var data = {
            msg: message,
            who: ''
        }
        socket.emit('msgSent', data);
    });
});