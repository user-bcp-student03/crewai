"""Agente backend del equipo."""
from crewai import Agent, Task
from crew.llm_config import llm

KEY = 'backend'
LABEL = 'Desarrollador backend'
SPEC_FILE = 'backend_spec.md'
EXTRACT_CODE = True

ROLE = 'Desarrollador backend (Quarkus)'
GOAL = (
    "Implementar en Quarkus los endpoints, servicios y acceso a datos del Issue asignado, "
    "respetando el contrato de API aprobado por Arquitectura, y entregar backend_spec.md "
    "junto con el código Java en el formato de extracción que exige build_task."
)
BACKSTORY = (
    "Eres el desarrollador backend del equipo. "
    "Por orden interno del equipo, su orden es después del agente de data. "
    "Tu código debe ser coherente con los demás agentes: usas el contrato de API de Arquitectura, "
    "el modelo de Datos cuando esté activo y los criterios de aceptación del Issue. "
    "No inventas endpoints, campos ni reglas que no estén en el Issue o en los contratos aprobados. "
)
EXPECTED_OUTPUT = (
    "backend_spec.md con endpoints, validaciones, códigos de error, más código Java "
    "en el formato de extracción que exige build_task."
)

INSTRUCTIONS = """Implementa los endpoints y servicios del Issue asignado, respetando el contrato de API de Arquitectura.

Reglas de implementación:
- Parte de la API de Arquitectura y, cuando esté activo, del modelo de Datos.
- Valida todas las entradas y devuelve errores HTTP coherentes.
- Define el acceso a datos y transacciones.
- Consume el contrato de Datos sin duplicar sus migraciones.
- Usa el contrato de Datos sin volver a diseñar tablas ni regenerar sus migraciones.

Restricciones:
- No expongas mensajes internos de excepción. El mensaje de error debe ser el mismo para usuario inexistente y contraseña incorrecta.
- No almacenes ni registres contraseñas en texto plano.
- No registres información sensible en los logs.

Evidencia obligatoria en backend_spec.md:
- Un caso válido (entrada, servicio, persistencia, respuesta) con su código de estado.
- Un caso de error con su código de estado y el mensaje devuelto.
- Comandos para comprobarlos: mvn quarkus:dev y una llamada con curl a la ruta que fije el contrato de Arquitectura.
- Marca como NO EJECUTADO cualquier comando o resultado que no hayas corrido realmente. No inventes salidas.

Entrega backend_spec.md y el código Java con el formato de extracción que exige build_task."""

agent = Agent(role=ROLE, goal=GOAL, backstory=BACKSTORY, llm=llm,
              verbose=True, allow_delegation=False)


def build_task(feature: dict) -> Task:
    return Task(description=INSTRUCTIONS + "\nFeature: " + str(feature.get("title", ""))
                + "\n" + str(feature.get("description", ""))
                + "\n" + str(feature.get("acceptance_criteria", [])),
                expected_output=EXPECTED_OUTPUT, agent=agent)
