// frontend/src/App.js
import { useState } from "react";

function App() {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);
  const [sessionId, setSessionId] = useState("");

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = input;
    setMessages([...messages, { type: "user", text: userMessage }]);
    setInput("");

    const response = await fetch("http://localhost:8000/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: userMessage, session_id: sessionId }),
    });

    const data = await response.json();
    setSessionId(data.session_id);
    setMessages(prev => [...prev, { type: "bot", text: data.reply }]);
  };

  return (
    <div style={{ padding: "2rem", fontFamily: "Arial" }}>
      <h2>Chatbot</h2>
      <div style={{ marginBottom: "1rem", height: "300px", overflowY: "scroll", border: "1px solid #ccc", padding: "1rem" }}>
        {messages.map((msg, i) => (
          <p key={i} style={{ textAlign: msg.type === "user" ? "right" : "left" }}>
            <b>{msg.type === "user" ? "You" : "Bot"}:</b> {msg.text}
          </p>
        ))}
      </div>
      <input
        type="text"
        value={input}
        onChange={e => setInput(e.target.value)}
        onKeyDown={e => e.key === "Enter" && sendMessage()}
        placeholder="Type your message..."
        style={{ padding: "0.5rem", width: "80%" }}
      />
      <button onClick={sendMessage} style={{ padding: "0.5rem" }}>Send</button>
    </div>
  );
}

export default App;
