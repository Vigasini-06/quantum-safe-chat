import { useState, useEffect } from "react";
import "./App.css";

function App() {
  
  const [loggedIn, setLoggedIn] = useState(false);
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState([]);
useEffect(() => {
  if (loggedIn) {
    generateKeys();
  }
}, [loggedIn]);
const generateKeys = async () => {
  try {
    const response = await fetch(
      "http://127.0.0.1:8000/keys/generate",
      {
        method: "POST"
      }
    );

    const data = await response.json();

    console.log("Quantum-safe keys:", data);

  } catch (error) {
    console.error("Key generation failed:", error);
  }
};
 const sendMessage = async () => {
  if (!message.trim()) return;

  try {
    const response = await fetch(
      "http://127.0.0.1:8000/messages/encrypt",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          message: message
        })
      }
    );

    const data = await response.json();

    if (!response.ok) {
      alert(data.detail || "Encryption failed");
      return;
    }

    setMessages([
      ...messages,
      {
        text: message,
        sender: "You",
        secure: true,
        encrypted: data.encrypted_message,
        signature: data.signature,
        kemCiphertext: data.kem_ciphertext,
        nonce: data.nonce
      }
    ]);

    setMessage("");

  } catch (error) {
    console.error(error);

    alert(
      "Could not connect to the Quantum-Safe Chat backend."
    );
  }
};

  if (loggedIn) {
    return (
      <div className="chat-app">

        {/* SIDEBAR */}
        <aside className="sidebar">

          <div className="sidebar-header">
            <div className="small-logo">QS</div>
            <div>
              <h2>Quantum-Safe</h2>
              <span>Secure Chat</span>
            </div>
          </div>

          <div className="security-status">
            <div className="status-dot"></div>
            <div>
              <strong>Quantum-Safe</strong>
              <small>Protection active</small>
            </div>
          </div>

          <div className="contact-title">
            Conversations
          </div>

          <div className="contact active-contact">
            <div className="avatar">B</div>
            <div>
              <strong>Bob</strong>
              <small>Secure conversation</small>
            </div>
          </div>

          <button
            className="logout-button"
            onClick={() => setLoggedIn(false)}
          >
            Sign Out
          </button>

        </aside>

        {/* CHAT AREA */}
        <main className="chat-area">

          <header className="chat-header">

            <div>
              <h2>Bob</h2>
              <span>End-to-end protected conversation</span>
            </div>

            <div className="encryption-indicator">
              🔒 Encrypted
            </div>

          </header>

          <section className="messages">

            {messages.length === 0 && (
              <div className="empty-chat">
                <div className="empty-icon">🔐</div>

                <h2>Secure Conversation</h2>

                <p>
                  Messages in this conversation are protected
                  using post-quantum cryptography.
                </p>

                <div className="algorithm-list">
                  <span>ML-KEM-768</span>
                  <span>AES-256-GCM</span>
                  <span>ML-DSA-65</span>
                </div>
              </div>
            )}

            {messages.map((msg, index) => (
              <div
                key={index}
                className="message-wrapper"
              >
                <div className="message-bubble">
                  <p>{msg.text}</p>

                  <div className="message-security">
                    ✓ Encrypted &nbsp; ✓ Signed
                  </div>
                </div>
              </div>
            ))}

          </section>

          <div className="message-input-area">

            <input
              type="text"
              value={message}
              placeholder="Type a secure message..."
              onChange={(e) => setMessage(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter") {
                  sendMessage();
                }
              }}
            />

            <button onClick={sendMessage}>
              Send
            </button>

          </div>

        </main>

      </div>
    );
  }

  return (
    <div className="app-container">

      <div className="security-panel">

        <div className="logo">QS</div>

        <h1>Quantum-Safe Chat</h1>

        <p className="tagline">
          Secure communication for the post-quantum era.
        </p>

        <div className="security-items">

          <div>
            <span>✓</span>
            ML-KEM-768 Key Exchange
          </div>

          <div>
            <span>✓</span>
            AES-256-GCM Encryption
          </div>

          <div>
            <span>✓</span>
            ML-DSA-65 Digital Signatures
          </div>

        </div>

      </div>

      <div className="login-panel">

        <div className="login-box">

          <h2>Welcome Back</h2>

          <p className="login-subtitle">
            Sign in to your secure conversations
          </p>

          <div className="input-group">
            <label>Email</label>

            <input
              type="email"
              placeholder="Enter your email"
            />
          </div>

          <div className="input-group">
            <label>Password</label>

            <input
              type="password"
              placeholder="Enter your password"
            />
          </div>

          <button
            className="primary-button"
            onClick={() => setLoggedIn(true)}
          >
            Sign In
          </button>

          <div className="security-badge">
            🔒 Quantum-Safe Cryptography Enabled
          </div>

        </div>

      </div>

    </div>
  );
}

export default App;