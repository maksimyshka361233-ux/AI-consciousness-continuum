import tkinter as tk
from contours import VitalContour, CognitiveContour, SocialContour
from arbiter import Arbiter

# Создаём контуры и арбитра
vh = VitalContour()
ve = CognitiveContour()
vs = SocialContour()
arbiter = Arbiter()

# Создаём главное окно
window = tk.Tk()
window.title("Трёхконтурный автопилот")
window.geometry("700x650")

# Заголовки блоков
tk.Label(window, text="Безопасность (V_h)", font=("Arial", 10, "bold")).grid(row=0, column=0)
tk.Label(window, text="Навигация и правила (V_e)", font=("Arial", 10, "bold")).grid(row=0, column=1)
tk.Label(window, text="Люди и сигналы (V_s)", font=("Arial", 10, "bold")).grid(row=0, column=2)

# Переменные для чекбоксов
var_pedestrian = tk.BooleanVar()
var_overheat = tk.BooleanVar()
var_oilpressure = tk.BooleanVar()

var_redlight = tk.BooleanVar()
var_stopsign = tk.BooleanVar()
var_nomark = tk.BooleanVar()
var_traffic = tk.BooleanVar()
var_officer = tk.BooleanVar()

var_driver_gas = tk.BooleanVar()
var_driver_brake = tk.BooleanVar()
var_other_signal = tk.BooleanVar()

# Чекбоксы V_h
tk.Checkbutton(window, text="Пешеход", variable=var_pedestrian).grid(row=1, column=0, sticky="w")
tk.Checkbutton(window, text="Перегрев (>120)", variable=var_overheat).grid(row=2, column=0, sticky="w")
tk.Checkbutton(window, text="Давление масла <0.5", variable=var_oilpressure).grid(row=3, column=0, sticky="w")

# Чекбоксы V_e
tk.Checkbutton(window, text="Красный свет", variable=var_redlight).grid(row=1, column=1, sticky="w")
tk.Checkbutton(window, text="Знак «Стоп»", variable=var_stopsign).grid(row=2, column=1, sticky="w")
tk.Checkbutton(window, text="Потеряна разметка", variable=var_nomark).grid(row=3, column=1, sticky="w")
tk.Checkbutton(window, text="Затор впереди", variable=var_traffic).grid(row=4, column=1, sticky="w")
tk.Checkbutton(window, text="Регулировщик", variable=var_officer).grid(row=5, column=1, sticky="w")

# Чекбоксы V_s
tk.Checkbutton(window, text="Водитель жмёт газ", variable=var_driver_gas).grid(row=1, column=2, sticky="w")
tk.Checkbutton(window, text="Водитель жмёт тормоз", variable=var_driver_brake).grid(row=2, column=2, sticky="w")
tk.Checkbutton(window, text="Сигналы других машин", variable=var_other_signal).grid(row=3, column=2, sticky="w")

# Лог
log_text = tk.Text(window, height=15, width=80)
log_text.grid(row=6, column=0, columnspan=3, pady=10)

def update():
    # Очищаем все контуры
    vh.clear_events()
    ve.clear_events()
    vs.clear_events()

    # События V_h
    if var_pedestrian.get():
        vh.add_event("Пешеход", 100)
    if var_overheat.get():
        vh.add_event("Перегрев", 90)
    if var_oilpressure.get():
        vh.add_event("Давление масла", 95)

    # События V_e
    if var_redlight.get():
        ve.add_event("Красный свет", 45)
    if var_stopsign.get():
        ve.add_event("Знак СТОП", 50)
    if var_nomark.get():
        ve.add_event("Потеряна разметка", 60)
    if var_traffic.get():
        ve.add_event("Затор", 80)
    if var_officer.get():
        ve.add_event("Регулировщик", 70)

    # События V_s
    if var_driver_gas.get():
        vs.add_event("Водитель: газ", 60)
    if var_driver_brake.get():
        vs.add_event("Водитель: тормоз", 65)
    if var_other_signal.get():
        vs.add_event("Сигналы других машин", 55)

    # Решение арбитра
    winner, interrupt = arbiter.decide([vh, ve, vs])

    # Вывод в лог
    log_text.insert(tk.END, "\n=== Обновление ===\n")
    log_text.insert(tk.END, vh.status() + "\n")
    log_text.insert(tk.END, ve.status() + "\n")
    log_text.insert(tk.END, vs.status() + "\n")

    # Описание действия
    action = ""
    if winner.name == "V_h":
        action = "ЭКСТРЕННОЕ ТОРМОЖЕНИЕ! Автомобиль резко остановлен!"
    elif winner.name == "V_e":
        if var_officer.get():
            action = "Автомобиль выполняет команду регулировщика."
        elif var_traffic.get():
            action = "Автомобиль останавливается перед затором."
        elif var_redlight.get():
            action = "Автомобиль останавливается перед красным светофором."
        elif var_stopsign.get():
            action = "Автомобиль выполняет полную остановку у знака «Стоп»."
        elif var_nomark.get():
            action = "Автомобиль снижает скорость и ориентируется по краю дороги."
        else:
            action = "Автомобиль продолжает движение по маршруту."
    elif winner.name == "V_s":
        if var_driver_gas.get() and not var_driver_brake.get():
            action = "Водитель жмёт газ, автомобиль ускоряется."
        elif var_driver_brake.get():
            action = "Водитель жмёт тормоз, автомобиль останавливается."
        elif var_other_signal.get():
            action = "Автомобиль реагирует на сигналы других машин."
        else:
            action = "Автомобиль следует социальным сигналам."

    log_text.insert(tk.END, f"ДЕЙСТВИЕ: {action}\n")
    if interrupt:
        log_text.insert(tk.END, f"({interrupt})\n")
    log_text.see(tk.END)


# Функция для копирования
def copy_text(event):
    try:
        selected = log_text.get("sel.first", "sel.last")
        window.clipboard_clear()
        window.clipboard_append(selected)
    except tk.TclError:
        pass

# Контекстное меню
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
