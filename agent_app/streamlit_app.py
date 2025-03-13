import streamlit as st
from typing import List, Dict
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from agent_service.chat_service import ChatService
import logging
from streamlit.runtime.scriptrunner import RerunData, RerunException
from streamlit.runtime.state import SessionState

def main():
    st.title("Student Portal Chatbot")

    # Initialize chat service in session state if it doesn't exist
    if "chat_service" not in st.session_state:
        st.session_state.chat_service = ChatService()

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # For demo purposes, the username is input by the user
    student_id = st.sidebar.text_input("Enter your student ID", value="1")

    # Display chat message history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Ask about your courses, credits, etc."):
        # Add user message to display history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Display user message
        with st.chat_message("user"):
            st.write(prompt)

        try:
            # Get response from chat service
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = st.session_state.chat_service.process_message(student_id, prompt)
                st.write(response)

            # Add response to display history
            st.session_state.messages.append({"role": "assistant", "content": response})

        except Exception as e:
            error_msg = f"Error: {str(e)}"
            st.error(error_msg)
            st.session_state.messages.append({"role": "assistant", "content": "I'm sorry, I encountered an error. Please try again."})

if __name__ == "__main__":
    main()
