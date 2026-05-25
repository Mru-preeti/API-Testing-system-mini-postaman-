import tkinter as tk
from ui.main_window import APITesterUI


def main():
    """Launch the API Tester application"""
    root = tk.Tk()
    app = APITesterUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
