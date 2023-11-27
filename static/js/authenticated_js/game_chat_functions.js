function submitForm() {
    var message_input = document.getElementById('new_message_input').value;
    var chat_id = document.getElementById('chat_id').value;
    
    
    if (message_input.trim() === "") {
        return false;
    }
  
    var formData = new FormData();
    formData.append('new_message_input', message_input);
    formData.append('chat_id', chat_id);

    // Submit form
    fetch('/my_game_chats', {
        method: 'POST',
        body: formData,
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Something went wrong submitting the form');
        }
        return response.json();
    })
    .then(data => {
        // Adds message to messages display
        append_message(message_input, data.timestamp, true);

        // Clears previous input
        document.getElementById("new_message_input").value = "";
    })
    .catch(error => {
        console.error('Error:', error);
        
        displayAlertMessage("Something went wrong submitting the message, please try again later!", true, false);
    });

    return false;
}


function append_message (message, timestamp, owner, author) {
    
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
    message_box.className = 'message-box border rounded col-10 col-sm-8 d-flex flex-column';
    
    const content = document.createElement('div');
    content.className = 'px-2 d-flex flex-wrap justify-content-start';
    content.textContent = message;
    message_box.appendChild(content);

    
    const timestamp_div = document.createElement('div');
    timestamp_div.className = 'px-2 d-flex justify-content-end timestamp';
    timestamp_div.textContent = timestamp;
    message_box.appendChild(timestamp_div);
    
    message_container.appendChild(message_box);
    
    messages.appendChild(message_container);

    // Scroll to the bottom after adding a new message
    messages.scrollTop = messages.scrollHeight;
}


// Puts focus onto the input box when page loads and allows user to submit with enter button
document.addEventListener("DOMContentLoaded", function() {
    var input_element = document.getElementById("new_message_input");
    var submit_button = document.getElementById("submit_message");

    if(input_element && submit_button) {
        // Submits with enter key if something has been entered
        input_element.addEventListener("keydown", function(e) {
            if (e.key === "Enter") {
                e.preventDefault();

                if (input_element.value.trim() !== "") {
                    submitForm();
                } 
            }
        });

        // Prevents submitting on click if nothing entered
        submit_button.addEventListener("click", function(e) {
            e.preventDefault();
            
            if (input_element.value.trim() !== "") {
                submitForm();
            }
        });

        input_element.focus(); 
    }
});


document.addEventListener("DOMContentLoaded", function() {
    const message_container = document.querySelector('.messages');

    // Check if container is overflowed
    if (message_container.scrollHeight > message_container.clientHeight) {
        // Scroll to bottom
        message_container.scrollTop = message_container.scrollHeight;
    }
});



// Socket IO functions below here

// Establish a SocketIO connection
const socket = io.connect('http://127.0.0.1:8080');


function connectToRoom(chat_id) {
    socket.emit('join_room', { load_chat: chat_id });
}


function disconnectFromRoom() {
    const curr_room = getLoadedChat(); 
    if (curr_room) {
        socket.emit('leave_room', { leave_room: curr_room });
    }
}


function getLoadedChat() {
    const chat_ele = document.getElementsByClassName('loaded_chat')[0];
    if(chat_ele){
        return chat_ele.id;
    } else {
        return null;
    }
}


// Called when user clicks a new chat to load, disconnects from previous room and loads new chat. New connection is made upon load
function disconnectAndNavigate(load_chat) {
    disconnectFromRoom();
    window.location.href = '/my_game_chats?load_chat=' + load_chat;
}


// Connects to room for loaded chat
document.addEventListener("DOMContentLoaded", function() {
    const chat_id = getLoadedChat();
    if (chat_id){
        connectToRoom(chat_id);
        socket.on('message', function(data) {
            // Gets data set on hidden div element for user_id
            const user_id = document.getElementById('user-id').dataset.userId
            
            if(user_id !== String(data.author_id)) {
                append_message(data.message, data.timestamp, false, data.author)
            }
        });
    }
});


// Disconnects user if they navigate to another page
window.addEventListener('beforeunload', function() {
    disconnectFromRoom();
});

