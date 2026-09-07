import tkinter as tk
import numpy as np
from arbiter import Arbiter

weights = np.array([
    [100, 0,   0],   # Пешеход → V_h
    [90,  0,   0],   # Перегрев → V_h
    [95,  0,   0],   # Давление масла → V_h
    [0,   70,  0],   # Красный свет → V_e
    [0,   0,   80],  # Знак СТОП → V_s
    [0,   60,  0],   # Потеряна разметка → V_e
    [0,   88,  0],   # Затор → V_e
    [0,   0,   70],  # Регулировщик → V_s
    [0,   0,   60],  # Водитель газ → V_s
    [0,   0,   65],  # Водитель тормоз → V_s
])

labels = [
    "Пешеход", "Перегрев", "Давление масла",
    "Красный свет", "Знак СТОП", "Потеряна разметка", "Затор", "Регулировщик",
    "Водитель газ", "Водитель тормоз"
]

event_actions = {
    "Пешеход": "ЭКСТРЕННОЕ ТОРМОЖЕНИЕ!",
    "Перегрев": "Остановка из-за перегрева.",
    "Давление масла": "Остановка из-за давления масла.",
    "Красный свет": "Остановка перед светофором.",
    "Знак СТОП": "Полная остановка у знака «Стоп».",
    "Потеряна разметка": "Снижение скорости, ориентирование по краю дороги.",
    "Затор": "Остановка перед затором.",
    "Регулировщик": "Выполнение команды регулировщика.",
    "Водитель газ": "Ускорение.",
    "Водитель тормоз": "Торможение.",
}

window = tk.Tk()
window.title("Нейроарбитр — трёхконтурная архитектура")
window.geometry("750x700")

tk.Label(window, text="Безопасность (V_h)", font=("Arial", 10, "bold")).grid(row=0, column=0)
tk.Label(window, text="Навигация (V_e)", font=("Arial", 10, "bold")).grid(row=0, column=1)
tk.Label(window, text="Социальное (V_s)", font=("Arial", 10, "bold")).grid(row=0, column=2)

vars_list = []
columns = [0, 0, 0, 1, 2, 1, 1, 2, 2, 2]
rows    = [1, 2, 3, 1, 1, 2, 3, 2, 3, 4]

for i, text in enumerate(labels):
    var = tk.BooleanVar()
    vars_list.append(var)
    tk.Checkbutton(window, text=text, variable=var).grid(row=rows[i], column=columns[i], sticky="w")

log_text = tk.Text(window, height=18, width=85)
log_text.grid(row=7, column=0, columnspan=3, pady=10)

log_text.tag_config("interrupt", foreground="red", font=("Arial", 10, "bold"))
log_text.tag_config("winner", foreground="blue", font=("Arial", 10, "bold"))
log_text.tag_config("normal", foreground="black")
log_text.tag_config("hysteresis", foreground="#888888")
log_text.tag_config("modulation", foreground="#aa6600", font=("Arial", 10, "bold"))

arbiter = Arbiter()

def update():
    inputs = np.array([1 if v.get() else 0 for v in vars_list])
    contributions = inputs[:, None] * weights
    raw = np.max(contributions, axis=0)
    base = np.array([10, 40, 10])
    priorities = np.maximum(base, raw)

    class FakeContour:
        def __init__(self, name, priority):
            self.name = name
            self.current_priority = int(priority)

    vh = FakeContour("V_h", priorities[0])
    ve = FakeContour("V_e", priorities[1])
    vs = FakeContour("V_s", priorities[2])

    winner, note = arbiter.decide([vh, ve, vs])

    winner_idx = {"V_h": 0, "V_e": 1, "V_s": 2}[winner.name]
    active_indices = [i for i, v in enumerate(vars_list) if v.get()]
    top_event = None
    top_value = -1
    for i in active_indices:
        val = weights[i][winner_idx]
        if val > top_value:
            top_value = val
            top_event = labels[i]

    log_text.insert(tk.END, "\n=== Обновление ===\n", "normal")
    active_events = [labels[i] for i in active_indices]
    if active_events:
        log_text.insert(tk.END, "События: " + ", ".join(active_events) + "\n", "normal")
    else:
        log_text.insert(tk.END, "События: нет\n", "normal")

    log_text.insert(tk.END, f"V_h: {vh.current_priority}  V_e: {ve.current_priority}  V_s: {vs.current_priority}\n", "normal")
    log_text.insert(tk.END, f"ПОБЕДИЛ: {winner.name}\n", "winner")

    if top_event:
        log_text.insert(tk.END, f"ГЛАВНОЕ СОБЫТИЕ: {top_event}\n", "normal")
        log_text.insert(tk.END, f"ДЕЙСТВИЕ: {event_actions[top_event]}\n", "normal")
    else:
        log_text.insert(tk.END, "ДЕЙСТВИЕ: Автомобиль движется по маршруту.\n", "normal")

    if note:
        if "ПРЕРЫВАНИЕ" in note:
            log_text.insert(tk.END, f"⚠ {note}\n", "interrupt")
        elif "Модуляция" in note:
            log_text.insert(tk.END, f"⚡ {note}\n", "modulation")
        elif "Гистерезис" in note:
            log_text.insert(tk.END, f"ℹ {note}\n", "hysteresis")
        else:
            log_text.insert(tk.END, f"{note}\n", "normal")
    log_text.see(tk.END)


def copy_text(event):
    try:
        selected = log_text.get("sel.first", "sel.last")
        window.clipboard_clear()
        window.clipboard_append(selected)
    except tk.TclError:
        pass

menu = tk.Menu(window, tearoff=0)
menu.add_command(label="Копировать", command=lambda: copy_text(None))

def show_menu(event):
    menu.tk_popup(event.x_root, event.y_root)

log_text.bind("<Button-3>", show_menu)

def loop():
    update()
    window.after(3000, loop)

loop()
window.mainloop()
window.mainloop()
