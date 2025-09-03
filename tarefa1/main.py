import tkinter as tk
from model import Model
from view import View
from controller import Controller

class App():
    def __init__(self):
        model = Model()

        view = View()

        controller = Controller(model, view)

        view.set_controller(controller)
        view.mainloop()

if __name__ == "__main__":
    app = App()
