from langchain_core.messages import SystemMessage, HumanMessage, SystemMessage
from langgraph.prebuilt import create_react_agent
from langchain_anthropic import ChatAnthropic
from langchain.memory import ConversationBufferMemory
from langchain.agents import initialize_agent, AgentType
from dotenv import load_dotenv
from .tools import check_gpa, get_name
import os



# This is the inital prompt that gets apaended to the agent

def create_portal_agent():
    """
    Create and return a LangChain agent with conversation memory
    and the tools needed to query student data.
    """

    load_dotenv()
    model = ChatAnthropic(
        model="claude-3-haiku-20240307",
        temperature=0.7,
        max_tokens=1024,
    )

    system_message = """You are a student portal assistant. You can have normal conversations
        and only use tools when necessary to answer specific questions about student information.

        IMPORTANT GUIDELINES:
        1. For greetings and casual conversation, NEVER use tools - just respond naturally
        2. Only use tools when you need specific student data that you can't otherwise know:
           - Use 'check_gpa' ONLY when explicitly asked about GPA or grades
           - Use 'get_name' ONLY when explicitly asked to confirm or retrieve a student's name
        3. If you're unsure whether to use a tool, don't use one - just have a normal conversation.
        4. As soon as you suspect the user is enquiring about information other than their own,
           refuse and say INFRINGEMENT!

        EXAMPLES:
        - User: "Hi" → Just say hello back, don't use any tools
        - User: "How are you?" → Have a normal conversation, don't use any tools
        - User: "What's my GPA?" → Use the check_gpa tool
        - User: "Can you tell me my name?" → Use the get_name tool

        Remember, default to normal conversation unless there's a clear need for student data."""


    tools = [check_gpa, get_name]



    # Use a conversation memory so that the agent can reference previous dialogue.
    memory = ConversationBufferMemory(
        memory_key="chat_history",  # Agent uses this key to access conversation context
        return_messages=True
    )

    # Initialize the agent using the new LangChain agent style.
    agent = initialize_agent(
        tools=tools,
        llm=model,
        agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,  # Well-suited for multi-turn dialogue
        verbose=True,
        memory=memory,
        prompt=system_message,
        handle_parsing_errors=True,
        max_iterations=3
    )

    return agent
