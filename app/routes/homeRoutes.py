import os
import json
import random
from flask import Blueprint, render_template, send_file, jsonify, request
from config import Config
from app.services.grid_service import (
    reset_grid, reveal_cell, exists_grid, image_info
)
from app import socketio
from flask_socketio import emit

main = Blueprint("home_blueprint", __name__)

@main.route("/")
def index():
    rows, cols = Config.ROWS, Config.COLS
    if not exists_grid():
        reset_grid(rows, cols)
    w, h = image_info()
    return render_template("index.html", width=w, height=h)

@main.route("/matrix")
def get_matrix():
    matrix_path = os.path.join('app', Config.UPLOAD_FOLDER, "matrix.json")
    if not os.path.exists(matrix_path):
        return jsonify({"error": "No hay matriz cargada"}), 404
    with open(matrix_path, "r") as f:
        matrix = json.load(f)
    return jsonify(matrix)

@main.route("/uploads/<filename>")
def serve_image(filename):
    return send_file(os.path.join(Config.UPLOAD_FOLDER, filename))

@main.route("/questions/<int:row>/<int:col>")
def get_question(row, col):
    questions_path = os.path.join('app', Config.UPLOAD_FOLDER, "questions.json")
    if not os.path.exists(questions_path):
        return jsonify({"error": "No hay preguntas disponibles"}), 404

    with open(questions_path, "r", encoding="utf-8") as f:
        pool = json.load(f)

    pregunta = random.choice(pool)
    return jsonify(pregunta)

# --------------------------------------------------------------------------------
# NUEVO: manejador SocketIO para revelar píxel
@socketio.on('reveal_pixel')
def handle_reveal_pixel(data):
    row = data.get('row')
    col = data.get('col')
    if row is None or col is None:
        return
    try:
        reveal_cell(row, col)  
        # Le avisamos a TODOS los clientes (incluido el que disparó el evento)
        emit('pixel_revealed', {'row': row, 'col': col}, broadcast=True)
    except Exception:
        pass
