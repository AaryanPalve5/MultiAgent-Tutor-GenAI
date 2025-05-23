// static/script.js

function addMessage(text, sender) {
    const win = document.getElementById("chat-window");
    const msg = document.createElement("div");
    msg.className = `message ${sender}`;
    const bubble = document.createElement("div");
    bubble.className = "bubble";
    bubble.innerText = text;
    msg.appendChild(bubble);
    win.appendChild(msg);
    win.scrollTop = win.scrollHeight;
  }
  
  // Text question
  document.getElementById("send-text").onclick = async () => {
    const q = document.getElementById("text-query").value.trim();
    if (!q) return;
    addMessage(q, "user");
    document.getElementById("text-query").value = "";
  
    const res = await fetch("/ask_text", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query: q })
    });
    const data = await res.json();
    addMessage(data.answer, "bot");
  };
  
  // Document upload
  document.getElementById("send-file").onclick = async () => {
    const inp = document.getElementById("file-input");
    if (!inp.files.length) return;
    const file = inp.files[0];
    addMessage(`Document: ${file.name}`, "user");
  
    const fd = new FormData();
    fd.append("file", file);
    const res = await fetch("/upload_file", { method: "POST", body: fd });
    const data = await res.json();
    addMessage(data.answer, "bot");
  };
  
  // Image upload
  document.getElementById("send-image").onclick = async () => {
    const inp = document.getElementById("image-input");
    if (!inp.files.length) return;
    const file = inp.files[0];
    addMessage(`Image: ${file.name}`, "user");
  
    const fd = new FormData();
    fd.append("image", file);
    const res = await fetch("/upload_image", { method: "POST", body: fd });
    const data = await res.json();
    addMessage(data.answer, "bot");
  };
  
  // YouTube summarization
  document.getElementById("send-youtube").onclick = async () => {
    const urlField = document.getElementById("youtube-url");
    const url = urlField.value.trim();
    if (!url) return;
    addMessage(`YouTube URL: ${url}`, "user");
    urlField.value = "";
  
    const res = await fetch("/youtube", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url })
    });
    const data = await res.json();
    addMessage(data.answer, "bot");
  };
  