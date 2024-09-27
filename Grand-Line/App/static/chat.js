document.addEventListener('DOMContentLoaded', function() {
    
    const chat = JSON.parse(document.getElementById('chat-data').textContent);
    displayMessageHistory(chat);

    
    function updateChat() {
        fetch('/get-chat-data')
            .then(response => {
                if (!response.ok) {
                    throw new Error('ca marche PASSSSSSSSSSSSSSSSSSSS');
                }
                return response.json();
            })
            .then(chatData => {
                const chatDataScript = document.getElementById('chat-data');
                
                chatDataScript.textContent = JSON.stringify(chatData);
                clearChatOutput();               
                displayMessageHistory(chatData);
                const output = document.getElementById('chat-window');
                output.scrollTo({
                top: output.scrollTop = output.scrollHeight,
                behavior: "smooth",
                });
                window.scrollTo({
                    top:window.scrollTop=window.scrollHeight,
                    behavior:"smooth"
                })
                
            })
            .catch(error => {
                console.error('y as pas de message:', error);
            });
    }

   
    setInterval(updateChat, 3000);
    
    
    
    
    document.getElementById('send').addEventListener('click', sendMessage);
    document.getElementById('message').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
    scrollToBottom();
});

function displayMessageHistory(data) {
    data.forEach(element => {
        displayMessage(element.sender, element.message);
        
    });
    
}

function sendMessage() {
    const messageInput = document.getElementById('message');
    const message = messageInput.value;
    if (message.trim() !== '') {
        
        fetch('/send-message', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: message }),
        })
        .then(response => {
            if (response.ok) {
                
                
                displayMessage('You', message)
                
                messageInput.value = '';
            } else {
                
                console.error('c pas bon.');
            }
        })
        .catch(error => {
            
            console.error(' ?', error);
        });
    }
}

function displayMessage(sender, message) {
    const output = document.getElementById('output');
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message');
    messageDiv.innerHTML = `<strong>${sender}:</strong> ${message}`;
    output.appendChild(messageDiv);
    output.scrollTop = output.scrollHeight;
}

function scrollToBottom() {
    const output = document.getElementById('chat-window');
    output.scrollTo({
    top: output.scrollTop = output.scrollHeight,
    behavior: "smooth",
    });
    
      
}

function clearChatOutput() {
    const output = document.getElementById('output');
    while (output.firstChild) {
        output.removeChild(output.firstChild);
    }
}

