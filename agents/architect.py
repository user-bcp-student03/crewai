"""Agente inicial del taller. Mejora sus instrucciones sin cambiar su contrato."""
from crewai import Agent, Task
from crew.llm_config import llm

KEY = 'architect'
LABEL = 'Arquitecto'
SPEC_FILE = 'user_story.md'
EXTRACT_CODE = False

INSTRUCTIONS = "Realiza la tarea de tu rol."
agent = Agent(role='Arquitecto', goal=("Definir la solución técnica de la feature. Define componentes, límites y contrato de API: "
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
