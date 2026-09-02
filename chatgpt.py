
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(), override=True)


st.set_page_config(
    page_title="Your Custom Assistant",
    page_icon="💬",
    layout="wide"
)


st.markdown("""
<style>
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #f8fafc, #eef2ff);
    }

    /* Header */
    .main-title {
        text-align: center;
        font-size: 42px;
        font-weight: 800;
        margin-bottom: 5px;
        color: #111827;
    }

    .subtitle {
        text-align: center;
        color: #6b7280;
        font-size: 17px;
        margin-bottom: 30px;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: Purple;
    }

    section[data-testid="stSidebar"] * {
        color: black;
    }

    /* Input box */
    div[data-testid="stChatInput"] {
        position: fixed;
        bottom: 20px;
        right: 5%;
        width: 65%;
        z-index: 999;
    }

    /* Chat area spacing */
    .block-container {
        padding-bottom: 120px;
    }

    /* API key status */
    .status-box {
        padding: 12px;
        border-radius: 10px;
        margin-top: 10px;
        font-weight: 600;
        text-align: center;
    }

    .active {
        background: #dcfce7;
        color: #166534;
    }

    .inactive {
        background: #fee2e2;
        color: #991b1b;
    }
</style>
""", unsafe_allow_html=True)


st.markdown(
    '<div class="main-title">💬 Your Custom ChatGPT</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Your personal AI assistant powered by OpenAI</div>',
    unsafe_allow_html=True
)


if "messages" not in st.session_state:
    st.session_state.messages = []

if "api_key" not in st.session_state:
    st.session_state.api_key = ""



with st.sidebar:

    st.markdown("## ⚙️ Assistant Settings")

    st.markdown("---")

    api_key = st.text_input(
        "🔑 OpenAI API Key",
        type="password",
        placeholder="Enter your API key..."
    )

    if api_key:
        st.session_state.api_key = api_key

        st.markdown(
            '<div class="status-box active">🟢 Chat Active</div>',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            '<div class="status-box inactive">🔴 Enter API Key to Start</div>',
            unsafe_allow_html=True
        )

    st.markdown("---")

    system_message = st.text_input(
        "🤖 System Role",
        placeholder="You are a helpful assistant"
    )

    if not system_message:
        system_message = "You are a helpful assistant"



if st.session_state.api_key:

    # Create ChatOpenAI only after key is entered
    chat = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0.5,
        api_key=st.session_state.api_key
    )

    # Add system message
    if not any(
        isinstance(msg, SystemMessage)
        for msg in st.session_state.messages
    ):
        st.session_state.messages.insert(
            0,
            SystemMessage(content=system_message)
        )

    for msg in st.session_state.messages:

        if isinstance(msg, SystemMessage):
            continue

        if isinstance(msg, HumanMessage):
            with st.chat_message("user"):
                st.write(msg.content)

        elif isinstance(msg, AIMessage):
            with st.chat_message("assistant"):
                st.write(msg.content)

    user_prompt = st.chat_input(
        "Message your AI assistant..."
    )

    if user_prompt:

        # Show user message
        with st.chat_message("user"):
            st.write(user_prompt)

        # Add user message
        st.session_state.messages.append(
            HumanMessage(content=user_prompt)
        )

        # Generate response
        with st.chat_message("assistant"):

            with st.spinner("Thinking..."):

                try:
                    response = chat.invoke(
                        st.session_state.messages
                    )

                    st.write(response.content)

                    st.session_state.messages.append(
                        AIMessage(content=response.content)
                    )

                except Exception as e:

                    st.error(
                        f"Something went wrong: {str(e)}"
                    )

else:

    st.markdown(
        "<div style='text-align:center; margin-top:100px;'>"
        "<div style='font-size:70px;'>🔐</div>"
        "<h2>Welcome to Your Custom Assistant</h2>"
        "<p style='color:#6b7280; font-size:17px;'>"
        "Enter your OpenAI API key from the sidebar to activate the chat."
        "</p>"
        "<p style='color:#9ca3af;'>"
        "Your API key is used to connect your assistant with OpenAI."
        "</p>"
        "</div>",
        unsafe_allow_html=True
    )

 
