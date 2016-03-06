(function () {
    'use strict';

    var socket_url,
        web_socket,
        chat_div = document.getElementById('chat-content'),
        chat_input = document.getElementById('chat-input'),
        connected_users_list = document.getElementById('connected-users'),
        info_overlay = document.getElementById('info-overlay'),
        info_panel = document.getElementById('info-panel'),
        users = {},
        active_users = [];

    window.onbeforeunload = function (e) {
        return "A chat is currently open.\nIf you leave this page you will no longer receive messages from this chat.";
    };

    function addMessage(type, username, message) {
        var p = document.createElement("p");
        p.className = type;
        var span = document.createElement("span");
        var boldText = username;
        if (type === 'asker' || type === 'responder') {
            boldText += ':';
        }
        span.appendChild(document.createTextNode(boldText));
        p.appendChild(span);
        p.appendChild(document.createTextNode(' ' + message));
        chat_div.appendChild(p);
        p.scrollIntoView();
    }

    function addUser(connection_id, username) {
        var li = document.createElement("li");
        li.id = 'connected-users-list-' + connection_id;
        li.appendChild(document.createTextNode(username));
        connected_users_list.appendChild(li);
    }

    function removeUser(connection_id) {
        document.getElementById('connected-users-list-' + connection_id).remove();
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
                users[user['connection_id']] = {
                    'nickname': user['nickname'],
                    'is_asker': user['is_asker']
                };
            }
            for (var i in history) {
                var user = users[history[i][0]],
                    message = history[i][1],
                    type = 'responder';
                if (user['is_asker']) {
                    type = 'asker';
                }
                addMessage(type, user['nickname'], message);
            }
            active_users = active_users.concat(data['onlinelist']);
            for (var i in active_users) {
                var connection_id = active_users[i];
                addUser(connection_id, users[connection_id]['nickname']);
            }
        } else if (obj['type'] === 'message') {
            var user = users[data['connection_id']],
                message = data['message'],
                type = 'responder';
            if (user['is_asker']) {
                type = 'asker';
            }
            addMessage(type, user['nickname'], message);
        } else if (obj['type'] === 'connect') {
            users[data['connection_id']] = {
                'nickname': data['nickname'],
                'is_asker': data['is_asker']
            };
            active_users.push(data['connection_id']);
            addUser(data['connection_id'], data['nickname']);
            addMessage('meta', data['nickname'], 'connected.');   
        } else if (obj['type'] === 'disconnect') {
            var index = active_users.indexOf(data['connection_id']);
            active_users.splice(index, 1);
            removeUser(data['connection_id']);
            addMessage('meta', users[data['connection_id']]['nickname'], 'disconnected.');
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

    function toggleInfoPanel() {
        if (info_panel.className === 'hidden') {
            info_overlay.className = '';
            info_panel.className = '';
        } else {
            info_overlay.className = 'hidden';
            info_panel.className = 'hidden';
        }
    }

    info_overlay.addEventListener('click', toggleInfoPanel);
    document.getElementById('info-button').addEventListener('click', function (e) {
        e.preventDefault();
        toggleInfoPanel();
    });

    document.querySelector('#resolve-button-wrapper a').addEventListener('click', function (e) {
        e.preventDefault();
        if (window.confirm("Are you sure you want to resolve the issue?")) {
            web_socket.send(JSON.stringify({
                'type': 'resolve',
                'data': null
            }));
            document.getElementById('resolve-button-wrapper').style.display = 'none';
            alert("The issue has been marked as resolved.");
        }
    });

})();
