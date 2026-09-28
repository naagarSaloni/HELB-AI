const API_BASE_URL = "http://127.0.0.1:8000/api";

export async function sendMessage(question, conversationId = null) {
  const response = await fetch(`${API_BASE_URL}/chat`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      question,
      conversation_id: conversationId,
    }),
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error.detail || "Failed to communicate with HELB AI.");
  }

  return response.json();
}

export async function getConversation(conversationId) {
  const response = await fetch(
    `${API_BASE_URL}/conversations/${conversationId}`
  );

  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error.detail || "Failed to load conversation.");
  }

  return response.json();
}