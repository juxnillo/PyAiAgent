import json
import random
from langchain_core.tools import tool
from datetime import datetime, timedelta
from typing import List

#------Tools-------

# Tool principal para escribir un diccionario en un archivo JSON
@tool
def write_json(filepath: str, data: dict) -> str:
    """Escribe un diccionario en un archivo JSON"""
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        return f"Error al escribir el archivo JSON: {str(e)}"
    return f"Archivo JSON escrito correctamente en {filepath}"

# Tool principal para leer un archivo JSON y devolver su contenido como una cadena
@tool
def read_json(filepath: str) -> str:
    """Lee un archivo JSON y devuelve su contenido como una cadena"""
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

# Tool para generar usuarios aleatorios
@tool
def generate_sample_users(
    first_names: List[str],
    last_names: List[str],
    domains: List[str],
    min_age: int,
    max_age: int,
) -> dict:
    """ Genera una lista de usuarios aleatorios.

    Args:
        first_names (List[str]): Lista de nombres de pila.
        last_names (List[str]): Lista de apellidos.
        domains (List[str]): Lista de dominios de correo electrónico.
        min_age (int): Edad mínima.
        max_age (int): Edad máxima.
    Returns:
        dict: Lista de usuarios aleatorios.
    """
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
