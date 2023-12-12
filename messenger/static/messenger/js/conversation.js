const conversation_id = JSON.parse(document.getElementById('conversation_id').textContent);
const current_user_id = JSON.parse(document.getElementById('current_user_id').textContent);

const convSocket = new WebSocket(
    'wss://'
    + window.location.host
    + '/ws/conversation/'
    + conversation_id
    + '/'
);

scrollToBottom();

convSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    removeEmpty();
    document.querySelector('#messages-list').appendChild(messageDOM(data));
    scrollToBottom();
};

convSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly ');
};

document.querySelector('#message-input').focus();
document.querySelector('#message-input').onkeyup = function(e) {
    if (e.key === 'Enter') {
        document.querySelector('#message-submit').click();
    }
};

document.querySelector('#message-submit').onclick = function(e) {
    e.preventDefault();
    const messageInputDom = document.querySelector('#message-input');
    const message = messageInputDom.value;
    if (message == "") return;

    convSocket.send(JSON.stringify({
        'message': message,
        'sender_id': current_user_id
    }));
    messageInputDom.value = '';
};

function messageDOM(data) {
    let senderClass = ""
    if (data.sender_id == current_user_id) {
        senderClass = "message-from-current-user";
    }
    const str = `<div class='message-container ${senderClass}'><p class='message-content'>${data.message}</p></div>`;

    const placeholder = document.createElement("div");
    placeholder.insertAdjacentHTML("afterbegin", str);
    const node = placeholder.firstElementChild;

    return node;
}

function scrollToBottom() {
    const container = document.getElementById("messages-list");
    let isScrolledToBottom = container.scrollHeight - container.clientHeight <= container.scrollTop + 1;

    if (!isScrolledToBottom) {
        container.scrollTop = container.scrollHeight - container.clientHeight;
    }
}

function removeEmpty() {
    const empty = document.getElementById("message-empty-chat");
    if (empty) { empty.remove();}
}