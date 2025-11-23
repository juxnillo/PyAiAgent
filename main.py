from dotenv import load_dotenv

load_dotenv()

from typing import List
from langchain_core.messages import HumanMessage, BaseMessage
from agent import run_agent

# Formateo de mensajes para el inicio del programa
if __name__ == "__main__":
    print("=" * 60)
    print("DataGen Agent - Generador de Datos Simple ")
    print("=" * 60)
    print("Genera datos simples de usuarios")
    print()
    print("Ejemplos:")
    print("   - Genera usuarios con nombres, Juan, Maria, Pedro y guardalos en un user.json")
    print("   - Crea usuarios con apellidos Garcia, Lopez, Martinez")
    print("   - Haz usuarios con 25 o 30 años con company.com en emails")
    print()
    print("Comandos: 'quit' o 'exit' para finalizar")
    print("=" * 60)


    history: List[BaseMessage] = []
    # bucle principal del programa donde pide al usuario una entrada
    while True:
        user_input = input("Usuario: ").strip()

        if user_input.lower() in ['quit', 'exit', 'q', ""]:
            print("Adios!")
            break

        print("Agente: ", end="", flush=True)
        response = run_agent(user_input, history)
        print(response.content)
        print()

        history += [HumanMessage(content=user_input), response]
