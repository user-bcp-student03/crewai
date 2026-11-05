"""Agente inicial del taller. Mejora sus instrucciones sin cambiar su contrato."""
from crewai import Agent, Task
from crew.llm_config import llm

KEY = 'architect'
LABEL = 'Arquitecto'
SPEC_FILE = 'user_story.md'
EXTRACT_CODE = False

INSTRUCTIONS = ("Como arquitecto, diseña la solución de la feature siguiendo estos pasos:\n"
                "1. Lee el Issue y las interfaces existentes antes de proponer nada.\n"
                "2. Define los componentes y sus límites.\n"
                "3. Define el contrato de API: entradas, respuestas y errores.\n"
                "4. Escribe el recorrido de una petición y un ejemplo de petición y respuesta.\n"
                "5. Enumera criterios verificables alineados con los criterios de aceptación.\n"
                "6. Señala los supuestos pendientes y las decisiones que necesitan Datos, Backend y Frontend.\n"
                "Entrega el resultado como user_story.md.")
agent = Agent(role='Arquitecto de software', goal=("Definir la solución técnica de la feature. Define componentes, límites y contrato de API: "
                    "entradas, respuestas y errores, alineados con los criterios de aceptación."),
              backstory=("Eres un arquitecto de software senior con amplia experiencia en arquitectura "
                         "hexagonal y diseño de APIs. Lees el Issue y las interfaces existentes, "
                         "describes el recorrido de una petición con ejemplos de petición y respuesta, "
                         "señalas supuestos pendientes y dejas decisiones claras para Datos, "
                         "Backend y Frontend."), llm=llm,
              verbose=True, allow_delegation=False)


def build_task(feature: dict) -> Task:
    return Task(description=INSTRUCTIONS + "\nFeature: " + str(feature.get("title", ""))
                + "\n" + str(feature.get("description", ""))
                + "\n" + str(feature.get("acceptance_criteria", [])),
                expected_output='Una historia de usuario.', agent=agent)
