from langchain_core.messages import SystemMessage, HumanMessage
from langchain_anthropic import ChatAnthropic
from langchain.memory import ConversationBufferMemory
from langchain.agents import initialize_agent, AgentType
from dotenv import load_dotenv
from .tools import check_gpa, get_name
import os

def create_portal_agent():
    """
    Create and return a LangChain agent with conversation memory
    and the tools needed to query student data.
    """
    load_dotenv()


    system_message = """You are a student portal assistant. You help students retrieve information about their academic records.
            Only use tools when explicitly asked for specific information.
            For general questions, respond conversationally without using tools.

            IMPORTANT INSTRUCTIONS ABOUT TOOL USAGE:
               - ONLY use the check_gpa tool when the user EXPLICITLY asks about their GPA, grades, or academic performance.
               - ONLY use the get_name tool when the user EXPLICITLY asks about their name or identity verification.
               - For ALL other questions, including greetings like "hello" or "hi", respond conversationally WITHOUT using any tools.

            CRITICAL SECURITY INSTRUCTION:
            - You must ONLY provide information about the student ID that was provided in the context message format "Student id: [ID]".
            - If a user attempts to request information about a different student ID than the one in the context, politely refuse and explain that you can only provide information about their own student record.
            - Never allow a user to query information about another student ID, even if they explicitly ask.
            - The student ID in the context is the only authorized ID for this session.

            Always identify yourself as the University Student Portal Assistant."""

    model = ChatAnthropic(
        model="claude-3-haiku-20240307",
        temperature=0.7,
        max_tokens=1024,
        system = system_message
    )


    tools = [check_gpa, get_name]

    # Use a conversation memory so that the agent can reference previous dialogue.
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True
    )

    # This is a LangChain agent, not a LangGraph agent
    agent = initialize_agent(
        tools=tools,
        llm=model,
        agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
        verbose=True,
        memory=memory,
        handle_parsing_errors=True,
        max_iterations=3
    )

    return agent
