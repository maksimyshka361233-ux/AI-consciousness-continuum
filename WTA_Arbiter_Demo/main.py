import tkinter as tk
import numpy as np
from arbiter import Arbiter

# Матрица весов: 10 входов -> 3 контура
weights = np.array([
    [100, 0, 0],
    [90, 0, 0],
    [95, 0, 0],
    [0, 45, 0],
    [0, 80, 0],
    [0, 60, 0],
    [0, 80, 0],
    [0, 85, 0],
    [0, 0, 60],
    [0, 0, 65],
])

# Названия событий
labels = [
    "Пешеход", "Перегрев", "Давление масла",
    "Красный свет", "Знак СТОП", "Потеряна разметка", "Затор", "Регулировщик",
    "Водитель газ", "Водитель тормоз"
]

# Действия для каждого события, если оно победило
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
window.title("Нейроарбитр")
window.geometry("700x650")

tk.Label(window, text="Безопасность (V_h)", font=("Arial", 10, "bold")).grid(row=0, column=0)
tk.Label(window, text="Навигация (V_e)", font=("Arial", 10, "bold")).grid(row=0, column=1)
tk.Label(window, text="Социальное (V_s)", font=("Arial", 10, "bold")).grid(row=0, column=2)

vars_list = []
columns = [0, 0, 0, 1, 1, 1, 1, 1, 2, 2]
rows = [1, 2, 3, 1, 2, 3, 4, 5, 1, 2]

for i, text in enumerate(labels):
    var = tk.BooleanVar()
    vars_list.append(var)
    tk.Checkbutton(window, text=text, variable=var).grid(row=rows[i], column=columns[i], sticky="w")

log_text = tk.Text(window, height=15, width=80)
log_text.grid(row=6, column=0, columnspan=3, pady=10)

arbiter = Arbiter()

def update():
    inputs = np.array([1 if v.get() else 0 for v in vars_list])
    contributions = inputs[:, None] * weights
    raw = np.max(contributions, axis=0)
    base = np.array([10, 40, 10])
    priorities = np.maximum(base, raw)

    # Каждый раз — новый выбор
    arbiter.current_winner = None

    class FakeContour:
        def __init__(self, name, priority):
            self.name = name
            self.current_priority = int(priority)

    vh = FakeContour("V_h", priorities[0])
    ve = FakeContour("V_e", priorities[1])
    vs = FakeContour("V_s", priorities[2])

    winner, interrupt = arbiter.decide([vh, ve, vs])

    # Определяем главное событие победившего контура
    winner_idx = {"V_h": 0, "V_e": 1, "V_s": 2}[winner.name]
    active_indices = [i for i, v in enumerate(vars_list) if v.get()]
    top_event = None
    top_value = -1
    for i in active_indices:
        val = weights[i][winner_idx]
        if val > top_value:
            top_value = val
            top_event = labels[i]

    # Логи
    log_text.insert(tk.END, "\n=== Обновление ===\n")
    active_events = [labels[i] for i in active_indices]
    if active_events:
        log_text.insert(tk.END, "События: " + ", ".join(active_events) + "\n")
    else:
        log_text.insert(tk.END, "События: нет\n")

    log_text.insert(tk.END, f"V_h: {vh.current_priority}  V_e: {ve.current_priority}  V_s: {vs.current_priority}\n")
    log_text.insert(tk.END, f"ПОБЕДИЛ: {winner.name}\n")

    if top_event:
        log_text.insert(tk.END, f"ГЛАВНОЕ СОБЫТИЕ: {top_event}\n")
        log_text.insert(tk.END, f"ДЕЙСТВИЕ: {event_actions[top_event]}\n")
    else:
        log_text.insert(tk.END, "ДЕЙСТВИЕ: Автомобиль движется по маршруту.\n")

    if interrupt:
        log_text.insert(tk.END, f"({interrupt})\n")
    log_text.see(tk.END)
    class FakeContour:
        def __init__(self, name, priority):
            self.name = name
            self.current_priority = int(priority)

    vh = FakeContour("V_h", priorities[0])
    ve = FakeContour("V_e", priorities[1])
    vs = FakeContour("V_s", priorities[2])

    winner, interrupt = arbiter.decide([vh, ve, vs])

    # Определяем главное событие победившего контура
    winner_idx = {"V_h": 0, "V_e": 1, "V_s": 2}[winner.name]
    active_indices = [i for i, v in enumerate(vars_list) if v.get()]
    top_event = None
    top_value = -1
    for i in active_indices:
        val = weights[i][winner_idx]
        if val > top_value:
            top_value = val
            top_event = labels[i]

    # Логи
    log_text.insert(tk.END, "\n=== Обновление ===\n")
    active_events = [labels[i] for i in active_indices]
    if active_events:
        log_text.insert(tk.END, "События: " + ", ".join(active_events) + "\n")
    else:
        log_text.insert(tk.END, "События: нет\n")

    log_text.insert(tk.END, f"V_h: {vh.current_priority}  V_e: {ve.current_priority}  V_s: {vs.current_priority}\n")
    log_text.insert(tk.END, f"ПОБЕДИЛ: {winner.name}\n")

    if top_event:
        log_text.insert(tk.END, f"ГЛАВНОЕ СОБЫТИЕ: {top_event}\n")
        log_text.insert(tk.END, f"ДЕЙСТВИЕ: {event_actions[top_event]}\n")
    else:
        log_text.insert(tk.END, "ДЕЙСТВИЕ: Автомобиль движется по маршруту.\n")

    if interrupt:
        log_text.insert(tk.END, f"({interrupt})\n")
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
loop()

window.mainloop()
