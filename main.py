# app/main.py
import streamlit as st
import os
from datetime import datetime
from app.auth_utils import is_logged_in, get_credentials, logout
from app.app import CalendarAgent

# Page configuration
st.set_page_config(
    page_title="AI Calendar Assistant",
    page_icon="📅",
    layout="wide"
)

# Custom CSS for better UI
st.markdown("""
    <style>
    .stTextInput>div>div>input {
        padding: 12px;
        border-radius: 8px;
    }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        padding: 0.5rem 1rem;
    }
    .message {
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        max-width: 80%;
    }
    .user-message {
        background-color: #e3f2fd;
        margin-left: auto;
        margin-right: 0;
    }
    .ai-message {
        background-color: #f5f5f5;
    }
    .header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'agent' not in st.session_state:
    st.session_state.agent = None
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = is_logged_in()

def initialize_agent():
    """Initialize the calendar agent if not already done"""
    if st.session_state.agent is None:
        with st.spinner("Initializing AI assistant..."):
            st.session_state.agent = CalendarAgent()

def handle_logout():
    """Handle user logout"""
    if logout():
        st.session_state.logged_in = False
        st.session_state.agent = None
        st.session_state.messages = []

def handle_login():
    """Handle user login"""
    creds = get_credentials()
    if creds:
        st.session_state.logged_in = True
        initialize_agent()

def add_message(role, content):
    """Add a message to the chat"""
    st.session_state.messages.append({
        "role": role,
        "content": content,
        "time": datetime.now().strftime("%H:%M")
    })

def handle_submit():
    """Handle message submission"""
    user_input = st.session_state.user_input.strip()
    if user_input:
        # Add user message
        add_message("user", user_input)
        
        # Clear input immediately
        st.session_state.user_input = ""
        
        # Get AI response
        try:
            response = st.session_state.agent.process_message(user_input)
            add_message("assistant", response)
        except Exception as e:
            add_message("assistant", f"Sorry, I encountered an error: {str(e)}")

# Main app
def main():
    st.title("📅 AI Calendar Assistant")
    
    # Login/Logout button
    col1, col2 = st.columns([4, 1])
    with col2:
        if st.session_state.logged_in:
            if st.button("Logout", type="primary", on_click=handle_logout):
                st.rerun()
                
        else:
            if st.button("Login with Google", type="primary", on_click=handle_login):
                st.rerun()
                
    
    # Show login message if not logged in
    if not st.session_state.logged_in:
        st.warning("Please login to use the AI Calendar Assistant")
        return
    
    # Initialize agent if not already done
    if st.session_state.agent is None:
        initialize_agent()
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
            st.caption(f"at {message['time']}")
    
    # Input area
    with st.form("chat_form", clear_on_submit=True):
        col1, col2 = st.columns([5, 1])
        with col1:
            st.text_input(
                "Your message",
                key="user_input",
                label_visibility="collapsed",
                placeholder="Ask me about your calendar..."
            )
        with col2:
            st.form_submit_button("Send", on_click=handle_submit)

if __name__ == "__main__":
    main()