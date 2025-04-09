# Crear entorno virtual
python -m venv venv

# Activarlo Mac
source venv/bin/activate
# Windows
.\venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Correr app
python run.py

# En caso permisos para ejecutar PowerShell en Visual Code
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
