import os
import json
from flask import Blueprint, render_template, send_file, jsonify
from app.services.grid_service import create_grid, create_mask, exists_grid, image_info
from config import Config

main = Blueprint("home_blueprint", __name__)


@main.route("/")
def index():
    rows = Config.ROWS
    cols = Config.COLS
    probability = Config.PROBABILITY

    if not exists_grid():
        grid = create_grid(rows, cols, probability)
        imageWidth, imageHeight = create_mask(rows, cols, grid)

    imageWidth, imageHeight = image_info()

    return render_template("index.html", width=imageWidth, height=imageHeight)


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


@main.route("/create_random_grid")
def create_random_grid():
    rows = Config.ROWS
    cols = Config.COLS
    probability = Config.PROBABILITY

    grid = create_grid(rows, cols, probability)
    imageWidth, imageHeight = create_mask(rows, cols, grid)

    return render_template("index.html", width=imageWidth, height=imageHeight)
