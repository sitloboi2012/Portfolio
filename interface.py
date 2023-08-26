from __future__ import annotations

import os
import streamlit as st

from bot_object.llama2 import Llama_Bot

def check_validate_bot(bot_type: str):
    if bot_type in ["Llama 2 🦙", "GPT4All Wizard 1.1 🔥"]:
        return bot_type, None
    
    openai_api_key = st.text_input("Enter your OpenAI API Key: ")
    
    if (openai_api_key != "") and (openai_api_key.startswith("sk-")):
        st.success("Accepted OpenAI API Key")
        return bot_type, openai_api_key

def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]


def main() -> None:
    st.set_page_config(page_title = "Multi Chatbot Project 🦙💬")
    
    st.sidebar.title("Welcome to UniverseBot")
    bot_type, api_key = check_validate_bot(st.sidebar.selectbox("Choose your bot:", ["Llama 2 🦙", "GPT-3.5-Turbo-16k 🤖", "GPT4All Wizard 1.1 🔥"]))
    temperature = st.sidebar.slider("Choose the temperature:", min_value=0.01, max_value=5.0, value=0.1, step=0.01)
    top_p = st.sidebar.slider("Choose the top_p value:", min_value=0.01, max_value=1.0, value=0.9, step=0.01)
    max_length = st.sidebar.slider("Choose the max_length:", min_value=64, max_value=4096, value=512, step=8)
    st.sidebar.button('Clear Chat History', on_click=clear_chat_history)
    
    
    if bot_type == "Llama 2 🦙":
        os.environ['REPLICATE_API_TOKEN'] = "r8_AOdyXko1qgGpcM6urUaWG1iL9ohZUYD0jF6Bx"
        model_obj = Llama_Bot("7B", temperature, top_p, max_length)
        model_obj.__repr__()
    elif bot_type == "GPT-3.5-Turbo-16k 🤖":
        os.environ["OPENAI_API_KEY"] = api_key
        

    
    if "messages" not in st.session_state.keys():
        st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]
    
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
                response = model_obj.generate_response(prompt, st.session_state.messages)
                placeholder = st.empty()
                full_response = ''
                for item in response:
                    full_response += item
                    placeholder.markdown(full_response)
                placeholder.markdown(full_response)
        message = {"role": "assistant", "content": full_response}
        st.session_state.messages.append(message)
        


if __name__ == "__main__":
    main()