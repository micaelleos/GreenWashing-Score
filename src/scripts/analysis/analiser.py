import sys
import os
from pydantic import BaseModel, Field
from typing import Literal, List
from langchain_core.tools import tool
from langgraph.graph import MessagesState
from typing_extensions import Annotated, TypedDict
import uuid
from src.scripts.analysis.prompt import *
from src.scripts.chat.document_loader import custom_retriver, retrieve_sections, retrieve_sections_page, tools
from langchain_openai import ChatOpenAI

from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langchain_community.callbacks import get_openai_callback




PERSIST_DIR="../data"
OPENAI_API_KEY = os.environ['OPEN_API_KEY']
# Classe para representar um critério individual
class Avaliacao(TypedDict):
    nome_criterio: Annotated[str, "Nome do critério que está sendo avaliado"]
    nota: Annotated[int, "Nota atribuída ao critério (deve estar entre 0 e 5)"]  # Nota atribuída ao critério
    justificativa: Annotated[str, "Justificativa da nota"]  # Justificativa da nota
    recomendacao: Annotated[str, "Recomendação para o trecho"]  # Recomendação para o critério

# Classe principal que representa o estado com uma lista de critérios
class Criterios(TypedDict):
    criterios: Annotated[list[Avaliacao], "Uma lista de critérios com suas avaliações"]

# Inherit 'messages' key from MessagesState, which is a list of chat messages
class AgentState(MessagesState):
    # Final structured response from the agent
    final_response: Criterios


class GreenAgent():

    def __init__(self):
        self.cost = []
        self.llm = ChatOpenAI(model_name="gpt-4o", temperature=0.2,top_p=0.3,openai_api_key=OPENAI_API_KEY) #ChatAnthropic(model='claude-3-opus-20240229',api_key=CLAUDE_API) 
        self.tools = tools
        self.model_with_tools = self.llm.bind_tools(self.tools)
        self.model_with_structured_output = self.llm.with_structured_output(Criterios)
        self.memory = MemorySaver()

        # Define a new graph
        self.workflow = StateGraph(AgentState)

        # Define the two nodes we will cycle between
        self.workflow.add_node("agent", self.call_model)
        self.workflow.add_node("respond", self.respond)
        self.workflow.add_node("tools", ToolNode(self.tools))

        # Set the entrypoint as `agent`
        # This means that this node is the first one called
        self.workflow.set_entry_point("agent")

        # We now add a conditional edge
        self.workflow.add_conditional_edges(
            "agent",
            self.should_continue,
            {
                "continue": "tools",
                "respond": "respond",
            },
        )

        self.workflow.add_edge("tools", "agent")
        self.workflow.add_edge("respond", END)
        self.graph = self.workflow.compile(checkpointer=self.memory,debug=True)

    def call_model(self,state: AgentState):
        chain = prompt_agent | self.model_with_tools
        response = chain.invoke(input={"messages":state['messages']})
        # We return a list, because this will get added to the existing list
        return {"messages": [response]}


    # Define the function that responds to the user
    def respond(self,state: AgentState):
        # We call the model with structured output in order to return the same format to the user every time
        # state['messages'][-2] is the last ToolMessage in the convo, which we convert to a HumanMessage for the model to use
        # We could also pass the entire chat history, but this saves tokens since all we care to structure is the output of the tool
        chain = prompt_structure | self.model_with_structured_output
        response = chain.invoke(input={"messages":[HumanMessage(content=state["messages"][-2].content)]})
        # We return the final answer
        return {"final_response": response}


    # Define the function that determines whether to continue or not
    def should_continue(self,state: AgentState):
        messages = state["messages"]
        last_message = messages[-1]
        # If there is no function call, then we respond to the user
        if not last_message.tool_calls:
            return "respond"
        # Otherwise if there is, we continue
        else:
            return "continue"
        
    def analizer_page(self,initial_page:int,final_page:int):
        docs = retrieve_sections_page(initial_page,final_page)
        docs_analized = []
        docx={}
        for doc in docs:
            config = {"configurable": {"thread_id": uuid.uuid4()}}
            inputs={"messages":HumanMessage(doc.page_content)}
            with  get_openai_callback() as cb:
                answer = self.graph.invoke(input=inputs,config=config)
                docx['documents']=doc.page_content
                docx['id'] = doc.id
                docx['metadata'] = doc.metadata
                docx["analise"] = answer['final_response']
                docx["history"] = answer['messages']
                docs_analized.append(docx)
                docx={}
            self.cost.append(cb)
        print("finalizou")
        return docs_analized
    
    def analizer_full_document(self):
        docs = retrieve_sections()
        docs_analized = []
        for doc_analized in docs:
            config = {"configurable": {"thread_id": uuid.uuid4()}}
            inputs={"messages":HumanMessage(doc_analized['documents'])}
            answer = self.graph.invoke(input=inputs,config=config)
            doc_analized["analise"] = answer['final_response']
            doc_analized["history"] = answer['messages']
            docs_analized.append(doc_analized)
        return docs_analized

    def analizer(self,query:str):
        result = self.graph.invoke(input={"messages":HumanMessage(query)},config = {"configurable": {"thread_id": uuid.uuid4()}})
        return result['final_response']

if __name__ == "__main__":
    teste = GreenAgent()
    print(teste.graph.invoke(input={"messages":HumanMessage("o que você pode fazer?")},config = {"configurable": {"thread_id": "def234"}}))