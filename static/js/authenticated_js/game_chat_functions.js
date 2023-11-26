function append_message (author, message, timestamp, owner) {
   
    let messages = document.querySelector('.messages');

    const message_container = document.createElement('div');
    message_container.className = owner ? 'd-flex flex-wrap justify-content-end my-3' : 'd-flex flex-wrap justify-content-start';

    if (!owner) {
        const owner_username = document.createElement('div');
        owner_username.className = 'author col-10 col-sm-8 d-flex flex-wrap justify-content-start px-1';
        owner_username.textContent = author;
        message_container.appendChild(owner_username);
    }

    const message_box = document.createElement('div');
    message_box.className = 'chat-box border rounded col-10 col-sm-8 d-flex flex-column';

    const content = document.createElement('div');
    content.className = 'px-2 d-flex flex-wrap justify-content-start';
    content.textContent = message;
    message_box.appendChild(content);


    const timestamp_div = document.createElement('div');
    timestamp_div.className = 'px-2 d-flex justify-content-end timestamp';
    timestamp_div.textContent = timestamp;
    message_box.appendChild(timestamp);

    message_container.appendChild(message_box);

    messages.appendChild(message_container);
}


// ------------------------------------------------------------------------------------POSSIBLY DON'T NEED, BUT WOULD NEED TO HANDLE PARAMS FOR APPEND ABOVE PROPERLY
function load_chat (user_chats, chat_users, id_to_load, user_id) {
    let chat_list = document.querySelector('.messages');

    // Removes any content before updating
    while (chat_list.firstChild) {
        chat_list.removeChild(chat_list.firstChild);
    };

    // Finds chat to load, and adds messages
    user_chats.forEach(chat => {
        if (chat.event_id === id_to_load) {
            chat.messages.forEach(message => {
                const author = chat_users[message.user_id];
                const message_content = message.message;
                const options = { day: '2-digit', month: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit', timeZone: 'Europe/London' };
                const timestamp = new Intl.DateTimeFormat('en-GB', options).format(message.timestamp);
                const owner = message.user_id===user_id ? true : false;

                append_message(author, message_content, timestamp, owner);
            });
        }
    });
}