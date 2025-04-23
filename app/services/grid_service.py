import os
import json
import numpy as np
from PIL import Image, ImageDraw
from config import Config

upload_folder = Config.UPLOAD_FOLDER

def exists_grid():
    matrix_path = os.path.join('app', upload_folder, "matrix.json")
    return os.path.exists(matrix_path)

def image_info():
    image_path = os.path.join('app', upload_folder, "base.png")
    if not os.path.exists(image_path):
        return "No se encontró la imagen base.", 404

    img = Image.open(image_path).convert("RGBA")
    imageWidth, imageHeight = img.size
    return imageWidth, imageHeight

def reset_grid(rows, cols):
    """
    Inicializa siempre la matriz a 1 (todas las casillas enmascaradas)
    y genera la máscara result.png.
    """
    grid_matrix = np.ones((rows, cols), dtype=int)
    matrix_path = os.path.join('app', upload_folder, "matrix.json")
    with open(matrix_path, "w") as f:
        json.dump(grid_matrix.tolist(), f)
    create_mask(rows, cols, grid_matrix)
    return grid_matrix

def create_mask(rows, cols, grid):
    os.makedirs(upload_folder, exist_ok=True)
    image_path = os.path.join('app', upload_folder, "base.png")
    if not os.path.exists(image_path):
        return "No se encontró la imagen base.", 404

    img = Image.open(image_path).convert("RGBA")
    imageWidth, imageHeight = img.size

    cell_w = imageWidth // cols
    cell_h = imageHeight // rows
    mask = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(mask)

    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == 1:
                x0 = j * cell_w
                y0 = i * cell_h
                x1 = x0 + cell_w
                y1 = y0 + cell_h
                draw.rectangle([x0, y0, x1 - 1, y1 - 1], fill=(0, 0, 0, 255))

    result = Image.alpha_composite(img, mask)
    result_path = os.path.join('app', upload_folder, "result.png")
    result.save(result_path)

    return imageWidth, imageHeight

def reveal_cell(row, col):
    """
    Cambia la casilla (row,col) a 0 (revelado) y vuelve a generar result.png.
    """
    matrix_path = os.path.join('app', upload_folder, "matrix.json")
    with open(matrix_path, "r") as f:
        grid = np.array(json.load(f))

    if grid[row][col] == 1:
        grid[row][col] = 0
        with open(matrix_path, "w") as f:
            json.dump(grid.tolist(), f)
        create_mask(grid.shape[0], grid.shape[1], grid)
