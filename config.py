import os
from dotenv import load_dotenv

# Cargar variables desde .env
load_dotenv()


class Config:
    UPLOAD_FOLDER = 'uploads'
    ROWS = 80
    COLS = 80
    PROBABILITY = 0.95
