import { useEffect, useRef, useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

import { sendMessage } from "./services/api";

import "./index.css";


const categories = [
  {
    id: "loans",
    icon: "🎓",
    title: "Loans & Applications",
    description: "Apply for a HELB loan and check requirements",

    options: [
      "How do I apply for a HELB loan?",
      "What are the requirements for an undergraduate loan?",
      "What are undergraduate loans?",
      "What are TVET loans?",
      "What is the HELB loan application process?",
    ],
  },

  {
    id: "repayment",
    icon: "💳",
    title: "Loan Repayment",
    description: "Repayment methods, balance and statements",

    options: [
      "How do I repay my HELB loan?",
      "Can I repay my HELB loan using M-PESA?",
      "What are the HELB loan repayment methods?",
      "How can I check my HELB loan balance?",
      "How can I get my HELB loan statement?",
    ],
  },

  {
    id: "scholarships",
    icon: "🎓",
    title: "Scholarships",
    description: "HELB scholarships and eligibility information",

    options: [
      "What scholarships does HELB offer?",
      "What are the scholarship requirements?",
      "What is the Post Graduate Scholarship?",
      "How do I apply for a HELB scholarship?",
    ],
  },

  {
    id: "requirements",
    icon: "📋",
    title: "Requirements & FAQs",
    description: "General HELB information and requirements",

    options: [
      "What are the HELB eligibility requirements?",
      "What documents are required?",
      "What are the Student FAQs?",
      "What general services does HELB provide?",
    ],
  },

  {
    id: "deadlines",
    icon: "📅",
    title: "Deadlines",
    description: "Application deadlines and important dates",

    options: [
      "What are the HELB loan application deadlines?",
      "What are the scholarship deadlines?",
      "What are the important HELB dates?",
    ],
  },

  {
    id: "support",
    icon: "🧑‍💼",
    title: "Talk to Support",
    description: "Create a support ticket for human assistance",

    options: [
      "I need human support",
      "My problem is not listed",
      "I cannot find the information I need",
    ],
  },
];


function App() {
  const [messages, setMessages] = useState([]);

  const [input, setInput] = useState("");

  const [conversationId, setConversationId] = useState(null);

  const [loading, setLoading] = useState(false);

  const [selectedCategory, setSelectedCategory] = useState(null);

  const messagesEndRef = useRef(null);

  const inputRef = useRef(null);


  // ==========================================================
  // AUTO SCROLL
  // ==========================================================

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [
    messages,
    loading,
    selectedCategory,
  ]);


  // ==========================================================
  // ADD MESSAGE
  // ==========================================================

  const addMessage = (
    role,
    content,
    extra = {}
  ) => {
    setMessages((previous) => [
      ...previous,

      {
        id: `${Date.now()}-${Math.random()}`,

        role,

        content,

        ...extra,
      },
    ]);
  };


  // ==========================================================
  // NEW CHAT
  // ==========================================================

  const handleNewChat = () => {
    setMessages([]);

    setInput("");

    setConversationId(null);

    setSelectedCategory(null);

    setTimeout(() => {
      inputRef.current?.focus();
    }, 100);
  };


  // ==========================================================
  // SEND MESSAGE
  // ==========================================================

  const handleSend = async (
    question = input
  ) => {
    const cleanQuestion = question.trim();

    if (!cleanQuestion || loading) {
      return;
    }

    setInput("");

    setSelectedCategory(null);

    // Show user message immediately
    addMessage(
      "user",
      cleanQuestion
    );

    setLoading(true);

    try {
      const result = await sendMessage(
        cleanQuestion,
        conversationId
      );

      // Save conversation ID
      if (result.conversation_id) {
        setConversationId(
          result.conversation_id
        );
      }

      // Add assistant response
      addMessage(
        "assistant",

        result.answer ||
          "I couldn't generate a response.",

        {
          sources:
            result.sources || [],

          ticketId:
            result.ticket_id || null,

          ticketStatus:
            result.ticket_status || null,

          escalate:
            result.escalate || false,

          evidenceSupported:
            result.evidence_supported ?? false,

          agent:
            result.agent || null,

          intent:
            result.intent || null,
        }
      );
    } catch (error) {
      addMessage(
        "assistant",

        `Sorry, I couldn't connect to the HELB support service.

**Error:** ${error.message}`
      );
    } finally {
      setLoading(false);

      setTimeout(() => {
        inputRef.current?.focus();
      }, 100);
    }
  };


  // ==========================================================
  // CATEGORY CLICK
  // ==========================================================

  const handleCategoryClick = (
    category
  ) => {
    setSelectedCategory(category);
  };


  // ==========================================================
  // SUBCATEGORY CLICK
  // ==========================================================

  const handleOptionClick = (
    option
  ) => {
    handleSend(option);
  };


  // ==========================================================
  // BACK TO CATEGORIES
  // ==========================================================

  const handleBackToCategories = () => {
    setSelectedCategory(null);
  };


  // ==========================================================
  // RENDER
  // ==========================================================

  return (
    <div className="app">

      <div className="chat-shell">

        {/* ==================================================
            HEADER
        ================================================== */}

        <header className="chat-header">

          <div className="brand">

            <div className="brand-logo">
              H
            </div>

            <div className="brand-info">

              <div className="brand-title">
                HELB AI
              </div>

              <div className="brand-subtitle">
                Official HELB Support Assistant
              </div>

            </div>

          </div>


          <div className="header-right">

            <div className="online-status">

              <span className="online-dot"></span>

              Online

            </div>


            <button
              className="new-chat-button"
              onClick={handleNewChat}
            >
              + New chat
            </button>

          </div>

        </header>


        {/* ==================================================
            CHAT BODY
        ================================================== */}

        <main className="chat-body">

          {/* ==================================================
              WELCOME SCREEN
          ================================================== */}

          {messages.length === 0 && (

            <div className="welcome-screen">

              <div className="welcome-avatar">
                H
              </div>


              <div className="welcome-title">
                Hello! 👋
              </div>


              <p className="welcome-description">
                I'm the HELB AI Support Agent.
                I can help you with loans,
                repayment, scholarships,
                requirements and other HELB
                services.
              </p>


              <p className="welcome-question">
                What would you like help with?
              </p>


              {/* ==================================================
                  MAIN CATEGORIES
              ================================================== */}

              {!selectedCategory && (

                <div className="topic-section">

                  <div className="topic-title">
                    Choose a topic
                  </div>


                  <div className="category-grid">

                    {categories.map(
                      (category) => (

                        <button
                          key={category.id}
                          className="category-card"

                          onClick={() =>
                            handleCategoryClick(
                              category
                            )
                          }
                        >

                          <div className="category-icon">
                            {category.icon}
                          </div>


                          <div className="category-content">

                            <div className="category-title">
                              {category.title}
                            </div>


                            <div className="category-description">
                              {category.description}
                            </div>

                          </div>


                          <div className="category-arrow">
                            →
                          </div>

                        </button>

                      )
                    )}

                  </div>

                </div>

              )}


              {/* ==================================================
                  SUBCATEGORIES
              ================================================== */}

              {selectedCategory && (

                <div className="subcategory-section">

                  <div className="subcategory-header">

                    <button
                      className="back-button"
                      onClick={
                        handleBackToCategories
                      }
                    >
                      ← Back
                    </button>


                    <div className="subcategory-heading">

                      <span>
                        {selectedCategory.icon}
                      </span>

                      {selectedCategory.title}

                    </div>

                  </div>


                  <div className="subcategory-list">

                    {selectedCategory.options.map(
                      (option, index) => (

                        <button
                          key={index}

                          className="subcategory-button"

                          onClick={() =>
                            handleOptionClick(
                              option
                            )
                          }
                        >

                          <span>
                            {option}
                          </span>

                          <span>
                            →
                          </span>

                        </button>

                      )
                    )}

                  </div>

                </div>

              )}

            </div>

          )}


          {/* ==================================================
              CONVERSATION
          ================================================== */}

          {messages.length > 0 && (

            <div className="messages-container">

              {messages.map(
                (message) => (

                  <div
                    key={message.id}

                    className={`message-row ${message.role}`}
                  >

                    {/* Assistant avatar */}

                    {message.role ===
                      "assistant" && (

                      <div className="message-avatar">
                        H
                      </div>

                    )}


                    {/* Message bubble */}

                    <div
                      className={`message-bubble ${message.role}`}
                    >

                      {/* ==================================================
                          ASSISTANT MESSAGE
                      ================================================== */}

                      {message.role ===
                        "assistant" ? (

                        <div className="markdown-content">

                          <ReactMarkdown
                            remarkPlugins={[
                              remarkGfm,
                            ]}

                            components={{
                              a: ({
                                node,
                                ...props
                              }) => (

                                <a
                                  {...props}

                                  target="_blank"

                                  rel="noopener noreferrer"
                                />

                              ),
                            }}
                          >
                            {message.content}
                          </ReactMarkdown>

                        </div>

                      ) : (

                        /* ==================================================
                           USER MESSAGE
                        ================================================== */

                        <div className="user-message-content">
                          {message.content}
                        </div>

                      )}


                      {/* ==================================================
                          ESCALATION TICKET
                      ================================================== */}

                      {message.escalate &&
                        message.ticketId && (

                        <div className="ticket-card">

                          <div className="ticket-icon">
                            ✓
                          </div>


                          <div>

                            <div className="ticket-title">
                              Support ticket created
                            </div>


                            <div className="ticket-id">
                              {message.ticketId}
                            </div>


                            <div className="ticket-status">
                              Status:{" "}
                              {message.ticketStatus ||
                                "open"}
                            </div>

                          </div>

                        </div>

                      )}


                      {/* ==================================================
                          OFFICIAL SOURCES
                      ================================================== */}

                      {message.sources?.length >
                        0 && (

                        <div className="sources-section">

                          <div className="sources-title">
                            Official HELB sources
                          </div>


                          {message.sources
                            .slice(0, 3)
                            .map(
                              (
                                source,
                                index
                              ) => (

                                <a
                                  key={index}

                                  className="source-item"

                                  href={
                                    source.url
                                  }

                                  target="_blank"

                                  rel="noopener noreferrer"
                                >

                                  <span className="source-icon">
                                    ↗
                                  </span>


                                  <span>
                                    {source.name ||
                                      "Official HELB source"}
                                  </span>

                                </a>

                              )
                            )}

                        </div>

                      )}

                    </div>

                  </div>

                )
              )}


              {/* ==================================================
                  TYPING INDICATOR
              ================================================== */}

              {loading && (

                <div className="message-row assistant">

                  <div className="message-avatar">
                    H
                  </div>


                  <div className="typing-bubble">

                    <span></span>
                    <span></span>
                    <span></span>

                  </div>

                </div>

              )}


              {/* ==================================================
                  CONTINUE HELP
              ================================================== */}

              {!loading && (

                <div className="continue-help">

                  <div className="continue-help-title">
                    What else can I help you with?
                  </div>


                  {!selectedCategory && (

                    <div className="continue-help-options">

                      {categories.map(
                        (category) => (

                          <button
                            key={category.id}

                            className="continue-option"

                            onClick={() =>
                              handleCategoryClick(
                                category
                              )
                            }
                          >

                            <span className="continue-option-icon">
                              {category.icon}
                            </span>


                            <span className="continue-option-text">
                              {category.title}
                            </span>


                            <span className="continue-option-arrow">
                              →
                            </span>

                          </button>

                        )
                      )}

                    </div>

                  )}


                  {/* ==================================================
                      CONVERSATION SUBCATEGORY
                  ================================================== */}

                  {selectedCategory && (

                    <div className="conversation-subcategory">

                      <div className="conversation-subcategory-header">

                        <button
                          className="back-button"

                          onClick={
                            handleBackToCategories
                          }
                        >
                          ← Back
                        </button>


                        <div className="subcategory-heading">

                          <span>
                            {selectedCategory.icon}
                          </span>

                          {selectedCategory.title}

                        </div>

                      </div>


                      <div className="subcategory-list">

                        {selectedCategory.options.map(
                          (
                            option,
                            index
                          ) => (

                            <button
                              key={index}

                              className="subcategory-button"

                              onClick={() =>
                                handleOptionClick(
                                  option
                                )
                              }
                            >

                              <span>
                                {option}
                              </span>


                              <span>
                                →
                              </span>

                            </button>

                          )
                        )}

                      </div>

                    </div>

                  )}

                </div>

              )}


              <div ref={messagesEndRef} />

            </div>

          )}

        </main>


        {/* ==================================================
            INPUT AREA
        ================================================== */}

        <footer className="input-area">

          <div className="input-wrapper">

            <input
              ref={inputRef}

              type="text"

              value={input}

              onChange={(event) =>
                setInput(
                  event.target.value
                )
              }

              onKeyDown={(event) => {

                if (
                  event.key === "Enter" &&
                  !event.shiftKey
                ) {

                  event.preventDefault();

                  handleSend();

                }

              }}

              placeholder="Ask anything about HELB..."

              disabled={loading}
            />


            <button
              className="send-button"

              onClick={() =>
                handleSend()
              }

              disabled={
                !input.trim() ||
                loading
              }

              aria-label="Send message"
            >
              ↑
            </button>

          </div>


          <div className="input-disclaimer">
            HELB AI uses official HELB information
            to answer your questions.
          </div>

        </footer>

      </div>

    </div>
  );
}


export default App;