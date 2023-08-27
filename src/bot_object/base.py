from __future__ import annotations
from abc import ABC, abstractmethod

import streamlit as st


class BaseModel:
    def __init__(self, model_name: str):
        self.model_name = model_name

    @abstractmethod
    def generate_response(self):
        pass

    @abstractmethod
    def generate_option(self):
        pass

    @abstractmethod
    def update_message_state(self):
        pass