const chatBody = document.getElementById("chatBody");
const chatInput = document.getElementById("chatInput");

const botResponses = {
  default:
    "I'm your AI farming assistant 🌾. Ask me anything about rice diseases, prevention, fertilizers, or harvesting!",
  "bacterial leaf blight":
    "Bacterial Leaf Blight (BLB) is caused by Xanthomonas oryzae. It creates yellow-white lesions and can reduce yield by up to 50% if untreated.",
  "prevent rice":
    "Prevention tips:\n1. Use resistant varieties\n2. Avoid excess nitrogen\n3. Maintain spacing\n4. Ensure drainage\n5. Remove infected residues",
  "fertilizers":
    "Recommended fertilizers:\n• Nitrogen (N): 80–120 kg/ha\n• Phosphorus (P): 40–60 kg/ha\n• Potassium (K): 40–60 kg/ha\nSplit nitrogen into 3 stages.",
  "harvest":
    "Harvest rice when:\n• 80–85% grains are straw-colored\n• Grain moisture is 20–25%\n• Panicles droop naturally"
};

function addMessage(text, type) {
  const div = document.createElement("div");
  div.className = `chat-msg ${type} animate-slide`;
  div.innerText = text;
  chatBody.appendChild(div);
  chatBody.scrollTop = chatBody.scrollHeight;
}

async function sendMessage() {
  const text = chatInput.value.trim();
  if (!text) return;

  addMessage(text, "user");
  chatInput.value = "";

  showTyping();

  try {
    // Chatbot is a public endpoint - no auth required
    const response = await fetch("http://127.0.0.1:8000/chatbot", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: text })
    });
    if (!response.ok) {
      throw new Error(`Server error: ${response.status}`);
    }
    const data = await response.json();
    removeTyping();
    addMessage(data.response, "bot");
  } catch (error) {
    removeTyping();
    addMessage("Sorry, I'm unable to respond right now.", "bot");
  }
}

function quickAsk(text) {
  chatInput.value = text;
  sendMessage();
}

function showTyping() {
  const typing = document.createElement("div");
  typing.id = "typing";
  typing.className = "chat-msg bot typing";
  typing.innerText = "Typing...";
  chatBody.appendChild(typing);
}

function removeTyping() {
  const typing = document.getElementById("typing");
  if (typing) typing.remove();
}

addMessage(botResponses.default, "bot");
