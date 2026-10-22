"""Agente inicial del taller. Mejora sus instrucciones sin cambiar su contrato."""
from crewai import Agent, Task
from crew.llm_config import llm

KEY = 'backend'
LABEL = 'Desarrollador backend'
SPEC_FILE = 'backend_spec.md'
EXTRACT_CODE = True

INSTRUCTIONS = """Implementa únicamente el alcance backend de la feature y respeta el contrato de API, los criterios de aceptación y las decisiones aprobadas por Arquitectura. Antes de proponer cambios, revisa el código, la configuración y las pruebas existentes; conserva sus convenciones y evita rediseños o cambios secundarios.

Identifica el Definition of Done (DoD) aplicable en las instrucciones del workspace, la documentación del proyecto o el contexto aprobado del Issue. Cumple cada criterio aplicable además de los criterios de aceptación de la feature, y relaciona cada uno con evidencia verificable (cambio, prueba o comando). Si el DoD no está disponible, indícalo explícitamente en la especificación; no inventes criterios ni declares cumplido lo que no se verificó. Señala como pendiente cualquier punto que dependa de acciones externas al alcance backend.

Toma las decisiones tecnológicas explícitas de la especificación aprobada por Arquitectura como fuente prioritaria: respeta el lenguaje y su versión, framework, herramienta de construcción y base de datos definidos allí, aunque sustituyan Java 25, Quarkus, Maven o PostgreSQL. Estos últimos son valores de respaldo únicamente para las tecnologías que Arquitectura no haya definido. Si una decisión de Arquitectura contradice la configuración real del repositorio o el formato de extracción disponible, no la reemplaces silenciosamente por los valores de respaldo: documenta la incompatibilidad, su impacto y el supuesto o bloqueo mínimo en la especificación.

Implementa los endpoints y servicios necesarios sin alterar rutas, esquemas, formatos de respuesta ni otros elementos del contrato aprobado. Valida entradas en el límite apropiado y devuelve errores coherentes con el contrato. Define el acceso a datos y los límites transaccionales necesarios, manteniendo consistencia ante errores.

Para persistencia, consume el contrato, esquema y migraciones aprobados por el rol Datos cuando estén presentes; no los dupliques ni los reemplaces. Si el flujo no incluye ese rol (equipo de seis), especifica e incluye solo el esquema y las migraciones indispensables para esta feature, con estrategia de reversión cuando corresponda.

Protege comportamiento crítico con pruebas de caracterización si la cobertura existente no basta. Incluye al menos un caso válido y uno de error, y comandos concretos de la herramienta de construcción definida por Arquitectura para comprobarlos (Maven solo si es la opción aprobada o la alternativa de respaldo). Ejecuta pruebas relevantes solo si el entorno lo permite; informa exactamente qué se ejecutó y su resultado, y no presentes comandos propuestos como evidencia de ejecución.

Limita los cambios a la feature, usa los patrones y el estilo ya adoptados, y registra riesgos residuales, supuestos y verificaciones pendientes. Respeta la rama aprobada por el flujo del Issue; no impongas nombres ni afirmes haber creado una rama o PR. No incluyas en el resultado tareas ajenas ni afirmes evidencia de auditoría, pruebas o PR que no se haya obtenido realmente. No apliques cambios al workspace: entrega la especificación y los archivos Java como artefactos en la respuesta."""
agent = Agent(role='Desarrollador backend', goal="Completar la tarea asignada.",
              backstory="Eres un integrante del equipo.", llm=llm,
              verbose=True, allow_delegation=False)


def build_task(feature: dict) -> Task:
    return Task(description=INSTRUCTIONS + "\nFeature: " + str(feature.get("title", ""))
                + "\n" + str(feature.get("description", ""))
                + "\n" + str(feature.get("acceptance_criteria", [])),
                expected_output='''Primero entrega una sección titulada `backend_spec.md` cuyo contenido sea un documento Markdown real, no texto plano ni un bloque de código. Incluye alcance, tecnologías priorizadas según Arquitectura, endpoints y contratos, validaciones y errores, acceso a datos y transacciones, una lista trazable de criterios del Definition of Done con su evidencia o estado pendiente, pruebas (caso válido y error), comandos de verificación acordes con la herramienta de construcción aprobada, resultados realmente comprobados, riesgos residuales y supuestos. Luego entrega cada archivo Java necesario en un bloque ```java independiente. La primera línea de cada bloque debe ser // Nombre.java y enseguida debe aparecer la declaración package correspondiente a su ubicación de extracción (por ejemplo, pe.bcp.login.resource, pe.bcp.login.service, pe.bcp.login.repository, pe.bcp.login.dto o pe.bcp.login.model). No incluyas archivos no Java en bloques que el extractor pueda guardar ni inventes resultados de ejecución.''', agent=agent)
