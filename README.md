Frontend Link:
https://ai-chatbot-project-go.streamlit.app
⚡ Nexus AI — Enterprise Conversational Intelligence

Nexus AI is a modern, high-performance conversational AI assistant built using **Streamlit**, **LangChain**, and **OpenAI's LLM API**. The application provides an interactive UI with dynamic authentication, system prompt customization, and session stats tracking.


 ✨ Features

🔒 Dynamic API Authentication:** The main interface stays locked until a valid OpenAI API Key (`sk-...`) is provided via the sidebar.
🎭 Custom Bot Persona:** Live updating of system prompts to change the assistant's behavior on the fly.
⚡ Real-Time Streaming:** Typing-effect stream responses for interactive user experience.
🔍 Chat Search & Filter:** Quickly filter past conversation messages using key terms.
📊 Live Session Metrics:** Real-time analytics tracking message count and total character count.
🗑️ One-Click Clear:** Option to clear active conversation history instantly.


 📂 Project Structure


project/
├── .env                # Environment variables configuration
├── .gitignore          # Files to ignore in Git repository
├── app.py              # Main Streamlit UI & LangChain logic
├── project.ipynb       # Jupyter notebook for testing & experiments
├── requirements.txt    # Project dependencies
└── README.md           # Project documentation
