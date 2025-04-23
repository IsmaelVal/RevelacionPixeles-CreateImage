 from flask import Blueprint, render_template, send_file, jsonify, request
 from app.services.grid_service import (
-    create_grid, create_mask, exists_grid, image_info
+    reset_grid, reveal_cell, exists_grid, image_info
 )
 from config import Config
 import os, json

 main = Blueprint("home_blueprint", __name__)

 @main.route("/")
 def index():
     rows, cols = Config.ROWS, Config.COLS

-    if not exists_grid():
-        grid = create_grid(rows, cols, Config.PROBABILITY)
+    # Si no hay matriz, inicialízala a todo enmascarado
+    if not exists_grid():
+        reset_grid(rows, cols)

     imageWidth, imageHeight = image_info()
     return render_template("index.html", width=imageWidth, height=imageHeight)

@@
 @main.route("/matrix")
 def get_matrix():
     # … tu código actual …
     return jsonify(matrix)

+# Endpoint para servir preguntas definidas en uploads/questions.json
+@main.route("/questions/<int:row>/<int:col>")
+def get_question(row, col):
+    questions_path = os.path.join('app', Config.UPLOAD_FOLDER, "questions.json")
+    if not os.path.exists(questions_path):
+        return jsonify({"error": "No hay archivo de preguntas"}), 404
+
+    with open(questions_path, "r") as f:
+        questions = json.load(f)
+
+    key = f"{row},{col}"
+    q = questions.get(key)
+    if not q:
+        return jsonify({"error": "Pregunta no encontrada"}), 404
+    return jsonify(q)

+# Endpoint para revelar una casilla tras respuesta correcta
+@main.route("/reveal", methods=["POST"])
+def reveal():
+    data = request.get_json()
+    row = data.get("row")
+    col = data.get("col")
+    if row is None or col is None:
+        return jsonify({"error": "Faltan coordenadas"}), 400
+    try:
+        reveal_cell(row, col)
+        return jsonify({"status": "ok"})
+    except Exception as e:
+        return jsonify({"error": str(e)}), 500
