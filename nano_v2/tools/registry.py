"""
Tool Registry
Registers and executes Nano tools.
"""


class ToolRegistry:
    def __init__(self):
        self.tools = {}

    def register(self, name: str, tool):
        """Register a tool."""
        self.tools[name] = tool

    def unregister(self, name: str):
        """Remove a tool."""
        if name in self.tools:
            del self.tools[name]

    def get(self, name: str):
        """Return a tool."""
        return self.tools.get(name)

    def execute(self, name: str, *args, **kwargs):
        """Execute a registered tool."""
        tool = self.get(name)

        if tool is None:
            raise ValueError(f"Tool '{name}' not found")

        if callable(tool):
            return tool(*args, **kwargs)

        if hasattr(tool, "run"):
            return tool.run(*args, **kwargs)

        raise TypeError(f"Tool '{name}' is not executable")

    def list_tools(self):
        """Return all registered tools."""
        return sorted(self.tools.keys())