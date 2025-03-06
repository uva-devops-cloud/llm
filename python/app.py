import os
import streamlit as st
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure page
st.set_page_config(
    page_title="Claude Chatbot",
    page_icon="🤖",
    layout="wide"
)

def get_or_create_chat_history():
    """Initialize or get existing chat history"""
    if "messages" not in st.session_state:
        # Define system prompt
        system_prompt = """You are Claude, a helpful, harmless, and honest AI assistant.
        You excel at having thoughtful conversations and providing detailed, accurate information.
        You respond in a friendly, conversational manner while being precise and informative."""

        st.session_state.messages = [
            SystemMessage(content=system_prompt)
        ]
    return st.session_state.messages

def get_llm():
    """Initialize the Claude model"""
    return ChatAnthropic(
        anthropic_api_key=os.getenv("ANTHROPIC_API_KEY"),
        model="claude-3-haiku-20240307",  # More responsive model for testing
        temperature=0.7,
        max_tokens=1024,
        streaming=True
    )

def main():
    st.title("🤖 Claude Chatbot")
    st.subheader("LLM based student portal")

    # Get chat history
    messages = get_or_create_chat_history()

    # Initialize LLM
    llm = get_llm()

    # Display chat history (skip system message)
    for msg in messages:
        if not isinstance(msg, SystemMessage):
            if isinstance(msg, HumanMessage):
                with st.chat_message("user"):
                    st.write(msg.content)
            else:
                with st.chat_message("assistant"):
                    st.write(msg.content)

    # Get user input
    user_input = st.chat_input("Ask Claude something...")

    if user_input:
        # Add user message to chat history
        human_message = HumanMessage(content=user_input)
        messages.append(human_message)

        # Display user message
        with st.chat_message("user"):
            st.write(user_input)

        # Generate and display AI response
        with st.chat_message("assistant"):
            response_placeholder = st.empty()
            full_response = ""

            # Stream the response
            for chunk in llm.stream(messages):
                if chunk.content:
                    full_response += chunk.content
                    response_placeholder.markdown(full_response)

            # Add AI response to chat history
            messages.append(AIMessage(content=full_response))

    # Add button to clear chat history
    if st.sidebar.button("Clear Conversation"):
        system_message = messages[0]  # Keep the system message
        st.session_state.messages = [system_message]
        st.experimental_rerun()

if __name__ == "__main__":
    main()
