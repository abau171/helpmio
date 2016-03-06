(function () {
    'use strict';

    var socket_url,
        web_socket,
        note_overlay = document.getElementById('note-overlay'),
        note_panel = document.getElementById('note-panel'),
        open_notify_dialog = document.getElementById('open-notify-dialog');

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

    function toggleNotifyDialog() {
        if (note_panel.className === 'hidden') {
            note_panel.className = '';
            note_overlay.className = '';
        } else {
            note_panel.className = 'hidden';
            note_overlay.className = 'hidden';
        }
    }

    note_overlay.addEventListener('click', toggleNotifyDialog);

    open_notify_dialog.addEventListener('click', function (e) {
        e.preventDefault();
        toggleNotifyDialog();
    });

})();
