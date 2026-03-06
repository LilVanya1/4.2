import tkinter as tk
from tkinter import messagebox
import ctypes
import os
import sys
import math
import random

from circular_queue_py import Sruct

is_created = False
backend_type = "Python"
py_queue = Sruct()
cpp_dyn = None
cpp_stl = None

ext = ".dll" if sys.platform == "win32" else ".so"
base = os.path.dirname(os.path.abspath(__file__))

dyn_path = os.path.join(base, "circular_queue_dynamic" + ext)
if os.path.exists(dyn_path):
    cpp_dyn = ctypes.CDLL(dyn_path)
    cpp_dyn.lib_init.restype = None
    cpp_dyn.lib_add.restype = ctypes.c_int
    cpp_dyn.lib_add.argtypes = [ctypes.c_int]
    cpp_dyn.lib_dequeue.restype = ctypes.c_int
    cpp_dyn.lib_dequeue.argtypes = [ctypes.POINTER(ctypes.c_int)]
    cpp_dyn.lib_peek.restype = ctypes.c_int
    cpp_dyn.lib_peek.argtypes = [ctypes.POINTER(ctypes.c_int)]
    cpp_dyn.lib_clear.restype = None
    cpp_dyn.lib_size.restype = ctypes.c_int
    cpp_dyn.lib_get_elements.restype = ctypes.c_int
    cpp_dyn.lib_get_elements.argtypes = [ctypes.POINTER(ctypes.c_int), ctypes.c_int]

stl_path = os.path.join(base, "circular_queue_stl" + ext)
if os.path.exists(stl_path):
    cpp_stl = ctypes.CDLL(stl_path)
    cpp_stl.lib_init.restype = None
    cpp_stl.lib_add.restype = ctypes.c_int
    cpp_stl.lib_add.argtypes = [ctypes.c_int]
    cpp_stl.lib_dequeue.restype = ctypes.c_int
    cpp_stl.lib_dequeue.argtypes = [ctypes.POINTER(ctypes.c_int)]
    cpp_stl.lib_peek.restype = ctypes.c_int
    cpp_stl.lib_peek.argtypes = [ctypes.POINTER(ctypes.c_int)]
    cpp_stl.lib_clear.restype = None
    cpp_stl.lib_size.restype = ctypes.c_int
    cpp_stl.lib_get_elements.restype = ctypes.c_int
    cpp_stl.lib_get_elements.argtypes = [ctypes.POINTER(ctypes.c_int), ctypes.c_int]


def do_init():
    global py_queue
    if backend_type == "Python":
        py_queue = Sruct()
    elif backend_type == "C++ Dynamic" and cpp_dyn:
        cpp_dyn.lib_init()
    elif backend_type == "C++ STL" and cpp_stl:
        cpp_stl.lib_init()


def do_add(value):
    if backend_type == "Python":
        py_queue.add(value)
    elif backend_type == "C++ Dynamic" and cpp_dyn:
        cpp_dyn.lib_add(value)
    elif backend_type == "C++ STL" and cpp_stl:
        cpp_stl.lib_add(value)


def do_dequeue():
    if backend_type == "Python":
        return py_queue.dequeue()
    elif backend_type == "C++ Dynamic" and cpp_dyn:
        val = ctypes.c_int()
        res = cpp_dyn.lib_dequeue(ctypes.byref(val))
        if res == 0:
            return None
        return val.value
    elif backend_type == "C++ STL" and cpp_stl:
        val = ctypes.c_int()
        res = cpp_stl.lib_dequeue(ctypes.byref(val))
        if res == 0:
            return None
        return val.value
    return None


def do_peek():
    if backend_type == "Python":
        return py_queue.peek()
    elif backend_type == "C++ Dynamic" and cpp_dyn:
        val = ctypes.c_int()
        res = cpp_dyn.lib_peek(ctypes.byref(val))
        if res == 0:
            return None
        return val.value
    elif backend_type == "C++ STL" and cpp_stl:
        val = ctypes.c_int()
        res = cpp_stl.lib_peek(ctypes.byref(val))
        if res == 0:
            return None
        return val.value
    return None


def do_clear():
    if backend_type == "Python":
        py_queue.clear()
    elif backend_type == "C++ Dynamic" and cpp_dyn:
        cpp_dyn.lib_clear()
    elif backend_type == "C++ STL" and cpp_stl:
        cpp_stl.lib_clear()


def do_size():
    if backend_type == "Python":
        return py_queue.get_size()
    elif backend_type == "C++ Dynamic" and cpp_dyn:
        return cpp_dyn.lib_size()
    elif backend_type == "C++ STL" and cpp_stl:
        return cpp_stl.lib_size()
    return 0


def do_get_elements():
    if backend_type == "Python":
        return py_queue.get_elements()
    elif backend_type == "C++ Dynamic" and cpp_dyn:
        buf = (ctypes.c_int * 10000)()
        count = cpp_dyn.lib_get_elements(buf, 10000)
        result = []
        for i in range(count):
            result.append(buf[i])
        return result
    elif backend_type == "C++ STL" and cpp_stl:
        buf = (ctypes.c_int * 10000)()
        count = cpp_stl.lib_get_elements(buf, 10000)
        result = []
        for i in range(count):
            result.append(buf[i])
        return result
    return []


def log(msg):
    log_text.config(state=tk.NORMAL)
    log_text.insert(tk.END, msg + "\n")
    log_text.see(tk.END)
    log_text.config(state=tk.DISABLED)


def draw_queue():
    canvas.delete("all")

    if not is_created:
        canvas.create_text(440, 190, text="Структура не создана", font=("Arial", 16), fill="gray")
        return

    elements = do_get_elements()
    size = do_size()

    status_label.config(text="Бэкенд: " + backend_type + " | Элементов: " + str(size), fg="green")

    if size == 0:
        canvas.create_text(440, 190, text="Очередь пуста", font=("Arial", 16), fill="gray")
        return

    cx = 440
    cy = 200
    r = 150
    if size < 10:
        r = 30 + size * 12
    node_r = 22

    positions = []
    for i in range(size):
        angle = -math.pi / 2 + 2 * math.pi * i / size
        x = cx + r * math.cos(angle)
        y = cy + r * math.sin(angle)
        positions.append((x, y))

    for i in range(size):
        x1 = positions[i][0]
        y1 = positions[i][1]
        next_i = (i + 1) % size
        x2 = positions[next_i][0]
        y2 = positions[next_i][1]

        dx = x2 - x1
        dy = y2 - y1
        dist = math.sqrt(dx * dx + dy * dy)
        if dist == 0:
            continue

        sx = x1 + (dx / dist) * node_r
        sy = y1 + (dy / dist) * node_r
        ex = x2 - (dx / dist) * node_r
        ey = y2 - (dy / dist) * node_r

        canvas.create_line(sx, sy, ex, ey, arrow=tk.LAST, fill="#555", width=2)

    for i in range(size):
        x = positions[i][0]
        y = positions[i][1]

        if i == 0:
            color = "#4CAF50"
        elif i == size - 1:
            color = "#F44336"
        else:
            color = "#2196F3"

        canvas.create_oval(x - node_r, y - node_r, x + node_r, y + node_r, fill=color, width=2)
        canvas.create_text(x, y, text=str(elements[i]), font=("Arial", 10, "bold"), fill="white")

    hx = positions[0][0]
    hy = positions[0][1]
    canvas.create_text(hx, hy - node_r - 12, text="HEAD", font=("Arial", 9, "bold"), fill="green")

    tx = positions[size - 1][0]
    ty = positions[size - 1][1]
    canvas.create_text(tx, ty + node_r + 12, text="TAIL", font=("Arial", 9, "bold"), fill="red")


def on_backend_change():
    global is_created
    is_created = False
    status_label.config(text="Структура не создана (сменён бэкенд)", fg="red")
    draw_queue()
    log("Бэкенд сменён на: " + backend_var.get())


def btn_create():
    global is_created, backend_type
    backend_type = backend_var.get()
    do_init()
    is_created = True
    draw_queue()
    log("Структура создана.")


def btn_enqueue():
    if not is_created:
        messagebox.showwarning("Внимание", "Структура не создана! Нажмите 'Создать'.")
        return

    val_str = entry_value.get()
    if val_str == "":
        messagebox.showerror("Ошибка", "Введите число!")
        return

    try:
        value = int(val_str)
    except ValueError:
        messagebox.showerror("Ошибка", "Введите целое число!")
        return

    do_add(value)
    entry_value.delete(0, tk.END)
    draw_queue()
    log("Добавлен элемент: " + str(value))


def btn_dequeue():
    if not is_created:
        messagebox.showwarning("Внимание", "Структура не создана! Нажмите 'Создать'.")
        return

    if do_size() == 0:
        messagebox.showwarning("Внимание", "Очередь пуста! Нечего удалять.")
        log("Ошибка: удаление из пустой очереди.")
        return

    value = do_dequeue()
    draw_queue()
    log("Удалён элемент: " + str(value))


def btn_peek():
    if not is_created:
        messagebox.showwarning("Внимание", "Структура не создана! Нажмите 'Создать'.")
        return

    if do_size() == 0:
        messagebox.showwarning("Внимание", "Очередь пуста!")
        log("Ошибка: peek из пустой очереди.")
        return

    value = do_peek()
    messagebox.showinfo("Peek", "Первый элемент: " + str(value))
    log("Peek: " + str(value))


def btn_random():
    if not is_created:
        messagebox.showwarning("Внимание", "Структура не создана! Нажмите 'Создать'.")
        return

    try:
        count = int(entry_count.get())
        min_val = int(entry_min.get())
        max_val = int(entry_max.get())
    except ValueError:
        messagebox.showerror("Ошибка", "Заполните все поля целыми числами!")
        return

    if count <= 0:
        messagebox.showerror("Ошибка", "Количество должно быть положительным!")
        return

    if min_val > max_val:
        messagebox.showerror("Ошибка", "Минимум больше максимума!")
        return

    for i in range(count):
        value = random.randint(min_val, max_val)
        do_add(value)

    draw_queue()
    log("Добавлено " + str(count) + " случайных чисел [" + str(min_val) + ", " + str(max_val) + "]")


def btn_clear():
    if not is_created:
        messagebox.showwarning("Внимание", "Структура не создана! Нажмите 'Создать'.")
        return

    old_size = do_size()
    do_clear()
    draw_queue()
    log("Очередь очищена. Удалено: " + str(old_size))


root = tk.Tk()
root.title("Циклическая очередь")
root.geometry("900x720")
root.resizable(False, False)

top_frame = tk.Frame(root)
top_frame.pack(fill=tk.X, padx=10, pady=5)

tk.Label(top_frame, text="Бэкенд:", font=("Arial", 11)).pack(side=tk.LEFT)

backend_var = tk.StringVar(value="Python")

rb1 = tk.Radiobutton(top_frame, text="Python", variable=backend_var, value="Python",
                      font=("Arial", 10), command=on_backend_change)
rb1.pack(side=tk.LEFT, padx=5)

if cpp_dyn:
    rb2 = tk.Radiobutton(top_frame, text="C++ Dynamic", variable=backend_var, value="C++ Dynamic",
                          font=("Arial", 10), command=on_backend_change)
    rb2.pack(side=tk.LEFT, padx=5)

if cpp_stl:
    rb3 = tk.Radiobutton(top_frame, text="C++ STL", variable=backend_var, value="C++ STL",
                          font=("Arial", 10), command=on_backend_change)
    rb3.pack(side=tk.LEFT, padx=5)

status_label = tk.Label(root, text="Структура не создана", font=("Arial", 11, "bold"), fg="red")
status_label.pack(pady=2)

canvas = tk.Canvas(root, width=880, height=380, bg="white", relief=tk.SUNKEN, bd=2)
canvas.pack(padx=10, pady=5)

canvas.create_text(440, 190, text="Структура не создана", font=("Arial", 16), fill="gray")

input_frame = tk.Frame(root)
input_frame.pack(fill=tk.X, padx=10, pady=3)

tk.Label(input_frame, text="Значение:", font=("Arial", 10)).pack(side=tk.LEFT)
entry_value = tk.Entry(input_frame, width=8, font=("Arial", 10))
entry_value.pack(side=tk.LEFT, padx=5)

tk.Label(input_frame, text="Кол-во:", font=("Arial", 10)).pack(side=tk.LEFT, padx=(15, 0))
entry_count = tk.Entry(input_frame, width=5, font=("Arial", 10))
entry_count.pack(side=tk.LEFT, padx=3)

tk.Label(input_frame, text="Мин:", font=("Arial", 10)).pack(side=tk.LEFT, padx=(10, 0))
entry_min = tk.Entry(input_frame, width=5, font=("Arial", 10))
entry_min.pack(side=tk.LEFT, padx=3)

tk.Label(input_frame, text="Макс:", font=("Arial", 10)).pack(side=tk.LEFT, padx=(10, 0))
entry_max = tk.Entry(input_frame, width=5, font=("Arial", 10))
entry_max.pack(side=tk.LEFT, padx=3)

btn_frame = tk.Frame(root)
btn_frame.pack(fill=tk.X, padx=10, pady=5)

tk.Button(btn_frame, text="Создать", command=btn_create, font=("Arial", 10), width=10).pack(side=tk.LEFT, padx=3)
tk.Button(btn_frame, text="Добавить", command=btn_enqueue, font=("Arial", 10), width=10).pack(side=tk.LEFT, padx=3)
tk.Button(btn_frame, text="Удалить", command=btn_dequeue, font=("Arial", 10), width=10).pack(side=tk.LEFT, padx=3)
tk.Button(btn_frame, text="Peek", command=btn_peek, font=("Arial", 10), width=10).pack(side=tk.LEFT, padx=3)
tk.Button(btn_frame, text="Случайные", command=btn_random, font=("Arial", 10), width=10).pack(side=tk.LEFT, padx=3)
tk.Button(btn_frame, text="Очистить", command=btn_clear, font=("Arial", 10), width=10).pack(side=tk.LEFT, padx=3)

log_text = tk.Text(root, height=6, font=("Consolas", 10), state=tk.DISABLED, bg="#f5f5f5")
log_text.pack(fill=tk.BOTH, padx=10, pady=5, expand=True)

root.mainloop()
