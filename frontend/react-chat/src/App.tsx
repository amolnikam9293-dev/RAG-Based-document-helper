import { useState, useRef, useEffect } from "react";
// import type { ChatRequest, ChatResponse } from "./types";

// const API_URL = "http://127.0.0.1:8000/chat";

interface Message {
  role: "user" | "assistant";
  content: string;
}

function App() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState<string>("");
  const chatEndRef = useRef<HTMLDivElement | null>(null);
  const [isStreaming, setIsStreaming] = useState(false);

  const sessionId = "user-123";

  // const sendMessage = async (): Promise<void> => {
  //   if (!input.trim()) return;

  //   // Add user message
  //   setMessages((prev) => [...prev, { role: "user", content: input }]);

  //   const payload: ChatRequest = {
  //     session_id: sessionId,
  //     message: input,
  //   };

  //   const res = await fetch(API_URL, {
  //     method: "POST",
  //     headers: { "Content-Type": "application/json" },
  //     body: JSON.stringify(payload),
  //   });

  //   const data: ChatResponse = await res.json();

  //   setMessages((prev) => [
  //     ...prev,
  //     { role: "assistant", content: data.response },
  //   ]);

  //   setInput("");
  // };

  const API_URL = "http://127.0.0.1:8000/chat/stream";

  const sendMessage = async (): Promise<void> => {
    if (!input.trim()) return;

    setIsStreaming(true);

    // Add user message
    setMessages((prev) => [...prev, { role: "user", content: input }]);

    // Add empty assistant message (for streaming)
    let assistantMessage = "";
    setMessages((prev) => [...prev, { role: "assistant", content: "" }]);

    const payload = {
      session_id: sessionId,
      message: input,
    };

    const res = await fetch(API_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Accept: "text/event-stream",
      },
      body: JSON.stringify(payload),
    });

    if (!res.body) {
      console.error("No response body");
      return;
    }

    const reader = res.body.getReader();
    const decoder = new TextDecoder("utf-8");

    while (true) {
      const { value, done } = await reader.read();
      if (done) break;

      const chunk = decoder.decode(value, { stream: true });

      // Split SSE lines
      const lines = chunk.split("\n");

      for (const line of lines) {
        if (!line.startsWith("data:")) continue;

        const data = line.replace("data:", "").trim();

        if (data === "[DONE]") {
          setIsStreaming(false);
          setInput("");
          return;
        }

        try {
          const parsed = JSON.parse(data);
          const token = parsed.token;

          assistantMessage += token;

          setMessages((prev) => {
            const updated = [...prev];
            updated[updated.length - 1] = {
              role: "assistant",
              content: assistantMessage,
            };
            return updated;
          });
        } catch (e) {
          console.error("Failed to parse token", e);
        }
      }
    }

    setIsStreaming(false);
  };

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  function TypingDots() {
    return (
      <span style={{ display: "inline-flex", gap: 4 }}>
        <Dot />
        <Dot delay="0.2s" />
        <Dot delay="0.4s" />
      </span>
    );
  }

  function Dot({ delay = "0s" }: { delay?: string }) {
    return (
      <span
        style={{
          width: 6,
          height: 6,
          backgroundColor: "#555",
          borderRadius: "50%",
          display: "inline-block",
          animation: `blink 1.4s infinite both`,
          animationDelay: delay,
        }}
      />
    );
  }

  return (
    <div
      style={{
        height: "100vh",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        background: "#f5f5f5",
      }}
    >
      <div
        style={{
          width: "100%",
          maxWidth: "800px",
          height: "90vh",
          display: "flex",
          flexDirection: "column",
          background: "#fff",
          borderRadius: 12,
          boxShadow: "0 10px 30px rgba(0,0,0,0.1)",
          overflow: "hidden",
        }}
      >
        {/* Header */}
        <div
          style={{
            padding: "16px",
            borderBottom: "1px solid #eee",
            fontSize: "18px",
            fontWeight: 600,
          }}
        >
          🤖 RAG Chat Assistant
        </div>

        {/* Chat area */}
        <div
          id="chat-container"
          style={{
            flex: 1,
            padding: "16px",
            overflowY: "auto",
            background: "#fafafa",
          }}
        >
          {messages.map((m, i) => (
            <div
              key={i}
              style={{
                display: "flex",
                alignItems: "flex-end",
                justifyContent: m.role === "user" ? "flex-end" : "flex-start",
                marginBottom: 12,
                gap: 8,
              }}
            >
              {/* Assistant avatar */}
              {m.role === "assistant" && (
                <div
                  style={{
                    width: 32,
                    height: 32,
                    borderRadius: "50%",
                    background: "#007bff",
                    color: "#fff",
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    fontSize: 16,
                  }}
                >
                  🤖
                </div>
              )}

              {/* Message bubble */}
              <div
                style={{
                  maxWidth: "70%",
                  padding: "10px 14px",
                  borderRadius: 16,
                  background: m.role === "user" ? "#007bff" : "#e5e5ea",
                  color: m.role === "user" ? "#fff" : "#000",
                  whiteSpace: "pre-wrap",
                  lineHeight: 1.4,
                }}
              >
                {m.content ||
                  (m.role === "assistant" && isStreaming && <TypingDots />)}
              </div>

              {/* User avatar */}
              {m.role === "user" && (
                <div
                  style={{
                    width: 32,
                    height: 32,
                    borderRadius: "50%",
                    background: "#666",
                    color: "#fff",
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    fontSize: 16,
                  }}
                >
                  🙂
                </div>
              )}
            </div>
          ))}

          <div ref={chatEndRef} />
        </div>

        {/* Input */}
        <div
          style={{
            display: "flex",
            padding: "12px",
            borderTop: "1px solid #eee",
            background: "#fff",
          }}
        >
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && sendMessage()}
            placeholder="Ask a question..."
            style={{
              flex: 1,
              padding: "12px",
              borderRadius: 20,
              border: "1px solid #ccc",
              outline: "none",
              fontSize: 14,
            }}
          />
          <button
            disabled={isStreaming}
            onClick={sendMessage}
            style={{
              opacity: isStreaming ? 0.6 : 1,
              marginLeft: 10,
              padding: "0 20px",
              borderRadius: 20,
              border: "none",
              background: "#007bff",
              color: "#fff",
              cursor: "pointer",
            }}
          >
            Send
          </button>
        </div>
      </div>
    </div>
  );
}

export default App;
