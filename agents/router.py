import os
import re
import sys
import httpx
from pathlib import Path

from tools.app_tool import AppTool
from tools.file_tool import FileTool
from tools.cmd_tool import CMDTool
from tools.search_tool import WebSearchTool
from tools.memory_tool import MemoryTool
from tools.code_tool import CodeTool

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL      = "qwen2.5:7b"


class Router:
    def __init__(self, system_prompt: str = None):
        self.system_prompt = system_prompt or (
            "You are Nano, a helpful AI desktop assistant. "
            "Reply in English only under 3 sentences. "
            "Address the user as Anike."
        )
        self.app_tool    = AppTool()
        self.file_tool   = FileTool()
        self.cmd_tool    = CMDTool()
        self.search_tool = WebSearchTool()
        self.memory_tool = MemoryTool()
        self.code_tool   = CodeTool()

    def process(self, text: str, history: list = None) -> tuple[str, str]:
        """
        1. Detect & execute matching tool from tools/
        2. Build prompt for LLM including tool result (if any)
        3. Call LLM for concise response
        4. Return (response_text, action_text)
        """
        tool_result = self._execute_tool(text)

        messages = [{"role": "system", "content": self.system_prompt}]
        if history:
            for item in history[-8:]:
                if isinstance(item, dict) and "role" in item and "content" in item:
                    messages.append({"role": item["role"], "content": item["content"]})

        user_content = text
        if tool_result:
            user_content = f"{text}\n\n[Tool execution result: {tool_result}]"

        messages.append({"role": "user", "content": user_content})

        response = self._call_llm(messages)
        return response, (tool_result or "")

    def _execute_tool(self, text: str) -> str:
        tl = text.lower().strip()

        # 1. Memory tool (remember, recall, forget)
        if any(w in tl for w in ["remember", "note that", "keep in mind", "don't forget",
                                "what do you know", "what do you remember", "recall",
                                "forget everything", "clear memory"]):
            res = self.memory_tool.run(text)
            if res:
                return res

        # 2. File tool (create folder, create file, read file, open folder)
        if any(w in tl for w in ["create folder", "make folder", "new folder", "mkdir",
                                "create file", "new file", "make file",
                                "open folder", "open file", "open desktop", "open downloads",
                                "open documents", "read file", "show file", "contents of"]):
            res = self.file_tool.run(text)
            if res:
                return res

        # 3. App tool (open, launch, start, close, kill app)
        if any(w in tl for w in ["open ", "launch ", "start ", "close ", "kill ", "quit "]):
            res = self.app_tool.run(text)
            if res:
                return res

        # 4. Search tool
        if any(w in tl for w in ["search for", "look up", "find info", "latest news on", "google "]):
            res = self.search_tool.run(text)
            if res:
                return res

        # 5. Code tool
        if any(w in tl for w in ["write code", "write a python", "write python", "build a website",
                                "create a python script", "make a python script"]):
            res = self.code_tool.run(text)
            if res:
                return res

        # 6. Command tool (pip, git, ipconfig, dir, run script, system info, tasklist, raw cmd)
        res = self.cmd_tool.run(text)
        if res:
            return res

        return ""

    def _call_llm(self, messages: list) -> str:
        try:
            resp = httpx.post(
                OLLAMA_URL,
                json={
                    "model": MODEL,
                    "messages": messages,
                    "stream": False,
                    "options": {"temperature": 0.7, "num_predict": 200},
                },
                timeout=45.0,
            )
            data = resp.json()
            if "message" in data and "content" in data["message"]:
                return data["message"]["content"].strip()
            elif "response" in data:
                return data["response"].strip()
            return "Command executed successfully."
        except Exception as e:
            return f"Action finished. (LLM error: {e})"