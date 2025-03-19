import os
import streamlit as st
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from src.scripts.chat.tools import tools_esg_agent
from langchain_core.messages import AIMessage
from src.scripts.chat.prompt import prompt, saudacao

@st.cache_resource()
def memory():
    memory = MemorySaver() 
    return memory

class Bot():
    def __init__(self):
        self.OPENAI_API_KEY=os.environ["OPEN_API_KEY"]

        self.llm = ChatOpenAI(model="gpt-4o",api_key=self.OPENAI_API_KEY)
        self.memory = memory()
        self.tools = tools_esg_agent
        self.agent_executor = create_react_agent(self.llm, self.tools, checkpointer=self.memory, prompt=prompt)

        self.config = {"configurable": {"thread_id": "def234"}}

        self.agent_executor.invoke(input={"messages":[{"role":"assistant","content":saudacao}]},config=self.config)

    def chat(self,query:str):
        menssage = None
        for event in self.agent_executor.stream(
            {"messages": [{"role": "user", "content": query}]},
            stream_mode="values",
            config=self.config,
        ):
            #event["messages"][-1].pretty_print()
            if isinstance(event["messages"][-1], AIMessage):
                menssage = event["messages"][-1]
        return menssage.content