from langchain_groq import ChatGroq
from langchain.agents import create_agent
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from typing import List
from tools import write_json, read_json, generate_sample_users

TOOLS = [write_json, read_json, generate_sample_users]

llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.7)

SYSTEM_MESSAGE = ("Hola, soy un asistente virtual diseñado para ayudarte con tus tareas. ¿En qué puedo ayudarte hoy?")

agent = create_agent(llm, TOOLS, system_prompt=SYSTEM_MESSAGE)

def run_agent(user_input: str, history: List[BaseMessage]) -> AIMessage:
    try:
        result = agent.invoke({"messages": history + [HumanMessage(content=user_input)]}, # type: ignore
        config={"recursion_limit": 50})

        return result["messages"][-1]
    except Exception as e:
        return AIMessage(content=f"Error: {str(e)}")
