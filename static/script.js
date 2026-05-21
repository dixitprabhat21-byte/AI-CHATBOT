// Initialization and User Session Management Logic
document.addEventListener("DOMContentLoaded", function() {
    let storedName = localStorage.getItem("chatbot_username");
    if (storedName) {
        document.getElementById("name-modal").style.display = "none";
        document.getElementById("user-greeting").innerHTML = `Hello, ${storedName} 👋`;
    }
});

function saveUserSession() {
    let nameInput = document.getElementById("username-input").value.trim();
    if (!nameInput) {
        nameInput = "Guest Explorer";
    }
    localStorage.setItem("chatbot_username", nameInput);
    document.getElementById("name-modal").style.display = "none";
    document.getElementById("user-greeting").innerHTML = `Hello, ${nameInput} 👋`;
    
    // Add an initial welcome message from the AI natively
    appendMessage("AI Assistant", `Hello ${nameInput}! I am online and fully calibrated. Ask me anything or feed me code! 🚀✨`, false);
}

function handleKeyPress(event) {
    if (event.key === "Enter") {
        sendMessage();
    }
}

function sendSuggestedPrompt(promptText) {
    document.getElementById("user-input").value = promptText;
    sendMessage();
}

async function sendMessage() {
    let inputField = document.getElementById("user-input");
    let messageText = inputField.value.trim();
    if (!messageText) return;

    // Render User Message bubble on Screen immediately
    appendMessage("You", messageText, true);
    inputField.value = "";

    // Render smooth flashing loading placeholder bubble for UX response alignment
    let chatBox = document.getElementById("chat-box");
    let loadingId = "load_" + Date.now();
    chatBox.innerHTML += `
        <div class="chat-message-row ai-row" id="${loadingId}">
            <div class="message-avatar"><i class="fa-solid fa-robot"></i></div>
            <div class="message-content">
                <span class="sender-title">AI Assistant</span>
                <p class="loading-dots">Thinking<span>.</span><span>.</span><span>.</span></p>
            </div>
        </div>
    `;
    chatBox.scrollTop = chatBox.scrollHeight;

    try {
        let response = await fetch("/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: messageText })
        });

        let data = await response.json();
        
        // Remove loading state element
        let loadingEl = document.getElementById(loadingId);
        if (loadingEl) loadingEl.remove();

        // Append real AI response strings safely
        appendMessage("AI Assistant", data.reply, false);

    } catch (error) {
        let loadingEl = document.getElementById(loadingId);
        if (loadingEl) loadingEl.remove();
        appendMessage("AI Assistant", "⚙️ Connection interrupted. Let's send that payload down the wire again! ✨", false);
    }
}

function appendMessage(sender, text, isUser) {
    let chatBox = document.getElementById("chat-box");
    let timeString = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    
    let messageRowClass = isUser ? "user-row" : "ai-row";
    let iconHTML = isUser ? `<i class="fa-solid fa-user"></i>` : `<i class="fa-solid fa-robot"></i>`;
    
    chatBox.innerHTML += `
        <div class="chat-message-row ${messageRowClass}">
            <div class="message-avatar">${iconHTML}</div>
            <div class="message-content">
                <span class="sender-title">${sender}</span>
                <p>${text}</p>
                <span class="message-time">${timeString}</span>
            </div>
        </div>
    `;
    chatBox.scrollTop = chatBox.scrollHeight;
}
