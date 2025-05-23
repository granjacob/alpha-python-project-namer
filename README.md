# newgran

**`newgran`** es una utilidad de línea de comandos en Python que genera nombres de proyecto únicos utilizando combinaciones del alfabeto griego, basados en palabras clave que describen el proyecto. Además, crea el directorio correspondiente con ese nombre y lleva un registro de los nombres usados por directorio.

## 🧠 ¿Cómo funciona?

- Usa el alfabeto griego para prefijar el nombre del proyecto.
- Las palabras clave que describen el stack (por ejemplo: `react,postgresql,springboot`) se agregan al nombre.
- Opcionalmente puedes agregar un sufijo (por ejemplo: `books`).
- Si un proyecto es eliminado, el prefijo griego puede ser reutilizado automáticamente.
- El progreso se guarda por directorio en `~/.gran_state`.

---

## 🚀 Instalación

1. Guarda el archivo del script como `newgran`.
2. Dale permisos de ejecución:

   ```bash
   chmod +x newgran
