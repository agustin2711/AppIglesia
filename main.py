import tkinter as tk
import requests
import json
import sys
import os
from tkinter import colorchooser
from PIL import Image, ImageTk
import threading

def resource_path(relative_path):
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS  # cuando es EXE (PyInstaller)
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(base_path, relative_path)


def config_path():
    if getattr(sys, 'frozen', False):
        # EXE → junto al ejecutable
        return os.path.join(os.path.dirname(sys.executable), "config.json")
    else:
        # Python normal
        return "config.json"
    
# ================= CONFIG =================
CONFIG_FILE = config_path()
EMOJI_DIR = resource_path("emojis")
ICON_DIR = resource_path("iconos")

COLOR_TEXTO = "#000000"
COLOR_BARRA = "#e3e3e3"
COLOR_RESALTADO = "#ffff00"

# ================= EMOJIS =================
EMOJI_MAP = {
    "🔴": "1f534.png",
    "🟢": "1f7e2.png",
    "🟠": "1f7e0.png",
    "🟡": "1f7e1.png",
    "🔵": "1f535.png",
    "⚪️": "26aa.png",
    "⚫️": "26ab.png",
    "⏰": "23f0.png",
    "📅": "1f4c5.png",
    "📝": "1f4dd.png",
    "📍": "1f4cd.png",
    "🎤": "1f3a4.png",
    "🎶": "1f3b6.png",
    "🔊": "1f50a.png",
    "➡️": "27a1.png",
    "👉": "1f449.png",
    "❗": "2757.png",
    "📖": "1f4d6.png",
}

emoji_images = {}
ultima_version = 0
ultimo_texto = None
# ================= CONFIG FILE =================
def cargar_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {}

def guardar_config():
    with open(CONFIG_FILE, "w") as f:
        json.dump({
            "geometry": ventana.geometry(),
            "font_size": font_size.get(),
            "url_crud": url_crud,
            "url_web": url_web
        }, f, indent=4)

# ================= EMOJIS =================
def cargar_emojis(size):
    emoji_images.clear()
    px = int(size * 0.9)
    for e, f in EMOJI_MAP.items():
        p = os.path.join(EMOJI_DIR, f)
        if os.path.exists(p):
            img = Image.open(p).convert("RGBA").resize((px, px), Image.LANCZOS)
            emoji_images[e] = ImageTk.PhotoImage(img)

def insertar_texto_con_emojis(texto):
    texto_widget.config(state="normal")
    texto_widget.delete("1.0", "end")

    i = 0
    while i < len(texto):
        for e in sorted(emoji_images, key=len, reverse=True):
            if texto.startswith(e, i):
                texto_widget.image_create("end", image=emoji_images[e])
                i += len(e)
                break
        else:
            texto_widget.insert("end", texto[i])
            i += 1

    texto_widget.config(state="disabled")

# ================= RESALTADO =================
def cambiar_color_actual(event=None):
    global COLOR_RESALTADO
    color = colorchooser.askcolor(title="Elegir color de resaltado")
    if color[1]:
        COLOR_RESALTADO = color[1]
        color_canvas.itemconfig(color_rect, fill=COLOR_RESALTADO)

def aplicar_resaltado():
    try:
        start = texto_widget.index("sel.first")
        end = texto_widget.index("sel.last")
    except tk.TclError:
        return

    texto_widget.tag_add("resaltado", start, end)
    texto_widget.tag_config("resaltado", background=COLOR_RESALTADO)

def quitar_resaltado_seleccion():
    try:
        start = texto_widget.index("sel.first")
        end = texto_widget.index("sel.last")
    except tk.TclError:
        return

    texto_widget.tag_remove("resaltado", start, end)

def limpiar_todo_resaltado():
    texto_widget.tag_remove("resaltado", "1.0", "end")

# ================= LONG POLLING =================
def loop_long_polling():
    global ultimo_texto, ultima_version

    while True:
        try:
            url = f"{url_crud}?version={ultima_version}"
            resp = requests.get(url, timeout=15)

            if resp.status_code == 200:
                data = resp.json()
                texto = data["texto"]
                version = data["version"]

                ventana.after(0, set_estado, True)

                if version != ultima_version:
                    ultima_version = version
                    ultimo_texto = texto
                    ventana.after(0, insertar_texto_con_emojis, texto)

            elif resp.status_code == 204:
                pass

        except Exception:
            ventana.after(0, set_estado, False)




# ================= ESTADO =================
def set_estado(conectado):
    img = icon_ok if conectado else icon_bad
    estado_icon.config(image=img)
    estado_icon.image = img
    estado_label.config(text="Conectado" if conectado else "Desconectado")

# ================= URL POPUP =================
def mostrar_info_urls():
    popup = tk.Toplevel(ventana)
    popup.title("Información de conexión")
    popup.resizable(False, False)
    popup.transient(ventana)
    popup.grab_set()

    w, h = 500, 400
    x = ventana.winfo_x() + (ventana.winfo_width() - w)//2
    y = ventana.winfo_y() + (ventana.winfo_height() - h)//2
    popup.geometry(f"{w}x{h}+{x}+{y}")

    frame = tk.Frame(popup, padx=12, pady=12)
    frame.pack(expand=True, fill="both")

    tk.Label(frame, text="URL API (CRUD)", font=("Arial", 10, "bold")).pack(anchor="w")
    entry_crud = tk.Entry(frame)
    entry_crud.insert(0, url_crud)
    entry_crud.config(state="readonly")
    entry_crud.pack(fill="x", pady=(0, 10))

    tk.Label(frame, text="URL Web", font=("Arial", 10, "bold")).pack(anchor="w")
    entry_web = tk.Entry(frame)
    entry_web.insert(0, url_web)
    entry_web.config(state="readonly")
    entry_web.pack(fill="x")

    tk.Label(frame, text="Acceso rápido (QR)", font=("Arial", 10, "bold")).pack(pady=(12, 6))
    qr_label = tk.Label(frame, image=icon_qr)
    qr_label.image = icon_qr 
    qr_label.pack()

    tk.Button(frame, text="Cerrar", command=popup.destroy).pack(pady=12)


# ================= TK =================
ventana = tk.Tk()
ventana.title("Texto Iglesia")
ventana.attributes("-topmost", True)

config = cargar_config()
url_crud = config.get("url_crud", "REEMPLAZAR_URL_API")
url_web = config.get("url_web", "REEMPLAZAR_URL_WEB")


if "geometry" in config:
    ventana.geometry(config["geometry"])

font_size = tk.IntVar(value=config.get("font_size", 14))

icon_ok = ImageTk.PhotoImage(Image.open(f"{ICON_DIR}/conectado.png").resize((14,14)))
icon_bad = ImageTk.PhotoImage(Image.open(f"{ICON_DIR}/desconectado.png").resize((14,14)))

icon_resaltar = ImageTk.PhotoImage(
    Image.open(f"{ICON_DIR}/resaltar.png").resize((18,18), Image.LANCZOS)
)

icon_sin_color = ImageTk.PhotoImage(
    Image.open(f"{ICON_DIR}/sin_color.png").resize((18,18), Image.LANCZOS)
)

icon_limpiar = ImageTk.PhotoImage(
    Image.open(f"{ICON_DIR}/limpiar.png").resize((18,18), Image.LANCZOS)
)
icon_qr = ImageTk.PhotoImage(
    Image.open(f"{ICON_DIR}/codigoQR.png").resize((160, 160), Image.LANCZOS)
)
# ================= BARRA =================

barra = tk.Frame(ventana, bg=COLOR_BARRA, padx=10, pady=10)
barra.pack(fill="x")

tk.Label(barra, text="Fuente", bg=COLOR_BARRA).pack(side="left")
tk.Spinbox(barra, from_=8, to=48, textvariable=font_size, width=5).pack(side="left")

color_canvas = tk.Canvas(barra, width=18, height=18, highlightthickness=1)
color_canvas.pack(side="left", padx=4)
color_rect = color_canvas.create_rectangle(
    0, 0, 18, 18, fill=COLOR_RESALTADO, outline="black"
)
color_canvas.bind("<Button-1>", cambiar_color_actual)

tk.Button(
    barra,
    image=icon_resaltar,
    command=aplicar_resaltado,
    bd=0,
    bg=COLOR_BARRA,
    activebackground=COLOR_BARRA
).pack(side="left", padx=4)

tk.Button(
    barra,
    image=icon_sin_color,
    command=quitar_resaltado_seleccion,
    bd=0,
    bg=COLOR_BARRA,
    activebackground=COLOR_BARRA
).pack(side="left", padx=4)

tk.Button(
    barra,
    image=icon_limpiar,
    command=limpiar_todo_resaltado,
    bd=0,
    bg=COLOR_BARRA,
    activebackground=COLOR_BARRA
).pack(side="left", padx=6)


tk.Button(barra, text="Info", command=mostrar_info_urls).pack(side="right", padx=10)




estado_icon = tk.Label(barra, image=icon_bad, bg=COLOR_BARRA)
estado_icon.pack(side="right", padx=5)
estado_label = tk.Label(barra, text="Desconectado", bg=COLOR_BARRA)
estado_label.pack(side="right")

# ================= TEXTO =================
texto_widget = tk.Text(
    ventana,
    wrap="word",
    font=("Arial", font_size.get()),
    bd=0,
    fg=COLOR_TEXTO,
    highlightthickness=0
)
texto_widget.pack(fill="both", expand=True)
texto_widget.config(state="disabled")

# ================= LOOP =================
def actualizar():
    threading.Thread(target=loop_long_polling, daemon=True).start()


def on_font_change(*_):
    texto_widget.config(font=("Arial", font_size.get()))
    cargar_emojis(font_size.get())
    if ultimo_texto:
        insertar_texto_con_emojis(ultimo_texto)

font_size.trace_add("write", on_font_change)

# ================= INIT =================
cargar_emojis(font_size.get())
actualizar()

ventana.protocol("WM_DELETE_WINDOW", lambda: (guardar_config(), ventana.destroy()))
ventana.mainloop()
