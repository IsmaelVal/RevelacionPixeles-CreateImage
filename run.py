from app import init_app, socketio

app = init_app()

if __name__ == "__main__":
    # Arrancamos con socketio.run en lugar de app.run
    socketio.run(app, debug=True)
