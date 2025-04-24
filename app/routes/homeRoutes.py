import os
import json
from flask import Blueprint, render_template, send_file, jsonify, request
from app.services.grid_service import (
    reset_grid, reveal_cell, exists_grid, image_info
)
from config import Config
# Importamos el objeto socketio del entrypoint
from run import socketio

main = Blueprint("home_blueprint", __name__)

@main.route("/")
def index():
    rows, cols = Config.ROWS, Config.COLS
    if not exists_grid():
        reset_grid(rows, cols)
    imageWidth, imageHeight = image_info()
    return render_template("index.html", width=imageWidth, height=imageHeight)

# ... tus endpoints /matrix y /questions ...

@main.route("/reveal", methods=["POST"])
def reveal():
    data = request.get_json()
    row = data.get("row")
    col = data.get("col")
    if row is None or col is None:
        return jsonify({"error": "Faltan coordenadas"}), 400

    try:
        reveal_cell(row, col)
        # Emitimos a todos los clientes que se reveló un pixel
        socketio.emit(
            "pixel_revealed",
            {"row": row, "col": col},
            broadcast=True
        )
        return jsonify({"status": "ok"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
