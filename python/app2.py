import os
import psycopg2
import streamlit as st
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from dotenv import load_dotenv
import pg8000

# Load environment variables
load_dotenv()

# Configure Streamlit page
st.set_page_config(
    page_title="Claude Chatbot",
    page_icon="🤖",
    layout="wide"
)

def get_student_gpa(student_id):

    """
    Connects to a PostgreSQL database using pg8000 and retrieves the GPA for the given student_id.
    Assumes a table 'students' with columns 'student_id' and 'gpa'.
    Connection details are loaded from environment variables.
    """
    print(student_id)
    try:
        conn = pg8000.connect(
            host=os.getenv('PGHOST'),
            user=os.getenv('PGUSER'),
            password=os.getenv("PGPASSWORD"),
            port=int(os.getenv("PGPORT", "5432")),  # Pass as string with default
            database=os.getenv("PGDATABASE", "mydb")
        )
        cursor = conn.cursor()
        cursor.execute("SELECT gpa FROM students WHERE id = %s", (student_id,))
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else None
    except Exception as e:
        st.error(f"Database error: {e}")
        return None

def get_student_name(student_id):

    """
    Connects to a PostgreSQL database using pg8000 and retrieves the GPA for the given student_id.
    Assumes a table 'students' with columns 'student_id' and 'gpa'.
    Connection details are loaded from environment variables.
    """
    print(student_id)
    try:
        conn = pg8000.connect(
            host=os.getenv('PGHOST'),
            user=os.getenv('PGUSER'),
            password=os.getenv("PGPASSWORD"),
            port=int(os.getenv("PGPORT", "5432")),  # Pass as string with default
            database=os.getenv("PGDATABASE", "mydb")
        )
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM students WHERE id = %s", (student_id,))
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else None
    except Exception as e:
        st.error(f"Database error: {e}")
        return None

def get_or_create_chat_history():
    """
    Initialize or get existing chat history.
    The system prompt instructs the assistant about the student database.
    """
    if "messages" not in st.session_state:
        system_prompt = (
            "You are Claude, an assistant for the student portal. "
            "You have access to a student database containing student IDs and their GPAs. "
            "Whenever a student asks for their GPA, please use the database for an accurate answer. "
            "If a student has not provided their student ID, ask them to provide it in the format: student_id: <your id>."
        )
        st.session_state.messages = [SystemMessage(content=system_prompt)]
    return st.session_state.messages

def get_llm():
    """
    Initialize the Claude model.
    """
    return ChatAnthropic(
        anthropic_api_key=os.getenv("ANTHROPIC_API_KEY"),
        model="claude-3-haiku-20240307",
        temperature=0.7,
        max_tokens=1024,
        streaming=True
    )

def main():
    st.title("🤖 Claude Chatbot")
    st.subheader("LLM-based Student Portal")

    # Retrieve or create chat history
    messages = get_or_create_chat_history()

    # Display chat history (skip system prompt)
    for msg in messages:
        if not isinstance(msg, SystemMessage):
            if isinstance(msg, HumanMessage):
                with st.chat_message("user"):
                    st.write(msg.content)
            else:  # AIMessage
                with st.chat_message("assistant"):
                    st.write(msg.content)

    # Get user input
    user_input = st.chat_input("Ask Claude something...")

    if user_input:
        # Record the student ID if provided
        if user_input.lower().startswith("student_id:"):
            student_id = user_input.split(":", 1)[1].strip()
            st.session_state.student_id = student_id
            response_text = f"Student ID '{student_id}' recorded. You can now ask for your GPA & name."
            messages.append(HumanMessage(content=user_input))
            messages.append(AIMessage(content=response_text))
            with st.chat_message("assistant"):
                st.write(response_text)
        # Intercept GPA queries and query the database directly
        elif "gpa" in user_input.lower():
            messages.append(HumanMessage(content=user_input))
            if "student_id" not in st.session_state:
                response_text = "Please provide your student ID first in the format: student_id: <your id>"
                messages.append(AIMessage(content=response_text))
                with st.chat_message("assistant"):
                    st.write(response_text)
            else:
                student_id = st.session_state.student_id
                gpa = get_student_gpa(student_id)
                if gpa is not None:
                    response_text = f"Your GPA is: {gpa}"
                else:
                    response_text = "Student ID not found in our records."
                messages.append(AIMessage(content=response_text))
                with st.chat_message("assistant"):
                    st.write(response_text)
        # For all other queries, use the LLM normally.
        elif "name" in user_input.lower():
            messages.append(HumanMessage(content=user_input))
            if "student_id" not in st.session_state:
                response_text = "Please provide your student ID first in the format: student_id: <your id>"
                messages.append(AIMessage(content=response_text))
                with st.chat_message("assistant"):
                    st.write(response_text)
            else:
                student_id = st.session_state.student_id
                name = get_student_name(student_id)
                if name is not None:
                    response_text = f"Your name is: {name}"
                else:
                    response_text = "Student ID not found in our records."
                messages.append(AIMessage(content=response_text))
                with st.chat_message("assistant"):
                    st.write(response_text)
        else:
            messages.append(HumanMessage(content=user_input))
            llm = get_llm()
            with st.chat_message("assistant"):
                response_placeholder = st.empty()
                full_response = ""
                for chunk in llm.stream(messages):
                    if chunk.content:
                        full_response += chunk.content
                        response_placeholder.markdown(full_response)
                messages.append(AIMessage(content=full_response))

    # Button to clear the conversation and student ID
    if st.sidebar.button("Clear Conversation"):
        st.session_state.messages = [messages[0]]  # Keep the system prompt
        st.session_state.pop("student_id", None)
        st.experimental_rerun()

if __name__ == "__main__":
    main()
