
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(), override=True)

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Fashion AI Assistant",
    page_icon="👗",
    layout="wide"
)

# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown("""
<style>

    /* Main Background */
    .stApp {
        background: linear-gradient(135deg, #f8fafc, #eef2ff);
    }

    /* Main Title */
    .main-title {
        text-align: center;
        font-size: 42px;
        font-weight: 800;
        margin-bottom: 5px;
        color: #111827;
    }

    /* Subtitle */
    .subtitle {
        text-align: center;
        color: #6b7280;
        font-size: 17px;
        margin-bottom: 30px;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: #e9d5ff;
    }

    section[data-testid="stSidebar"] * {
        color: #111827;
    }

    /* Input Box */
    div[data-testid="stChatInput"] {
        position: fixed;
        bottom: 20px;
        right: 5%;
        width: 65%;
        z-index: 999;
    }

    /* Chat Area */
    .block-container {
        padding-bottom: 120px;
    }

    /* Status Box */
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

    /* Fashion Welcome Box */
    .welcome-box {
        text-align: center;
        margin-top: 80px;
        padding: 35px;
        border-radius: 20px;
        background: rgba(255,255,255,0.7);
        box-shadow: 0 8px 30px rgba(0,0,0,0.08);
    }

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.markdown(
    '<div class="main-title">👗 Your Fashion AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Your personal AI fashion stylist powered by OpenAI'
    '</div>',
    unsafe_allow_html=True
)

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "api_key" not in st.session_state:
    st.session_state.api_key = ""

if "key_status" not in st.session_state:
    st.session_state.key_status = None

if "chat" not in st.session_state:
    st.session_state.chat = None

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.markdown("## ⚙️ Fashion Assistant Settings")

    st.markdown("---")

    # API KEY
    api_key = st.text_input(
        "🔑 OpenAI API Key",
        type="password",
        placeholder="Enter your API key..."
    )

    # --------------------------------------------------
    # CHECK API KEY IMMEDIATELY
    # --------------------------------------------------

    if api_key:

        # Only check if key changed
        if api_key != st.session_state.api_key:

            st.session_state.api_key = api_key

            with st.spinner("🔍 Checking API key..."):

                try:

                    test_chat = ChatOpenAI(
                        model="gpt-4o-mini",
                        temperature=0,
                        api_key=api_key
                    )

                    # Small test request
                    test_chat.invoke(
                        "Reply with only: OK"
                    )

                    # Key is valid
                    st.session_state.key_status = "valid"

                    st.session_state.chat = ChatOpenAI(
                        model="gpt-4o-mini",
                        temperature=0.5,
                        api_key=api_key
                    )

                except Exception:
                    st.session_state.key_status = "invalid"
                    st.session_state.chat = None

        # Show status
        if st.session_state.key_status == "valid":

            st.markdown(
                '<div class="status-box active">'
                '🟢 API Key Verified — Chat Active'
                '</div>',
                unsafe_allow_html=True
            )

        elif st.session_state.key_status == "invalid":

            st.markdown(
                '<div class="status-box inactive">'
                '🔴 Invalid API Key'
                '</div>',
                unsafe_allow_html=True
            )

            st.warning(
                "Please check your API key and enter it again."
            )

    else:

        st.session_state.key_status = None
        st.session_state.chat = None

        st.markdown(
            '<div class="status-box inactive">'
            '🔴 Enter API Key to Start'
            '</div>',
            unsafe_allow_html=True
        )

    st.markdown("---")

    # SYSTEM ROLE
    st.markdown("### 🤖 Assistant Role")

    st.info(
        "This assistant is specially designed "
        "for fashion-related questions only."
    )

    st.markdown("---")

    # CLEAR CHAT
    if st.button("🗑️ Clear Chat", use_container_width=True):

        st.session_state.messages = []

        st.rerun()

# --------------------------------------------------
# FASHION SYSTEM PROMPT
# --------------------------------------------------

FASHION_SYSTEM_MESSAGE = """
You are a professional Fashion AI Assistant.

Your ONLY purpose is to help users with fashion-related topics.

You can answer questions about:

- 👗 Clothing
- 👔 Men's fashion
- 👚 Women's fashion
- 👖 Outfit ideas
- 👠 Shoes
- 👜 Accessories
- 🎨 Clothing color combinations
- 💄 Fashion styling
- 💇 Hairstyle suggestions related to outfits
- 🧥 Seasonal fashion
- 💍 Jewelry styling
- 🕶️ Fashion accessories
- 👰 Wedding and party outfits
- 💼 Office and professional outfits
- 🏖️ Casual and vacation outfits
- 👟 Sneakers and footwear styling
- 📏 Body-type based styling
- 🌈 Color matching
- ✨ Fashion trends
- 🛍️ Clothing recommendations
- 🧵 Fabrics and clothing materials
- 👗 Dress styling

IMPORTANT:

If the user asks something that is NOT related to fashion,
do NOT answer the question.

Instead, politely respond:

"Sorry! 👗 I’m your Fashion AI Assistant, so I can only help with fashion, outfits, styling, clothing, colors, accessories, and related fashion topics. Please ask me a fashion-related question. ✨"

Do not provide answers about programming, mathematics,
politics, general knowledge, medicine, finance, technology,
history, or other unrelated subjects.

Keep your answers friendly, helpful, stylish, and professional.

When giving outfit suggestions, consider:
- Occasion
- Season
- Colors
- Personal style
- Gender when relevant
- Formality
- Comfort
- Current fashion trends
"""

# --------------------------------------------------
# CHAT AREA
# --------------------------------------------------

if (
    st.session_state.api_key
    and st.session_state.key_status == "valid"
    and st.session_state.chat
):

    # Display previous messages

    for msg in st.session_state.messages:

        if isinstance(msg, HumanMessage):

            with st.chat_message("user"):
                st.write(msg.content)

        elif isinstance(msg, AIMessage):

            with st.chat_message("assistant"):
                st.write(msg.content)

    # --------------------------------------------------
    # USER INPUT
    # --------------------------------------------------

    user_prompt = st.chat_input(
        "✨ Ask me anything about fashion..."
    )

    if user_prompt:

        # Show user message
        with st.chat_message("user"):
            st.write(user_prompt)

        # Add user message
        st.session_state.messages.append(
            HumanMessage(content=user_prompt)
        )

        # --------------------------------------------------
        # GENERATE RESPONSE
        # --------------------------------------------------

        with st.chat_message("assistant"):

            with st.spinner("👗 Styling your answer..."):

                try:

                    # Create complete conversation
                    conversation = [
                        SystemMessage(
                            content=FASHION_SYSTEM_MESSAGE
                        )
                    ] + st.session_state.messages

                    response = st.session_state.chat.invoke(
                        conversation
                    )

                    st.write(response.content)

                    # Save AI response
                    st.session_state.messages.append(
                        AIMessage(
                            content=response.content
                        )
                    )

                except Exception as e:

                    st.error(
                        f"❌ Something went wrong: {str(e)}"
                    )

# --------------------------------------------------
# NO API KEY / INVALID KEY
# --------------------------------------------------

else:
    st.markdown(
        """
        <div style="
            text-align:center;
            margin-top:120px;
            padding:40px;
        ">

            <div style="
                font-size:80px;
                margin-bottom:20px;
            ">
                👗✨
            </div>

            <h1 style="
                color:#5b21b6;
                font-size:42px;
                font-weight:800;
                margin-bottom:10px;
            ">
                Welcome to Your Fashion AI
            </h1>

            <p style="
                color:#4b5563;
                font-size:19px;
                margin-bottom:30px;
            ">
                Your personal AI fashion stylist
            </p>

            <div style="
                display:inline-block;
                padding:15px 30px;
                border-radius:30px;
                background:#f3e8ff;
                color:#4c1d95;
                font-size:16px;
                font-weight:600;
            ">
                👗 Outfit Ideas
                &nbsp;&nbsp; • &nbsp;&nbsp;
                🎨 Color Matching
                &nbsp;&nbsp; • &nbsp;&nbsp;
                👠 Styling
                &nbsp;&nbsp; • &nbsp;&nbsp;
                ✨ Trends
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

