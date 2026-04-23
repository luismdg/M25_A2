# ==== PRESENTACION ====
from persistencia import ejecutar_prompt


def handle_prompt(prompt):
    """
    Flujo completo: Presentación → Persistencia
    """
    return ejecutar_prompt(prompt)


def handle_presentacion(prompt):
    """
    Solo devuelve el prompt (simula entrada del usuario)
    """
    return {
        "input_usuario": prompt,
        "mensaje": "Prompt recibido en capa de presentación (sin procesar)"
    }