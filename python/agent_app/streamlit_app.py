import streamlit as st
from agent.agent_logic import create_portal_agent
def main():
    st.title("Student Portal Chatbot")

    # For demo purposes, the username is input by the user.
    student_id = st.sidebar.text_input("Enter your student ID", value="1")

    # Initialize chat history in session state if it doesn't exist
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Initialize the agent if it doesn't exist
    if "agent" not in st.session_state:
        st.session_state.agent = create_portal_agent()

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

            # Create agent-ready prompt with context
            context_prompt = f"Student id: {student_id}. {prompt}"

            # Get response from agent
            try:
                # First, add the message to agent memory
                st.session_state.agent.memory.chat_memory.add_user_message(context_prompt)

                # Then run the agent
                with st.chat_message("assistant"):
                    with st.spinner("Thinking..."):
                        response = st.session_state.agent.run(context_prompt)
                    st.write(response)

                # Add response to display history and agent memory
                st.session_state.messages.append({"role": "assistant", "content": response})
                st.session_state.agent.memory.chat_memory.add_ai_message(response)

            except Exception as e:
                error_msg = f"Error: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": "I'm sorry, I encountered an error. Please try again."})

if __name__ == "__main__":
    main()
