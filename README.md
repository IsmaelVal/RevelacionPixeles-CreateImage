# Crear entorno virtual
python -m venv venv

# Activarlo Mac
source venv/bin/activate
# Windows CMD
.\venv\Scripts\activate
# Windows PS
.\venv\Scripts\Activate.ps1

# Instalar dependencias
pip install -r requirements.txt

# Requerimientos socked
pip install flask-socketio eventlet

# Correr app
python run.py

# En caso permisos para ejecutar PowerShell en Visual Code
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
