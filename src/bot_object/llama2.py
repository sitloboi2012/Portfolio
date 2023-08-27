from __future__ import annotations

import streamlit as st
import replicate

from .base import BaseModel


class Llama2Model(BaseModel):
    def __init__(self, model_name: str):
        super().__init__(model_name)
        self.top_p: float = None
        self.model_size: str = None
        self.temperature: float = None
        self.max_length: int = None
        self.string_dialogue: str = """You are a helpful assistant. You do not respond as 'User' or pretend to be 'User'. You only respond once as 'Assistant'."""
    
    def __repr__(self):
        st.header("Llama 2 Generative Model 🦙")
        st.markdown(
            "This is the updated version of Llama original model created by Meta. For more information about the model, please access to this [link](https://ai.meta.com/llama/)"
        )
    
    def init_model(self):
        if self.model_size == "7B":
            self.model = "a16z-infra/llama7b-v2-chat:4f0a4744c7295c024a1de15e1a63c880d3da035fa1f49bfd344fe076074c8eea"
        elif self.model_size == "13B":
            self.model = "a16z-infra/llama13b-v2-chat:df7690f1994d94e96ad9d568eac121aecf50684a0b0963b25a41cc40061269e5"
        else:
            self.model = "replicate/llama70b-v2-chat:e951f18578850b652510200860fc4ea62b3b16fac280f83ff32282f87bbd2e48"

    def generate_option(self):
        self.model_size = st.sidebar.selectbox(
            "Choose the model size:", ["7B", "13B", "70B"], index = 0
        )
        self.temperature = st.sidebar.slider(
            "Choose the temperature:", min_value=0.01, max_value=5.0, value=0.1, step=0.01
        )
        self.top_p = st.sidebar.slider(
            "Choose the top_p value:", min_value=0.01, max_value=1.0, value=0.9, step=0.01
        )
        self.max_length = st.sidebar.slider(
            "Choose the max_length:", min_value=64, max_value=4096, value=1036, step=8
        )
    
    def generate_response(self, prompt_input: str, session_state_messages):
        for dict_message in session_state_messages:
            if dict_message["role"] == "user":
                self.string_dialogue += "User: " + dict_message["content"] + "\n\n"
            else:
                self.string_dialogue += "Assistant: " + dict_message["content"] + "\n\n"

        response = replicate.run(
            self.model,
            input={
                "prompt": f"{self.string_dialogue} {prompt_input} Assistant: ",
                "temperature": self.temperature,
                "top_p": self.top_p,
                "max_length": self.max_length,
                "repetition_penalty": 1,
            },
        )
        
        return response
    
    def update_message_state(self):
        return super().update_message_state()