import json
import os

MEMORY_FILE = "memory.json"


def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return {}

    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        return {}


def save_memory(memory):
    with open(MEMORY_FILE, "w", encoding="utf-8") as file:
        json.dump(memory, file, indent=4)


def remember(key, value):
    memory = load_memory()
    memory[key] = value
    save_memory(memory)

    return f"I'll remember that {key} is {value}."


def recall(key):
    memory = load_memory()

    if key not in memory:
        return f"I don't have anything stored about {key}."

    return f"{key} is {memory[key]}."