(function () {
    'use strict';

    var socket_url,
        web_socket,
        chat_div = document.getElementById('chat-content'),
        chat_input = document.getElementById('chat-input'),
        users = {},
        active_users = [];

    function addMessage(message) {
        chat_div.textContent += message + '\n';
    }

    if (window.location.protocol === 'https:') {
        socket_url = 'wss:';
    } else {
        socket_url = 'ws:';
    }
    socket_url += '//' + window.location.host;
    socket_url += socket_url_path;

    web_socket = new WebSocket(socket_url);
    web_socket.onmessage = function (msg) {
        var obj = JSON.parse(msg.data),
            data = obj['data'];
        if (obj['type'] === 'curstate') {
            var userlist = data['userlist'],
                history = data['history'];
            for (var i in userlist) {
                var user = userlist[i];
                connected_users[user['connection_id']] = {
                    'nickname': user['nickname'],
                    'is_asker': user['is_asker']
                };
            }
            for (var i in history) {
                var userName = connected_users[history[i][0]]['nickname'],
                    message = history[i][1];
                addMessage(userName + ': ' + message);
            }
            active_users.concat(data['onlinelist']);
        } else if (obj['type'] === 'message') {
            var userName = connected_users[data['connection_id']]['nickname'],
                message = data['message'];
            addMessage(userName + ': ' + message);
        } else if (obj['type'] === 'connect') {
            connected_users[data['connection_id']] = {
                'nickname': data['nickname'],
                'is_asker': data['is_asker']
            };
            active_users.push(data['connection_id']);
            addMessage(data['nickname'] + ' connected.');   
        } else if (obj['type'] === 'disconnect') {
            var index = active_users.indexOf(data['connection_id']);
            active_users.splice(index, 1);
            addMessage(connected_users[data['connection_id']]['nickname'] + ' disconnected.');
        }
    };

    document.getElementById('chat-input-form').addEventListener('submit', function(e) {
        e.preventDefault();
        var message = chat_input.value;
        chat_input.value = '';
        web_socket.send(JSON.stringify({
            'type': 'message',
            'data': message
        }));
        chat_input.focus();
    });

})();
