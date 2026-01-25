document.getElementById("contactForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const email = document.getElementById("email").value;
  const message = document.getElementById("message").value;

  const res = await fetch("http://127.0.0.1:8000/contact", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, message })
  });
  const data = await res.json();
  alert(data.message || data.error);
});

// WEBSOCKET CHAT
const chatMessages = document.getElementById("chatMessages");
const chatInput = document.getElementById("chatInput");
const sendChat = document.getElementById("sendChat");

const ws = new WebSocket("ws://127.0.0.1:8000/ws/chat");

ws.onmessage = (event) => {
  const div = document.createElement("div");
  div.textContent = event.data;
  chatMessages.appendChild(div);
  chatMessages.scrollTop = chatMessages.scrollHeight;
};

sendChat.addEventListener("click", () => {
  const message = chatInput.value.trim();
  if (message) {
    ws.send(message);
    chatInput.value = "";
  }
});

chatInput.addEventListener("keypress", (e) => {
  if (e.key === "Enter") sendChat.click();
});