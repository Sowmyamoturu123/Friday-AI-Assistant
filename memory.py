import json
import os


MEMORY_FILE = "memory.json"


def load_memory():
    """Load all saved memories from memory.json."""
    if not os.path.exists(MEMORY_FILE):
        return {}

    try:
        with open(
            MEMORY_FILE,
            "r",
            encoding="utf-8"
        ) as file:
            return json.load(file)

    except (json.JSONDecodeError, OSError):
        return {}


def save_memory(memory):
    """Save memories to memory.json."""
    with open(
        MEMORY_FILE,
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            memory,
            file,
            indent=4,
            ensure_ascii=False
        )


def remember(key, value):
    """Save or update a memory."""
    memory = load_memory()

    memory[key] = value

    save_memory(memory)

    return (
        f"I'll remember that "
        f"{key.replace('_', ' ')} is {value}."
    )


def recall(key):
    """Recall a specific memory."""
    memory = load_memory()

    # Exact key match
    if key in memory:
        return (
            f"{key.replace('_', ' ')} "
            f"is {memory[key]}."
        )

    # Flexible search through keys and values
    search_words = set(
        key.lower()
        .replace("_", " ")
        .split()
    )

    for stored_key, value in memory.items():

        stored_key_text = (
            stored_key
            .lower()
            .replace("_", " ")
        )

        stored_value_text = str(value).lower()

        stored_words = set(
            stored_key_text.split()
        )

        # Search in the key
        if search_words & stored_words:
            return (
                f"{stored_key.replace('_', ' ')} "
                f"is {value}."
            )

        # Search inside the stored value
        if key.lower() in stored_value_text:
            return (
                f"{stored_key.replace('_', ' ')} "
                f"is {value}."
            )

    return (
        f"I don't have anything stored "
        f"about {key}."
    )


def get_all_memories():
    """Return all stored memories."""
    memory = load_memory()

    if not memory:
        return (
            "I don't have any memories "
            "stored yet."
        )

    results = []

    for key, value in memory.items():
        results.append(
            f"{key.replace('_', ' ')}: {value}"
        )

    return "\n".join(results)