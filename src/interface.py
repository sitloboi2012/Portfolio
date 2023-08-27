from __future__ import annotations

import os
import streamlit as st

from bot_object.llama2 import Llama2Model
from bot_object.gpt import GPT_Model

MODEL_LIST = {
    "Llama 2 🦙": Llama2Model,
    "GPT-3.5-Turbo-16k 🤖": GPT_Model,
    "GPT4All Wizard 1.1 🔥": None
}

os.environ["REPLICATE_API_TOKEN"] = "r8_AOdyXko1qgGpcM6urUaWG1iL9ohZUYD0jF6Bx"
os.environ["OPENAI_API_KEY"] = "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"

def check_state():
    if "messages" not in st.session_state.keys():
        st.session_state.messages = [
            {"role": "assistant", "content": "How may I assist you today?"}
        ]

def clear_chat_history():
        st.session_state.messages = [
            {"role": "assistant", "content": "How may I assist you today?"}
        ]


def main() -> None:
    st.set_page_config(page_title="Multi Chatbot Project 🦙💬")

    st.sidebar.title("Welcome to UniverseBot")
    bot_type= st.sidebar.selectbox(
        "Choose your bot:",
        [
            "Choose bot at here",
            "Llama 2 🦙",
            "GPT-3.5-Turbo-16k 🤖",
            "GPT4All Wizard 1.1 🔥",
        ],
    )

    if bot_type in ["Llama 2 🦙", "GPT-3.5-Turbo-16k 🤖", "GPT4All Wizard 1.1 🔥"]:
        model = MODEL_LIST[bot_type](bot_type)
        model.generate_option()
        model.init_model()
        model.__repr__()
        st.sidebar.button('Clear Chat History', on_click=clear_chat_history)
    else:
        st.title("UniverseBot 🦙🤖🔥")
        st.write(
            "This is a page where you can find a collection of different Generative AI model"
        )
        st.info("How To Use")
        st.markdown(
            """
                    1. Choose the type of the bot
                    2. Choose the range of parameter you want to use
                    3. Start using it
                    """
        )

    if bot_type in ["Llama 2 🦙", "GPT-3.5-Turbo-16k 🤖", "GPT4All Wizard 1.1 🔥"]:
        if "messages" not in st.session_state.keys():
            st.session_state.messages = [
                {"role": "assistant", "content": "How may I assist you today?"}
            ]

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])

        if prompt := st.chat_input():
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.write(prompt)

        if st.session_state.messages[-1]["role"] != "assistant":
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = model.generate_response(
                        prompt, st.session_state.messages
                    )
                    placeholder = st.empty()
                    full_response = ""
                    for item in response:
                        full_response += item
                        placeholder.markdown(full_response)
                    placeholder.markdown(full_response)
            message = {"role": "assistant", "content": full_response}
            st.session_state.messages.append(message)


if __name__ == "__main__":
    main()
