from app import init_app
from config import Config

app = init_app()
app.config.from_object(Config)


if __name__ == "__main__":
    app.run(debug=True)
