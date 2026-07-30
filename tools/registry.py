"""
Nano AI v2
Tool Registry
"""

from typing import Callable


class ToolRegistry:

    def __init__(self):

        self.tools = {}

    # -----------------------------

    def register(self, name: str, func: Callable):

        self.tools[name.lower()] = func

    # -----------------------------

    def exists(self, name: str):

        return name.lower() in self.tools

    # -----------------------------

    def execute(self, name: str, *args, **kwargs):

        if not self.exists(name):
            return f"Tool '{name}' not found."

        return self.tools[name.lower()](*args, **kwargs)

    # -----------------------------

    def list_tools(self):

        return sorted(self.tools.keys())