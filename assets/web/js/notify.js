(function () {
    'use strict';

    var socket_url,
        web_socket;

    if (window.location.protocol === 'https:') {
        socket_url = 'wss:';
    } else {
        socket_url = 'ws:';
    }
    socket_url += '//' + window.location.host;
    socket_url += notify_socket_url_path;

    web_socket = new WebSocket(socket_url);
    web_socket.onmessage = function (msg) {
        console.log(msg);
    };

})();
