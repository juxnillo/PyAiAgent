from typing import List
import json
import random
from datetime import datetime, timedelta
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent

from dotenv import load_dotenv

load_dotenv()


#------Tools-------
@tool
def write_json(filepath: str, data: dict) -> str:
    #Escribe un diccionario en un archivo JSON
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        return f"Error al escribir el archivo JSON: {str(e)}"
    return f"Archivo JSON escrito correctamente en {filepath}"


@tool
def read_json(filepath: str) -> str:
    #Lee un archivo JSON y devuelve su contenido como una cadena
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data =json.load(f)
        return json.dumps(data, indent=2)
    except FileNotFoundError:
        return f"Error:Archivo no encontrado: {filepath}"
    except json.JSONDecodeError as e:
        return f"Error: Archivo JSON no permitido: {str(e)}"
    except Exception as e:
        return f"Error: No se puedeleer el archivo JSON: {str(e)}"


@tool
def generate_sample_users(
    first_names: List[str],
    last_names: List[str],
    domains: List[str],
    min_age: int,
    max_age: int,
) -> dict:
    # Genera una lista de usuarios aleatorios.

    #Args:
    #    first_names (List[str]): Lista de nombres de pila.
    #    last_names (List[str]): Lista de apellidos.
    #    domains (List[str]): Lista de dominios de correo electrónico.
    #    min_age (int): Edad mínima.
    #    max_age (int): Edad máxima.
    #Returns:
    #    dict: Lista de usuarios aleatorios.
    if not first_names:
        return {"Error": "Lista de nombres no puede estar vacía"}
    if not last_names:
        return {"Error": "Lista de apellidos no puede estar vacía"}
    if not domains:
        return {"Error": "Lista de dominios de correo electrónico no puede estar vacía"}
    if max_age < min_age:
        return {"Error": f"Edad mínima {min_age} no puede ser mas grande que la edad maxima {max_age}"}
    if min_age < 0 or max_age < 0:
        return {"Error": "Edad no puede ser negativa"}

    users = []
    count = len(first_names)

    for i in range(count):
        first = first_names[i]
        last = last_names[i % len(last_names)]
        domain = domains[i % len(domains)]
        email = f"{first.lower()}.{last.lower()}@{domain}"

        user = {
            "id": i + 1,
            "first_name": first,
            "last_name": last,
            "email": email,
            "username": f"{first.lower()}{random.randint(100, 999)}",
            "age": random.randint(min_age, max_age),
            "registeredAt": (datetime.now() - timedelta(days=random.randint(1, 365))).isoformat()
        }
        users.append(user)

    return {"users": users, "count": len(users)}


TOOLS = [write_json, read_json, generate_sample_users]

llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.7)

SYSTEM_MESSAGE = ("Hola, soy un asistente virtual diseñado para ayudarte con tus tareas. ¿En qué puedo ayudarte hoy?")

agent = create_react_agent(llm, TOOLS, prompt=SYSTEM_MESSAGE)

def run_agent(user_input: str, history: List[BaseMessage]) -> AIMessage:
    try:
        result = agent.invoke({"messages": history + [HumanMessage(content=user_input)]}, config={"recursion_limit": 50})

        return result["messages"][-1]
    except Exception as e:
        return AIMessage(content=f"Error: {str(e)}")

if __name__ == "__main__":
    print("=" * 60)
    print("DataGen Agent - Sample Data Generator")
    print("=" * 60)
    print("Generate Sample User Data")
    print()
    print("Examples:")
    print("   - Generate users named John, jane, Mike and save to user.json")
    print("   - Create users with last names Smith, Jones")
    print("   - Make users aged 25-35 with company.com emails")
    print()
    print("Commands: 'quit' or 'exit' to end")
    print("=" * 60)


    history: List[BaseMessage] = []

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() in ['quit', 'exit', 'q', ""]:
            print("Goodbye!")
            break

        print("Agent: ", end="", flush=True)
        response = run_agent(user_input, history)
        print(response.content)
        print()

        history += [HumanMessage(content=user_input), response]
