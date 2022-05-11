from tkinter import messagebox


class Alerts:

    def warning(self, message):
        """Выводит окно предупреждения."""
        messagebox.showwarning("Предупреждение", message)

    def error(self, message):
        """Выводит окно об ошибке."""
        messagebox.showerror("Ошибка", message)