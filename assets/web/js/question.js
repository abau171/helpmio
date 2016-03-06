(function () {
    'use strict';

    var socket_url,
        web_socket,
        chat_div = document.getElementById('chat-content'),
        chat_input = document.getElementById('chat-input');

    if (window.location.protocol === 'https:') {
        socket_url = 'wss:';
    } else {
        socket_url = 'ws:';
    }
    socket_url += '//' + window.location.host;
    socket_url += socket_url_path;

    web_socket = new WebSocket(socket_url);
    web_socket.onmessage = function (msg) {
        chat_div.textContent += msg.data + "\n";
    };

    document.getElementById('chat-input-form').addEventListener('submit', function(e) {
        e.preventDefault();
        var message = chat_input.value;
        chat_input.value = '';
        web_socket.send(message);
        chat_input.focus();
    });

})();
