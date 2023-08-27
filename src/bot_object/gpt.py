from __future__ import annotations

import os
import streamlit as st

from langchain import OpenAI
from langchain.memory import ConversationBufferMemory
from langchain.agents import initialize_agent
from langchain.agents import Tool
from langchain.agents import AgentType
from langchain.utilities import SerpAPIWrapper

from .base import BaseModel

os.environ["OPENAI_API_KEY"] = "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"
os.environ[
    "SERPAPI_API_KEY"
] = "024304badf8595585d3f9be3bfebe91a2a366f77b53ef91c704885334e4187d7"


class GPT_Model(BaseModel):
    def __init__(self, model_name: str):
        super().__init__(model_name)
        self.model_name = model_name
        self.temperature: float = None
        self.model = None
        self.memory = None
        self.agent = None
        self.chat_history = []
        self.string_dialogue: str = """You are a helpful assistant. You do not respond as 'User' or pretend to be 'User'. You only respond once as 'Assistant'."""

    def __repr__(self) -> str:
        st.header("GPT-3.5-Turbo-16k Generative Model 🤖")
        st.markdown(
            "This model is inherit from ChatGPT OpenAI Model. For more information, please access to this [link](https://openai.com/)"
        )

    def generate_response(self, prompt_input: str, session_state_messages):
        for dict_message in session_state_messages:
            if dict_message["role"] == "user":
                self.string_dialogue += "User: " + dict_message["content"] + "\n\n"
            else:
                self.string_dialogue += "Assistant: " + dict_message["content"] + "\n\n"

        response = self.agent.run(input = prompt_input)
                
        return response
        
    def generate_option(self):
        self.temperature = st.sidebar.slider(
            "Choose the temperature:",
            min_value=0.01,
            max_value=5.0,
            value=0.1,
            step=0.01,
        )

    def init_model(self):
        self.search = SerpAPIWrapper()
        self.tools = [
            Tool(
                name="Current Search",
                func=self.search.run,
                description="useful for when you need to answer questions about current events or the current state of the world",
            )
        ]
        self.model = OpenAI(
            model_name='gpt-3.5-turbo-16k',
            openai_api_key=os.environ["OPENAI_API_KEY"], temperature=self.temperature
        )
        
        self.memory = ConversationBufferMemory(memory_key="chat_history")

        self.agent = initialize_agent(
            self.tools,
            self.model,
            agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
            verbose=True, memory=self.memory,
            handle_parsing_errors=True,
        )
        
        st.session_state.memory = self.agent.memory.buffer
