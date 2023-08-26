from __future__ import annotations

import streamlit as st
import replicate


class Llama_Bot:
    def __init__(
        self, model_size: int, temperature: float, top_p: float, max_length: int
    ) -> None:
        self.temperature = temperature
        self.top_p = top_p
        self.max_length = max_length
        self.string_dialogue = """You are a helpful assistant. You do not respond as 'User' or pretend to be 'User'. You only respond once as 'Assistant'."""

        if model_size == "7B":
            self.model = "a16z-infra/llama7b-v2-chat:4f0a4744c7295c024a1de15e1a63c880d3da035fa1f49bfd344fe076074c8eea"
        elif model_size == "13B":
            self.model = "a16z-infra/llama13b-v2-chat:df7690f1994d94e96ad9d568eac121aecf50684a0b0963b25a41cc40061269e5"
        else:
            self.model = "replicate/llama70b-v2-chat:e951f18578850b652510200860fc4ea62b3b16fac280f83ff32282f87bbd2e48"

    def __repr__(self):
        st.header("Llama 2 Generative Model 🦙")
        st.markdown(
            "This is the updated version of Llama original model created by Meta. For more information about the model, please access to this [link](https://ai.meta.com/llama/)"
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