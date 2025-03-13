
from typing import List, Optional
from dataclasses import dataclass, field
from langchain_anthropic import ChatAnthropic
from langchain.agents import AgentExecutor



class ChatService:
    def __init__(self):
        self._agent: Optional[AgentExecutor] = None
        self._messages: List[dict] = []

    def initialize_agent(self):
        from agent.agent_logic import create_portal_agent
        if not self._agent:
            self._agent = create_portal_agent()
        return self._agent

    def process_message(self, student_id: str, user_message: str):
        if not self._agent:
            self.initialize_agent()

        context_prompt = f"Student id: {student_id}. {user_message}"

        try:
            # Let the agent handle its own memory management
            response = self._agent.run(context_prompt)
            return response

        except Exception as e:
            raise Exception(f"Error processing message: {str(e)}")
