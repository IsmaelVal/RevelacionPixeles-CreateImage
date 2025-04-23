 import os
 import json
 import numpy as np
 from PIL import Image, ImageDraw
 from config import Config

 upload_folder = Config.UPLOAD_FOLDER

+def reset_grid(rows, cols):
+    """
+    Inicializa siempre la matriz a 1 (todas las casillas enmascaradas)
+    y genera la máscara result.png.
+    """
+    grid_matrix = np.ones((rows, cols), dtype=int)
+    matrix_path = os.path.join('app', upload_folder, "matrix.json")
+    with open(matrix_path, "w") as f:
+        json.dump(grid_matrix.tolist(), f)
+    create_mask(rows, cols, grid_matrix)
+    return grid_matrix

 def exists_grid():
     matrix_path = os.path.join('app', upload_folder, "matrix.json")
     return os.path.exists(matrix_path)

 def image_info():
     # … tu código …
     return imageWidth, imageHeight

-def create_grid(rows, cols, probability):
-    grid_matrix = np.random.choice(
-        [0, 1], size=(rows, cols), p=[1 - probability, probability]
-    )
-    matrix_path = os.path.join('app', upload_folder, "matrix.json")
-    with open(matrix_path, "w") as f:
-        json.dump(grid_matrix.tolist(), f)
-    create_mask(rows, cols, grid_matrix)
-    return grid_matrix

 def create_mask(rows, cols, grid):
     # … tu código de dibujar la máscara …
     result.save(result_path)
     return imageWidth, imageHeight

+def reveal_cell(row, col):
+    """
+    Cambia la casilla (row,col) a 0 (revelado) y vuelve a generar result.png.
+    """
+    matrix_path = os.path.join('app', upload_folder, "matrix.json")
+    with open(matrix_path, "r") as f:
+        grid = np.array(json.load(f))
+
+    if grid[row][col] == 1:
+        grid[row][col] = 0
+        with open(matrix_path, "w") as f:
+            json.dump(grid.tolist(), f)
+        # Regenera la máscara con la celda desbloqueada
+        create_mask(grid.shape[0], grid.shape[1], grid)
