import tkinter as tk
from tkinter import ttk

class ScrollableFrame:
    def __init__(self, parent):
        # Container dentro do frame pai
        self.container = ttk.Frame(parent)
        self.container.pack(fill="both", expand=True)

        # Canvas
        self.canvas = tk.Canvas(self.container, highlightthickness=0, width=300, height=300)
        self.canvas.pack(side="left", fill="both", expand=True)

        # Scrollbar vertical
        self.scrollbar = ttk.Scrollbar(self.container, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Frame rolável dentro do canvas
        self.scrollable_frame = ttk.Frame(self.canvas)
        self.canvas_frame_id = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        # Atualiza a região de scroll quando o conteúdo muda
        self.scrollable_frame.bind("<Configure>", self._on_frame_configure)

        # Habilita scroll com mouse
        self._enable_scrolling(self.canvas)
        self._enable_scrolling(self.scrollable_frame)

    def _on_frame_configure(self, event):
        """Mantém o scroll atualizado e ajusta a largura do frame interno."""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        if self.scrollable_frame.winfo_reqwidth() != self.canvas.winfo_width():
            self.canvas.itemconfigure(self.canvas_frame_id, width=self.canvas.winfo_width())

    def _on_mouse_wheel(self, event):
        """Controle da rolagem com mouse (Windows, macOS, Linux)."""
        if getattr(event, "num", None) == 4 or getattr(event, "delta", 0) > 0:
            self.canvas.yview_scroll(-1, "units")
        elif getattr(event, "num", None) == 5 or getattr(event, "delta", 0) < 0:
            self.canvas.yview_scroll(1, "units")

    def _enable_scrolling(self, widget):
        """Liga o scroll quando o mouse está sobre o widget."""
        widget.bind("<Enter>", lambda e: self.canvas.focus_set())
        widget.bind("<MouseWheel>", self._on_mouse_wheel)   # Windows/macOS
        widget.bind("<Button-4>", self._on_mouse_wheel)     # Linux
        widget.bind("<Button-5>", self._on_mouse_wheel)     # Linux

    def adicionar_conteudo(self, texto: str):
        """Adiciona um novo Label com o texto fornecido."""
        ttk.Label(self.scrollable_frame, text=texto).pack(pady=2, padx=5)

    def limpar_canvas(self):
        """Remove todos os widgets do frame rolável."""
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()


# ---------------------- Exemplo de uso ----------------------
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Scrollable Frame Example")

    # Frame raiz
    main_frame = ttk.Frame(root)
    main_frame.pack(fill="both", expand=True)

    # Cria o scrollable
    sf = ScrollableFrame(main_frame)

    # Adiciona conteúdo inicial
    for i in range(20):
        sf.adicionar_conteudo(f"Item {i}")

    # Botões de teste
    button_frame = ttk.Frame(root)
    button_frame.pack(fill="x")

    ttk.Button(button_frame, text="Adicionar Item", command=lambda: sf.adicionar_conteudo("Novo item")).pack(side="left", padx=5, pady=5)
    ttk.Button(button_frame, text="Limpar", command=sf.limpar_canvas).pack(side="left", padx=5, pady=5)

    root.mainloop()
