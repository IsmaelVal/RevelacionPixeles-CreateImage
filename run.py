from app import init_app
from config import Config
from flask_socketio import SocketIO

app = init_app()
app.config.from_object(Config)

# Inicializa SocketIO
socketio = SocketIO(app, cors_allowed_origins="*")

if __name__ == "__main__":
    # Usamos eventlet para concurrencia
    socketio.run(app, debug=True)
