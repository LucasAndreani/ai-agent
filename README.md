# AI Agent

Herramienta de línea de comandos que usa la API de Gemini para actuar como agente autónomo de asistencia en programación. Dado un prompt, el agente planifica y ejecuta una secuencia de acciones sobre el código: lee archivos, los modifica y los ejecuta hasta resolver la tarea.

Inspirado en herramientas como Claude Code o Gemini CLI.


El agente corre un loop de hasta 20 iteraciones. En cada una, Gemini decide qué función llamar según el estado actual de la tarea. Cuando ya no necesita ejecutar más acciones, devuelve la respuesta final al usuario.

```
prompt de usuario
      ↓
  Gemini 2.0 Flash
      ↓
  ¿necesita usar una tool?
   ├── Sí → ejecuta la función → agrega resultado al contexto → repite
   └── No → imprime respuesta final
```

## Funciones disponibles

| Tool | Descripción |
|---|---|
| `get_files_info` | Lista archivos y directorios con su tamaño |
| `get_file_content` | Lee el contenido de un archivo (máx. 10.000 caracteres) |
| `write_file` | Escribe o sobreescribe un archivo |
| `run_python_file` | Ejecuta un archivo `.py` con argumentos opcionales (timeout: 30s) |

Todas las operaciones están restringidas al directorio de trabajo — el agente no puede leer ni modificar archivos fuera de él.

## Estructura del proyecto

```
ai_agent/
├── main.py                  # Entrypoint CLI y loop del agente
└── functions/
    ├── config.py            # System prompt y constantes
    ├── call_function.py     # Dispatcher de tools
    ├── get_files_info.py    # Tool: listar archivos
    ├── get_file_content.py  # Tool: leer archivo
    ├── write_file.py        # Tool: escribir archivo
    └── run_python.py        # Tool: ejecutar Python
```

## Requisitos

- Python 3.8+
- Cuenta y API key de [Google Gemini](https://aistudio.google.com/)

## Instalación

```bash
git clone https://github.com/LucasAndreani/ai-agent.git
cd ai-agent

pip install google-genai python-dotenv
```

Crear un archivo `.env` en la raíz del proyecto:

```
GEMINI_API_KEY=tu_api_key_aqui
```

## Uso

```bash
python -m ai_agent.main "tu prompt acá"
```

Para ver los detalles de cada llamada a función y el uso de tokens:

```bash
python -m ai_agent.main "tu prompt acá" --verbose
```

### Ejemplo

```bash
python -m ai_agent.main "Revisá el archivo calculator.py, corregí los errores y ejecutalo"
```

El agente va a leer el archivo, identificar los errores, reescribirlo y ejecutarlo, todo de forma autónoma.
