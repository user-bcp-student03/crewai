"""Agente inicial del taller. Mejora sus instrucciones sin cambiar su contrato."""
from crewai import Agent, Task
from crew.llm_config import llm

KEY = 'frontend'
LABEL = 'Desarrollador frontend'
SPEC_FILE = 'frontend_spec.md'
EXTRACT_CODE = True

INSTRUCTIONS = (
    "Parte del contrato de API y del recorrido del usuario para crear una tarea "
    "con título. Define el campo, su validación visible, las acciones y los "
    "estados de pantalla; envía la tarea a la API aprobada y permite usar el "
    "formulario con teclado."
)
agent = Agent(role='Desarrollador frontend',
              goal="Crear una tarea con título desde una interfaz Angular accesible.",
              backstory="Eres responsable del formulario de creación de tareas y su integración con la API aprobada.",
              llm=llm, verbose=True, allow_delegation=False)


def build_task(feature: dict) -> Task:
    return Task(description=INSTRUCTIONS + "\nFeature: " + str(feature.get("title", ""))
                + "\n" + str(feature.get("description", ""))
                + "\n" + str(feature.get("acceptance_criteria", [])),
                expected_output=(
                    'frontend_spec.md que liste el campo título, su validación visible, las '
                    'acciones y los estados de pantalla para crear una tarea, basándose en el '
                    'contrato de API y el recorrido del usuario. Incluye código Angular en '
                    'bloques markdown, uno por archivo, con la primera línea // nombre.component.ts, '
                    '// nombre.component.html, // nombre.component.css o // nombre.service.ts; '
                    'implementa consumo de API, estados de carga y error, y accesibilidad por teclado.'
                ), agent=agent)
