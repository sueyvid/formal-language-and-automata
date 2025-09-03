import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Scrollable Frame Example")

# 1. Container
container = ttk.Frame(root)
container.pack(fill="both", expand=True)

# 2. Canvas
canvas = tk.Canvas(container, highlightthickness=0)
canvas.pack(side="left", fill="both", expand=True)

# 3. Scrollbar vertical
scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
scrollbar.pack(side="right", fill="y")
canvas.configure(yscrollcommand=scrollbar.set)

# 4. Frame rolável dentro do canvas
scrollable_frame = ttk.Frame(canvas)
canvas_frame_id = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

# 5. Atualiza a scrollregion e (opcional) faz o frame interno acompanhar a largura do canvas
def on_frame_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))
    # Mantém a largura do frame interna igual à largura do canvas (evita "sobras" horizontais)
    if scrollable_frame.winfo_reqwidth() != canvas.winfo_width():
        canvas.itemconfigure(canvas_frame_id, width=canvas.winfo_width())

scrollable_frame.bind("<Configure>", on_frame_configure)

# 6. Handler do mouse wheel (Windows/macOS via delta; Linux via Button-4/5)
def on_mouse_wheel(event):
    # Sobe: delta > 0 (Win/mac) ou Button-4 (Linux)
    if getattr(event, "num", None) == 4 or getattr(event, "delta", 0) > 0:
        canvas.yview_scroll(-1, "units")
    # Desce: delta < 0 (Win/mac) ou Button-5 (Linux)
    elif getattr(event, "num", None) == 5 or getattr(event, "delta", 0) < 0:
        canvas.yview_scroll(1, "units")

# 7. Liga o scroll quando o mouse está sobre o canvas/área interna
def enable_scrolling(widget):
    # Garante que o canvas receba o evento de rolagem
    widget.bind("<Enter>", lambda e: canvas.focus_set())
    # Windows / macOS
    widget.bind("<MouseWheel>", on_mouse_wheel)
    # Linux (X11)
    widget.bind("<Button-4>", on_mouse_wheel)
    widget.bind("<Button-5>", on_mouse_wheel)

enable_scrolling(canvas)
enable_scrolling(scrollable_frame)

# 8. Exemplo de conteúdo
for i in range(50):
    ttk.Label(scrollable_frame, text=f"Item {i}").pack(pady=2, padx=5)

root.mainloop()
