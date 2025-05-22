// static/script.js

// Helper to add a message bubble to the chat
function addMessage(text, sender) {
    const chatWindow = document.getElementById('chat-window');
    const msgDiv = document.createElement('div');
    msgDiv.classList.add('message', sender);
    const bubble = document.createElement('div');
    bubble.classList.add('bubble');
    bubble.innerText = text;
    msgDiv.appendChild(bubble);
    chatWindow.appendChild(msgDiv);
    chatWindow.scrollTop = chatWindow.scrollHeight;
}

// Handle sending text queries
document.getElementById('send-text').onclick = () => {
    const queryField = document.getElementById('text-query');
    const query = queryField.value.trim();
    if (!query) return;
    addMessage(query, 'user');
    queryField.value = '';
    fetch('/ask_text', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: query })
    })
    .then(res => res.json())
    .then(data => addMessage(data.response, 'bot'));
};

// Handle document upload
document.getElementById('send-file').onclick = () => {
    const fileInput = document.getElementById('file-input');
    if (fileInput.files.length === 0) return;
    const file = fileInput.files[0];
    addMessage(`Uploading document: ${file.name}`, 'user');
    const formData = new FormData();
    formData.append('file', file);
    fetch('/upload_file', { method: 'POST', body: formData })
    .then(res => res.json())
    .then(data => addMessage(data.response, 'bot'));
};

// Handle image upload
document.getElementById('send-image').onclick = () => {
    const imgInput = document.getElementById('image-input');
    if (imgInput.files.length === 0) return;
    const file = imgInput.files[0];
    addMessage(`Sending image: ${file.name}`, 'user');
    const formData = new FormData();
    formData.append('image', file);
    fetch('/upload_image', { method: 'POST', body: formData })
    .then(res => res.json())
    .then(data => addMessage(data.response, 'bot'));
};

// Handle YouTube URL
document.getElementById('send-youtube').onclick = () => {
    const urlField = document.getElementById('youtube-url');
    const url = urlField.value.trim();
    if (!url) return;
    addMessage(`YouTube URL: ${url}`, 'user');
    urlField.value = '';
    fetch('/youtube', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url: url })
    })
    .then(res => res.json())
    .then(data => addMessage(data.response, 'bot'));
};
