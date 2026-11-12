# Manual de Instalación, Ejecución y Versionado en Git (Windows / VS Code)

## 1. Requisitos del Sistema
- Sistema Operativo Windows 10/11
- Python 3.10+ instalado
- Git instalado 
- Visual Studio Code

# 2. Clonación del repositorio y ubicación en linea base
```bash
git clone https://github.com/Melannyqo21/SIGR.git

cd sigr

git checkout v1.0.0

```

# 3. Pasos para Ejecutar en VS Code - Windows
```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
.\venv\Scripts\activate 

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar aplicación
python run.py
```

# 4. Acceder al navegador

http://127.0.0.1:5000